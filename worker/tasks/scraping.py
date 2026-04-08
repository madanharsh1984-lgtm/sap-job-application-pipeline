import logging

import httpx

from worker.celery_app import celery_app
from worker.config import settings

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, max_retries=3)
def trigger_job_scrape(self, user_id: int, search_params: dict) -> dict:
    """Trigger a job scraping task via the browser service.

    Args:
        user_id: The ID of the user requesting the scrape.
        search_params: Dictionary with keys like keywords, location, source.

    Returns:
        Dictionary with scraping results summary.
    """
    logger.info(
        "Starting job scrape for user_id=%d with params=%s",
        user_id,
        search_params,
    )

    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(
                "http://browser-service:9000/api/scrape",
                json=search_params,
            )
            response.raise_for_status()
            raw_jobs = response.json().get("jobs", [])

        logger.info(
            "Scrape completed for user_id=%d, found %d jobs",
            user_id,
            len(raw_jobs),
        )

        process_scraped_jobs.delay(user_id, raw_jobs)

        return {"status": "success", "jobs_found": len(raw_jobs)}

    except httpx.HTTPStatusError as exc:
        logger.error(
            "Browser service returned error %d for user_id=%d: %s",
            exc.response.status_code,
            user_id,
            exc.response.text,
        )
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 10)

    except Exception as exc:
        logger.exception(
            "Unexpected error during scrape for user_id=%d", user_id
        )
        raise self.retry(exc=exc, countdown=2 ** self.request.retries * 10)


@celery_app.task
def process_scraped_jobs(user_id: int, raw_jobs: list) -> dict:
    """Parse, normalize, and store scraped job data via the backend API.

    Args:
        user_id: The ID of the user who owns these jobs.
        raw_jobs: List of raw job dictionaries from the scraper.

    Returns:
        Dictionary with processing results summary.
    """
    logger.info(
        "Processing %d scraped jobs for user_id=%d", len(raw_jobs), user_id
    )

    stored = 0
    errors = 0

    with httpx.Client(timeout=30.0) as client:
        for raw_job in raw_jobs:
            normalized = {
                "title": raw_job.get("title", "").strip(),
                "company": raw_job.get("company", "").strip(),
                "location": raw_job.get("location", "").strip(),
                "url": raw_job.get("url", "").strip(),
                "source": raw_job.get("source", "unknown"),
                "description": raw_job.get("description", ""),
            }

            try:
                response = client.post(
                    f"{settings.API_BASE_URL}/api/v1/jobs",
                    json={"user_id": user_id, **normalized},
                )
                response.raise_for_status()
                stored += 1
            except httpx.HTTPError:
                logger.warning(
                    "Failed to store job '%s' for user_id=%d",
                    normalized.get("title"),
                    user_id,
                )
                errors += 1

    logger.info(
        "Finished processing jobs for user_id=%d: stored=%d, errors=%d",
        user_id,
        stored,
        errors,
    )

    return {"stored": stored, "errors": errors}
