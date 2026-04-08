"""Job listing and dashboard routes.

FSD Modules: M1 - Job Discovery Engine, M4.C - Dashboard
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.models.application import Application
from backend.app.models.job import Job
from backend.app.schemas.job import DashboardResponse, JobListResponse, JobResponse

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=JobListResponse)
async def list_jobs(
    source: str | None = Query(None, description="Filter by source platform"),
    remote_only: bool = Query(False, description="Show only remote jobs"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
):
    """List discovered jobs with optional filters."""
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
    query = select(Job).where(Job.scraped_at >= seven_days_ago)

    if source:
        query = query.where(Job.source == source)
    if remote_only:
        query = query.where(Job.is_remote.is_(True))

    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar() or 0

    query = query.order_by(Job.scraped_at.desc()).limit(limit).offset(offset)
    result = await db.execute(query)
    jobs = [JobResponse.model_validate(j) for j in result.scalars().all()]

    return JobListResponse(total=total, jobs=jobs)


@router.get("/dashboard", response_model=DashboardResponse)
async def dashboard(
    user_id: str = Query(..., description="Current user ID"),
    db: AsyncSession = Depends(get_db),
):
    """Get dashboard summary: eligible jobs, total recent jobs, applications sent."""
    seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)

    total_jobs = (
        await db.execute(
            select(func.count()).where(Job.scraped_at >= seven_days_ago)
        )
    ).scalar() or 0

    applications_sent = (
        await db.execute(
            select(func.count()).where(Application.user_id == user_id)
        )
    ).scalar() or 0

    return DashboardResponse(
        eligible_job_count=total_jobs,
        total_jobs_last_7_days=total_jobs,
        applications_sent=applications_sent,
        plan="free",
    )
