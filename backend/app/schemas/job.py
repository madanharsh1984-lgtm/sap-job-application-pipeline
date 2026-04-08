"""Pydantic schemas for job operations."""

from datetime import datetime

from pydantic import BaseModel


class JobCreate(BaseModel):
    """Schema for creating a job listing."""

    title: str
    company: str
    location: str | None = None
    description: str | None = None
    url: str | None = None
    source: str | None = None
    salary_range: str | None = None


class JobUpdate(BaseModel):
    """Schema for updating a job listing."""

    title: str | None = None
    company: str | None = None
    location: str | None = None
    status: str | None = None


class JobResponse(BaseModel):
    """Schema for job API responses."""

    id: int
    user_id: int
    title: str
    company: str | None
    location: str | None
    description: str | None
    url: str | None
    source: str | None
    status: str
    salary_range: str | None
    created_at: datetime
    updated_at: datetime | None

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    """Schema for paginated job list responses."""

    jobs: list[JobResponse]
    total: int
    page: int
    per_page: int
