from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Enum, Text, UUID
from sqlalchemy.orm import relationship
from database import Base
import datetime
import uuid

class User(Base):
    __tablename__ = "users"
    user_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    subscription_tier = Column(String, default="Free") # Enum in real prod
    name = Column(String)
    phone = Column(String, unique=True, index=True)
    is_email_verified = Column(Boolean, default=False)
    is_phone_verified = Column(Boolean, default=False)
    linkedin_id = Column(String)
    linkedin_profile_score = Column(Integer)
    is_beta_tester = Column(Boolean, default=False)
    beta_access_code = Column(String)
    onboarding_step = Column(Integer, default=0) # 0: Profile, 1: Verification, 2: LinkedIn, 3: Completed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # OTP Storage
    email_otp = Column(String)
    phone_otp = Column(String)
    
    credentials = relationship("UserCredential", back_populates="user")
    resumes = relationship("Resume", back_populates="user")
    applications = relationship("Application", back_populates="user")

class UserCredential(Base):
    __tablename__ = "user_credentials"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    platform = Column(String) # LinkedIn, Naukri, Gmail
    secret_path = Column(String) # Path in AWS Secrets Manager
    status = Column(String, default="Active")
    
    user = relationship("User", back_populates="credentials")

class JobLead(Base):
    __tablename__ = "job_leads"
    lead_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    platform = Column(String)
    job_title = Column(String)
    company = Column(String)
    location = Column(String)
    raw_text = Column(Text)
    recruiter_email = Column(String)
    scraped_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    applications = relationship("Application", back_populates="lead")

class Resume(Base):
    __tablename__ = "resumes"
    resume_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    file_name = Column(String)
    s3_path = Column(String)
    is_base = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="resumes")
    applications = relationship("Application", back_populates="resume")

class Application(Base):
    __tablename__ = "applications"
    app_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.user_id"))
    lead_id = Column(UUID(as_uuid=True), ForeignKey("job_leads.lead_id"))
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.resume_id"))
    status = Column(String, default="Pending")
    log = Column(Text)
    sent_at = Column(DateTime)
    
    user = relationship("User", back_populates="applications")
    lead = relationship("JobLead", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")
