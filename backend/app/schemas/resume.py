"""Pydantic schemas for resume operations."""

from datetime import datetime

from pydantic import BaseModel


class ResumeCreate(BaseModel):
    """Schema for creating a resume record."""

    filename: str
    target_job_id: int | None = None


class ResumeResponse(BaseModel):
    """Schema for resume API responses."""

    id: int
    user_id: int
    filename: str
    s3_key: str | None
    version: int
    is_tailored: bool
    target_job_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}
