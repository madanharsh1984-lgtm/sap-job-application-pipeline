"""
Celery tasks for the keyword deduplication + shared scraping pipeline.

Task flow:
  1. process_resume_task — orchestrator: extract → normalize → dedup check → scrape
  2. trigger_apify_task — runs Apify for a keyword set (only if no cache hit)
  3. store_jobs_task   — stores scraped jobs in the database
"""

import json
import logging

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from backend.app.core.config import settings
from backend.app.services.keyword_engine import process_resume_keywords
from backend.app.services.apify_service import run_apify_scrape
from backend.app.services.cache import (
    is_scrape_done,
    mark_scrape_processing,
    mark_scrape_done,
    clear_scrape_status,
)
from backend.app.models.keyword_set import KeywordSet
from backend.app.models.user_keyword_map import UserKeywordMap
from backend.app.models.resume import Resume
from backend.app.models.job import Job
from backend.app.tasks.celery_app import celery_app

logger = logging.getLogger(__name__)

# Sync engine for Celery workers (Celery is synchronous)
_sync_engine = None


def _get_sync_engine():
    global _sync_engine
    if _sync_engine is None:
        _sync_engine = create_engine(settings.DATABASE_URL_SYNC, pool_pre_ping=True)
    return _sync_engine


def _get_sync_session() -> Session:
    return Session(_get_sync_engine())


# ═══════════════════════════════════════════════════════════════════════════════
# TASK 1: Process Resume (Orchestrator)
# ═══════════════════════════════════════════════════════════════════════════════

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def process_resume_task(self, user_id: int, resume_text: str) -> dict:
    """
    Full pipeline for a new resume upload:
      1. Extract + normalize keywords
      2. Hash the keyword set
      3. Check if keyword_set exists (dedup)
      4. Create/reuse keyword_set in DB
      5. Map user to keyword_set
      6. If new keyword_set → trigger Apify
      7. If existing → user gets shared results immediately

    Note: Resume raw_text is truncated to 10,000 characters before storage
    to limit database row size. Keyword extraction runs on the full text.

    Returns dict with keyword_hash and is_new.
      6. If new keyword_set → trigger Apify
      7. If existing → user gets shared results immediately

    Returns dict with keyword_hash and is_new.
    """
    try:
        # Step 1–2: Extract, normalize, hash
        normalized_keywords, keyword_hash = process_resume_keywords(resume_text)
        logger.info(
            "User %d: extracted %d keywords, hash=%s",
            user_id, len(normalized_keywords), keyword_hash[:16]
        )

        with _get_sync_session() as db:
            # Step 3: Save resume (truncate to 10k chars to prevent excessive DB storage)
            resume = Resume(
                user_id=user_id,
                raw_text=resume_text[:10000],
                parsed_data=json.dumps(normalized_keywords),
            )
            db.add(resume)

            # Step 4: Check for existing keyword_set (dedup!)
            existing = db.execute(
                select(KeywordSet).where(KeywordSet.keyword_hash == keyword_hash)
            ).scalar_one_or_none()

            is_new = existing is None

            if existing:
                keyword_set = existing
                logger.info(
                    "User %d: DEDUP HIT — reusing keyword_set id=%d (hash=%s)",
                    user_id, keyword_set.id, keyword_hash[:16]
                )
            else:
                # Create new keyword_set
                keyword_set = KeywordSet(
                    keyword_hash=keyword_hash,
                    normalized_keywords=json.dumps(normalized_keywords),
                )
                db.add(keyword_set)
                db.flush()  # get the ID
                logger.info(
                    "User %d: NEW keyword_set id=%d (hash=%s)",
                    user_id, keyword_set.id, keyword_hash[:16]
                )

            # Step 5: Map user → keyword_set (skip if already mapped)
            existing_map = db.execute(
                select(UserKeywordMap).where(
                    UserKeywordMap.user_id == user_id,
                    UserKeywordMap.keyword_set_id == keyword_set.id,
                )
            ).scalar_one_or_none()

            if not existing_map:
                db.add(UserKeywordMap(
                    user_id=user_id,
                    keyword_set_id=keyword_set.id,
                ))

            db.commit()
            keyword_set_id = keyword_set.id

        # Step 6: Trigger Apify ONLY for new keyword sets
        if is_new:
            trigger_apify_task.delay(keyword_set_id, keyword_hash, normalized_keywords)

        return {
            "keyword_hash": keyword_hash,
            "keywords": normalized_keywords,
            "is_new": is_new,
            "keyword_set_id": keyword_set_id,
        }

    except Exception as exc:
        logger.exception("process_resume_task failed for user %d", user_id)
        raise self.retry(exc=exc)


# ═══════════════════════════════════════════════════════════════════════════════
# TASK 2: Trigger Apify (Only for New Keyword Sets)
# ═══════════════════════════════════════════════════════════════════════════════

@celery_app.task(bind=True, max_retries=3, default_retry_delay=30)
def trigger_apify_task(
    self,
    keyword_set_id: int,
    keyword_hash: str,
    keywords: list[str],
) -> dict:
    """
    Trigger Apify scraping for a keyword set.

    Fail-safe:
      - Redis lock prevents duplicate concurrent calls
      - If Apify fails → Celery retries with exponential backoff
      - DB unique constraint on keyword_hash prevents duplicates even under race
    """
    try:
        # Check Redis cache first
        if is_scrape_done(keyword_hash):
            logger.info("Apify already done for hash=%s, skipping", keyword_hash[:16])
            return {"status": "already_done", "keyword_hash": keyword_hash}

        # Acquire processing lock
        if not mark_scrape_processing(keyword_hash):
            logger.info("Apify already in progress for hash=%s, skipping", keyword_hash[:16])
            return {"status": "in_progress", "keyword_hash": keyword_hash}

        logger.info("Starting Apify scrape for keyword_set=%d (hash=%s)", keyword_set_id, keyword_hash[:16])

        # Run the actual Apify scrape
        job_results = run_apify_scrape(keywords)

        if not job_results:
            logger.warning("Apify returned 0 results for hash=%s", keyword_hash[:16])
            clear_scrape_status(keyword_hash)
            return {"status": "no_results", "keyword_hash": keyword_hash}

        # Store jobs in DB
        store_jobs_task.delay(keyword_set_id, keyword_hash, job_results)

        return {
            "status": "success",
            "keyword_hash": keyword_hash,
            "jobs_found": len(job_results),
        }

    except Exception as exc:
        logger.exception("trigger_apify_task failed for hash=%s", keyword_hash[:16])
        clear_scrape_status(keyword_hash)
        raise self.retry(exc=exc)


# ═══════════════════════════════════════════════════════════════════════════════
# TASK 3: Store Jobs in Database
# ═══════════════════════════════════════════════════════════════════════════════

@celery_app.task(bind=True, max_retries=3, default_retry_delay=10)
def store_jobs_task(
    self,
    keyword_set_id: int,
    keyword_hash: str,
    job_results: list[dict],
) -> dict:
    """
    Store scraped jobs in the database, linked to the keyword_set.
    Deduplicates by external_id to prevent storing the same job twice.
    """
    try:
        stored_count = 0

        with _get_sync_session() as db:
            for job_dict in job_results:
                external_id = job_dict.get("external_id")

                # Skip if already stored
                if external_id:
                    existing = db.execute(
                        select(Job).where(
                            Job.keyword_set_id == keyword_set_id,
                            Job.external_id == external_id,
                        )
                    ).scalar_one_or_none()
                    if existing:
                        continue

                job = Job(
                    keyword_set_id=keyword_set_id,
                    external_id=external_id,
                    title=job_dict.get("title", "Untitled"),
                    company=job_dict.get("company"),
                    location=job_dict.get("location"),
                    email=job_dict.get("email"),
                    post_url=job_dict.get("post_url"),
                    job_data=job_dict.get("job_data", "{}"),
                    source=job_dict.get("source"),
                )
                db.add(job)
                stored_count += 1

            db.commit()

        # Mark scrape as done in Redis
        mark_scrape_done(keyword_hash)

        logger.info(
            "Stored %d jobs for keyword_set=%d (hash=%s)",
            stored_count, keyword_set_id, keyword_hash[:16]
        )

        return {
            "status": "stored",
            "keyword_hash": keyword_hash,
            "stored_count": stored_count,
        }

    except Exception as exc:
        logger.exception("store_jobs_task failed for hash=%s", keyword_hash[:16])
        raise self.retry(exc=exc)
