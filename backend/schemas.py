from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    phone: Optional[str] = None
    is_email_verified: bool = False
    is_phone_verified: bool = False
    linkedin_id: Optional[str] = None
    linkedin_profile_score: Optional[int] = None
    onboarding_step: int = 0
    is_beta_tester: bool = False
    beta_access_code: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    linkedin_id: Optional[str] = None
    onboarding_step: Optional[int] = None

class User(UserBase):
    user_id: UUID
    subscription_tier: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OTPVerify(BaseModel):
    phone: str
    code: str

class EmailVerify(BaseModel):
    email: str
    code: str

class JobLeadBase(BaseModel):
    platform: str
    job_title: str
    company: str
    location: str
    raw_text: str
    recruiter_email: Optional[str] = None

class JobLead(JobLeadBase):
    lead_id: UUID
    scraped_at: datetime
    
    class Config:
        from_attributes = True

class ApplicationBase(BaseModel):
    user_id: UUID
    lead_id: UUID
    resume_id: UUID
    status: str
    log: Optional[str] = None

class ApplicationCreate(BaseModel):
    lead_id: UUID
    resume_id: UUID

class Application(ApplicationBase):
    app_id: UUID
    sent_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class WhatsAppLog(BaseModel):
    timestamp: str
    from_num: str
    to_num: str
    message: str
    status: str
