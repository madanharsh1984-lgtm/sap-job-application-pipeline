"""Pydantic schemas for application operations."""

from datetime import datetime

from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    """Schema for creating a job application."""

    job_id: int
    notes: str | None = None
    resume_used: str | None = None


class ApplicationUpdate(BaseModel):
    """Schema for updating a job application."""

    status: str | None = None
    notes: str | None = None


class ApplicationResponse(BaseModel):
    """Schema for application API responses."""

    id: int
    user_id: int
    job_id: int
    status: str
    applied_at: datetime | None
    notes: str | None
    resume_used: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
