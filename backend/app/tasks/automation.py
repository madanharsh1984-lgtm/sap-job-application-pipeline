import json
import logging

from app.celery_app import celery_app
from app.core.database import SessionLocal
from app.models.keyword_set import KeywordSet
from app.services.apply_service import trigger_linkedin_apply
from app.services.email_service import trigger_emails
from app.services.job_service import scrape_jobs_from_apify, store_jobs_for_keyword_set

logger = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    name='app.tasks.automation.trigger_apify',
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_backoff_max=300,
    retry_jitter=True,
    max_retries=5,
)
def trigger_apify(self, keyword_set_id: int):
    db = SessionLocal()
    try:
        keyword_set = db.query(KeywordSet).filter(KeywordSet.id == keyword_set_id).first()
        if keyword_set is None:
            return {'status': 'missing_keyword_set', 'keyword_set_id': keyword_set_id}

        keywords = json.loads(keyword_set.normalized_keywords)
        jobs = scrape_jobs_from_apify(keywords)
        inserted = store_jobs_for_keyword_set(db, keyword_set_id, jobs)
        return {'status': 'ok', 'keyword_set_id': keyword_set_id, 'inserted': inserted}
    except Exception:
        logger.exception('Apify scraping task failed for keyword_set_id=%s', keyword_set_id)
        raise
    finally:
        db.close()


@celery_app.task(name='app.tasks.automation.run_email')
def run_email():
    return trigger_emails()


@celery_app.task(name='app.tasks.automation.run_apply')
def run_apply():
    return trigger_linkedin_apply()
