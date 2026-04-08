"""
Admin routes — dashboard metrics, user management, job listing.

All endpoints require admin role (enforced via get_current_admin dependency).
"""

from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.core.database import get_db
from backend.app.core.security import get_current_admin
from backend.app.models.user import User
from backend.app.models.job import Job
from backend.app.models.keyword_set import KeywordSet
from backend.app.models.resume import Resume
from backend.app.models.user_keyword_map import UserKeywordMap
from backend.app.schemas.api import (
    AdminMetrics,
    AdminUserResponse,
    AdminUserListResponse,
    AdminJobListResponse,
    JobResponse,
)

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.get("/metrics", response_model=AdminMetrics)
async def admin_metrics(
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """Dashboard metrics for admin portal."""
    users_count = (await db.execute(select(func.count(User.id)))).scalar() or 0
    jobs_count = (await db.execute(select(func.count(Job.id)))).scalar() or 0
    ks_count = (await db.execute(select(func.count(KeywordSet.id)))).scalar() or 0
    resumes_count = (await db.execute(select(func.count(Resume.id)))).scalar() or 0

    return AdminMetrics(
        total_users=users_count,
        total_jobs=jobs_count,
        total_keyword_sets=ks_count,
        total_resumes=resumes_count,
    )


@router.get("/users", response_model=AdminUserListResponse)
async def admin_users(
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all users with resume/keyword counts."""
    result = await db.execute(select(User).order_by(User.created_at.desc()))
    users = result.scalars().all()

    user_list = []
    for u in users:
        # Count resumes
        res_count = (
            await db.execute(
                select(func.count(Resume.id)).where(Resume.user_id == u.id)
            )
        ).scalar() or 0

        # Count keyword set mappings
        ks_count = (
            await db.execute(
                select(func.count(UserKeywordMap.id)).where(
                    UserKeywordMap.user_id == u.id
                )
            )
        ).scalar() or 0

        user_list.append(
            AdminUserResponse(
                id=u.id,
                email=u.email,
                role=u.role,
                created_at=u.created_at,
                resume_count=res_count,
                keyword_set_count=ks_count,
            )
        )

    return AdminUserListResponse(total=len(user_list), users=user_list)


@router.get("/jobs", response_model=AdminJobListResponse)
async def admin_jobs(
    _admin: User = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db),
):
    """List all jobs across all keyword sets."""
    result = await db.execute(
        select(Job).order_by(Job.created_at.desc()).limit(500)
    )
    jobs = result.scalars().all()

    return AdminJobListResponse(
        total=len(jobs),
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
