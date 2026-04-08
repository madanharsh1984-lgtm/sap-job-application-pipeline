# =============================================================================
# models.py — Database Schema for Admin Portal (ADMIN_PORTAL_v1)
# =============================================================================
# Tables: users, user_integrations, resumes, jobs, applications,
#          payments, system_logs, ai_logs, admin_settings
# =============================================================================

from datetime import datetime, timezone

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# ── USERS ─────────────────────────────────────────────────────────────────────
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default="user")  # user | admin
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    is_paused = db.Column(db.Boolean, default=False, nullable=False)
    daily_application_limit = db.Column(db.Integer, default=50)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    last_login_at = db.Column(db.DateTime, nullable=True)

    # Relationships
    integrations = db.relationship(
        "UserIntegration", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    resumes = db.relationship(
        "Resume", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    applications = db.relationship(
        "Application", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    payments = db.relationship(
        "Payment", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    ai_logs = db.relationship(
        "AILog", backref="user", lazy=True, cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "role": self.role,
            "is_active": self.is_active,
            "is_paused": self.is_paused,
            "daily_application_limit": self.daily_application_limit,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_login_at": (
                self.last_login_at.isoformat() if self.last_login_at else None
            ),
            "integrations_count": len(self.integrations),
            "resumes_count": len(self.resumes),
            "applications_count": len(self.applications),
        }


# ── USER INTEGRATIONS ────────────────────────────────────────────────────────
class UserIntegration(db.Model):
    __tablename__ = "user_integrations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    platform = db.Column(
        db.String(50), nullable=False
    )  # linkedin | naukri | indeed | email
    status = db.Column(
        db.String(50), default="active"
    )  # active | inactive | error
    credentials_set = db.Column(db.Boolean, default=False)
    last_sync_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "platform": self.platform,
            "status": self.status,
            "credentials_set": self.credentials_set,
            "last_sync_at": (
                self.last_sync_at.isoformat() if self.last_sync_at else None
            ),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── RESUMES ───────────────────────────────────────────────────────────────────
class Resume(db.Model):
    __tablename__ = "resumes"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    filename = db.Column(db.String(500), nullable=False)
    keywords = db.Column(db.Text, nullable=True)  # JSON array of keywords
    is_tailored = db.Column(db.Boolean, default=False)
    target_job_title = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "filename": self.filename,
            "keywords": self.keywords,
            "is_tailored": self.is_tailored,
            "target_job_title": self.target_job_title,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── JOBS ──────────────────────────────────────────────────────────────────────
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    company = db.Column(db.String(255), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    platform = db.Column(
        db.String(50), nullable=False
    )  # linkedin | naukri | indeed | jobspy
    source_url = db.Column(db.String(1000), nullable=True)
    recruiter_email = db.Column(db.String(255), nullable=True)
    scraped_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )
    is_active = db.Column(db.Boolean, default=True)

    applications = db.relationship("Application", backref="job", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "platform": self.platform,
            "source_url": self.source_url,
            "recruiter_email": self.recruiter_email,
            "scraped_at": self.scraped_at.isoformat() if self.scraped_at else None,
            "is_active": self.is_active,
            "applications_count": len(self.applications),
        }


# ── APPLICATIONS ──────────────────────────────────────────────────────────────
class Application(db.Model):
    __tablename__ = "applications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"), nullable=True)
    platform = db.Column(
        db.String(50), nullable=False
    )  # email | linkedin | naukri | indeed
    status = db.Column(
        db.String(50), default="sent"
    )  # sent | failed | pending | applied
    failure_reason = db.Column(
        db.String(500), nullable=True
    )  # email_not_found | apply_failed | captcha | blocked
    applied_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "job_id": self.job_id,
            "platform": self.platform,
            "status": self.status,
            "failure_reason": self.failure_reason,
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }


# ── PAYMENTS ──────────────────────────────────────────────────────────────────
class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    razorpay_payment_id = db.Column(db.String(255), nullable=True)
    razorpay_order_id = db.Column(db.String(255), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default="INR")
    status = db.Column(
        db.String(50), default="pending"
    )  # success | failed | pending | refunded
    subscription_plan = db.Column(db.String(100), nullable=True)
    is_suspicious = db.Column(db.Boolean, default=False)
    created_at = db.Column(
        db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "razorpay_payment_id": self.razorpay_payment_id,
            "razorpay_order_id": self.razorpay_order_id,
            "amount": self.amount,
            "currency": self.currency,
            "status": self.status,
            "subscription_plan": self.subscription_plan,
            "is_suspicious": self.is_suspicious,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── SYSTEM LOGS ──────────────────────────────────────────────────────────────
class SystemLog(db.Model):
    __tablename__ = "system_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    level = db.Column(
        db.String(20), nullable=False, default="info"
    )  # info | warning | error | critical
    source = db.Column(
        db.String(100), nullable=False
    )  # scraper | api | queue | automation
    message = db.Column(db.Text, nullable=False)
    details = db.Column(db.Text, nullable=True)  # JSON extra data
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "level": self.level,
            "source": self.source,
            "message": self.message,
            "details": self.details,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── AI LOGS ───────────────────────────────────────────────────────────────────
class AILog(db.Model):
    __tablename__ = "ai_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action_type = db.Column(
        db.String(100), nullable=False
    )  # keyword_generation | resume_modification | job_matching
    input_data = db.Column(db.Text, nullable=True)  # JSON
    output_data = db.Column(db.Text, nullable=True)  # JSON
    model_used = db.Column(db.String(100), nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "action_type": self.action_type,
            "input_data": self.input_data,
            "output_data": self.output_data,
            "model_used": self.model_used,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


# ── ADMIN SETTINGS ───────────────────────────────────────────────────────────
class AdminSetting(db.Model):
    __tablename__ = "admin_settings"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text, nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "key": self.key,
            "value": self.value,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
