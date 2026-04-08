"""
Pydantic schemas for API request/response validation.
"""

from datetime import datetime

from pydantic import BaseModel, EmailStr


# ── Auth ─────────────────────────────────────────────────────────────────────

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    created_at: datetime

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Resume / Onboarding ─────────────────────────────────────────────────────

class OnboardRequest(BaseModel):
    resume_text: str


class OnboardResponse(BaseModel):
    message: str
    keyword_hash: str
    keywords: list[str]
    is_new_keyword_set: bool


# ── Jobs ─────────────────────────────────────────────────────────────────────

class JobResponse(BaseModel):
    id: int
    title: str
    company: str | None
    location: str | None
    email: str | None
    post_url: str | None
    source: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class JobListResponse(BaseModel):
    total: int
    keyword_hash: str | None
    jobs: list[JobResponse]


# ── Keyword Set ──────────────────────────────────────────────────────────────

class KeywordSetResponse(BaseModel):
    id: int
    keyword_hash: str
    normalized_keywords: str
    created_at: datetime

    model_config = {"from_attributes": True}
