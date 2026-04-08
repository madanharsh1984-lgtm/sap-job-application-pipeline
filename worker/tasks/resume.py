import logging

import httpx

from worker.celery_app import celery_app
from worker.config import settings

logger = logging.getLogger(__name__)


@celery_app.task
def generate_tailored_resume(
    user_id: int, job_id: int, base_resume_key: str
) -> dict:
    """Generate a tailored resume for a specific job posting.

    This is a placeholder that will be replaced with actual AI-powered
    resume tailoring in production.

    Args:
        user_id: The ID of the user.
        job_id: The ID of the target job posting.
        base_resume_key: S3 key or identifier for the base resume template.

    Returns:
        Dictionary containing the new resume ID and metadata.
    """
    logger.info(
        "Generating tailored resume for user_id=%d, job_id=%d, base_key=%s",
        user_id,
        job_id,
        base_resume_key,
    )

    try:
        with httpx.Client(timeout=30.0) as client:
            job_response = client.get(
                f"{settings.API_BASE_URL}/api/v1/jobs/{job_id}",
            )
            job_response.raise_for_status()
            job_data = job_response.json()

        logger.info(
            "Fetched job details for job_id=%d: title='%s'",
            job_id,
            job_data.get("title", "N/A"),
        )

        # Placeholder: AI-based resume tailoring will be integrated here.
        # For now, we create a mock tailored resume record.
        tailored_content = {
            "base_resume_key": base_resume_key,
            "target_job_title": job_data.get("title", ""),
            "target_company": job_data.get("company", ""),
            "tailored": True,
        }

        with httpx.Client(timeout=30.0) as client:
            upload_response = client.post(
                f"{settings.API_BASE_URL}/api/v1/resumes",
                json={
                    "user_id": user_id,
                    "job_id": job_id,
                    "content": tailored_content,
                },
            )
            upload_response.raise_for_status()
            result = upload_response.json()

        resume_id = result.get("id")
        logger.info(
            "Tailored resume created with id=%s for user_id=%d, job_id=%d",
            resume_id,
            user_id,
            job_id,
        )

        return {"resume_id": resume_id, "status": "success"}

    except httpx.HTTPError:
        logger.exception(
            "HTTP error while generating resume for user_id=%d, job_id=%d",
            user_id,
            job_id,
        )
        return {"resume_id": None, "status": "error"}

    except Exception:
        logger.exception(
            "Unexpected error generating resume for user_id=%d, job_id=%d",
            user_id,
            job_id,
        )
        return {"resume_id": None, "status": "error"}
