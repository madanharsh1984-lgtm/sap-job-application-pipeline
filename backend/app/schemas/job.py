"""Pydantic schemas for job-related API operations."""

import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class JobResponse(BaseModel):
    """Schema for job listing returned to the client."""

    id: uuid.UUID
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    description: Optional[str] = None
    url: Optional[str] = None
    source: str
    is_remote: bool
    posted_at: Optional[datetime] = None
    scraped_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    """Paginated list of jobs."""

    total: int
    jobs: list[JobResponse]


class DashboardResponse(BaseModel):
    """Dashboard summary for the user."""

    eligible_job_count: int
    total_jobs_last_7_days: int
    applications_sent: int
    plan: str
