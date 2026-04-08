"""
Onboarding + Jobs routes — the core keyword deduplication API.

POST /api/user/onboard  — upload resume text, trigger keyword pipeline
GET  /api/jobs           — fetch jobs mapped to the current user
"""

import json

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import get_current_user
from backend.app.models.user import User
from backend.app.models.keyword_set import KeywordSet
from backend.app.models.user_keyword_map import UserKeywordMap
from backend.app.models.job import Job
from backend.app.schemas.api import OnboardRequest, OnboardResponse, JobListResponse, JobResponse
from backend.app.services.keyword_engine import process_resume_keywords
from backend.app.tasks.scraping import process_resume_task

router = APIRouter(prefix="/api", tags=["jobs"])


# ═══════════════════════════════════════════════════════════════════════════════
# POST /user/onboard — Upload resume and trigger keyword dedup pipeline
# ═══════════════════════════════════════════════════════════════════════════════

@router.post("/user/onboard", response_model=OnboardResponse)
async def onboard_user(
    body: OnboardRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    User onboarding flow:
      1. Receive resume text
      2. Extract + normalize keywords → generate hash
      3. Check if keyword_set exists (dedup check)
      4. If exists → map user, return existing jobs
      5. If new → create keyword_set, queue Apify task
    """
    if not body.resume_text or len(body.resume_text.strip()) < 50:
        raise HTTPException(status_code=400, detail="Resume text too short (min 50 chars)")

    # Synchronous keyword processing (fast — no I/O)
    normalized_keywords, keyword_hash = process_resume_keywords(body.resume_text)

    if not normalized_keywords:
        raise HTTPException(status_code=400, detail="No keywords could be extracted from resume")

    # Check for existing keyword_set
    result = await db.execute(
        select(KeywordSet).where(KeywordSet.keyword_hash == keyword_hash)
    )
    existing_ks = result.scalar_one_or_none()
    is_new = existing_ks is None

    if existing_ks:
        keyword_set = existing_ks
    else:
        keyword_set = KeywordSet(
            keyword_hash=keyword_hash,
            normalized_keywords=json.dumps(normalized_keywords),
        )
        db.add(keyword_set)
        await db.flush()

    # Map user → keyword_set (if not already mapped)
    map_result = await db.execute(
        select(UserKeywordMap).where(
            UserKeywordMap.user_id == user.id,
            UserKeywordMap.keyword_set_id == keyword_set.id,
        )
    )
    if not map_result.scalar_one_or_none():
        db.add(UserKeywordMap(user_id=user.id, keyword_set_id=keyword_set.id))
        await db.flush()

    # Queue background task for full processing (resume save + Apify if needed)
    process_resume_task.delay(user.id, body.resume_text)

    return OnboardResponse(
        message="Resume processed. Jobs will be available shortly."
        if is_new
        else "Keywords matched existing set. Jobs are already available.",
        keyword_hash=keyword_hash,
        keywords=normalized_keywords,
        is_new_keyword_set=is_new,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# GET /jobs — Fetch jobs for the current user
# ═══════════════════════════════════════════════════════════════════════════════

@router.get("/jobs", response_model=JobListResponse)
async def get_jobs(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch all jobs mapped to the current user via their keyword sets.

    Flow:
      user → user_keyword_map → keyword_set → jobs
    """
    # Get all keyword_set_ids for this user
    map_result = await db.execute(
        select(UserKeywordMap.keyword_set_id).where(UserKeywordMap.user_id == user.id)
    )
    keyword_set_ids = [row[0] for row in map_result.all()]

    if not keyword_set_ids:
        return JobListResponse(total=0, keyword_hash=None, jobs=[])

    # Get the primary keyword hash for display
    ks_result = await db.execute(
        select(KeywordSet.keyword_hash).where(KeywordSet.id == keyword_set_ids[0])
    )
    primary_hash = ks_result.scalar_one_or_none()

    # Fetch all jobs linked to user's keyword sets
    jobs_result = await db.execute(
        select(Job)
        .where(Job.keyword_set_id.in_(keyword_set_ids))
        .order_by(Job.created_at.desc())
        .limit(200)
    )
    jobs = jobs_result.scalars().all()

    return JobListResponse(
        total=len(jobs),
        keyword_hash=primary_hash,
        jobs=[
            JobResponse(
                id=j.id,
                title=j.title,
                company=j.company,
                location=j.location,
                email=j.email,
                post_url=j.post_url,
                source=j.source,
                created_at=j.created_at,
            )
            for j in jobs
        ],
    )
