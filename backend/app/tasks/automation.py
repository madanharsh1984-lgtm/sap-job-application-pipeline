from app.celery_app import celery_app
from app.services.apply_service import trigger_linkedin_apply
from app.services.email_service import trigger_emails
from app.services.job_service import trigger_scrape


@celery_app.task(name='app.tasks.automation.run_scrape')
def run_scrape():
    return trigger_scrape()


@celery_app.task(name='app.tasks.automation.run_email')
def run_email():
    return trigger_emails()


@celery_app.task(name='app.tasks.automation.run_apply')
def run_apply():
    return trigger_linkedin_apply()
