# =============================================================================
# routes.py — Admin API Routes & Page Routes (ADMIN_PORTAL_v1)
# =============================================================================
# All admin API routes require JWT + ADMIN role.
# API prefix: /admin/*
# =============================================================================

import json
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import Blueprint, jsonify, render_template, request
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
)
from werkzeug.security import check_password_hash, generate_password_hash

from admin_portal.models import (
    AILog,
    AdminSetting,
    Application,
    Job,
    Payment,
    SystemLog,
    User,
    UserIntegration,
    db,
)

# ── Blueprints ────────────────────────────────────────────────────────────────
admin_bp = Blueprint("admin_api", __name__)
pages_bp = Blueprint("pages", __name__)


# ── Role Decorator ────────────────────────────────────────────────────────────
def admin_required(fn):
    """Decorator that requires JWT + ADMIN role."""

    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user = db.session.get(User, int(identity))
        if not user or user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper


# =============================================================================
# AUTH ENDPOINTS
# =============================================================================


@admin_bp.route("/auth/login", methods=["POST"])
def admin_login():
    """Authenticate admin and return JWT token."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid credentials"}), 401

    if user.role != "admin":
        return jsonify({"error": "Admin access required"}), 403

    if not user.is_active:
        return jsonify({"error": "Account is deactivated"}), 403

    user.last_login_at = datetime.now(timezone.utc)
    db.session.commit()

    token = create_access_token(identity=str(user.id))
    return jsonify(
        {
            "token": token,
            "user": {"id": user.id, "email": user.email, "name": user.name},
        }
    )


@admin_bp.route("/auth/setup", methods=["POST"])
def admin_setup():
    """One-time setup: create the first admin user if none exists."""
    existing_admin = User.query.filter_by(role="admin").first()
    if existing_admin:
        return jsonify({"error": "Admin already exists. Use login."}), 409

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "").strip()

    if not email or not password or not name:
        return jsonify({"error": "Name, email, and password required"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    admin = User(
        email=email,
        password_hash=generate_password_hash(password),
        name=name,
        role="admin",
        is_active=True,
    )
    db.session.add(admin)
    db.session.commit()

    _log_system("info", "auth", f"Admin account created: {email}")

    token = create_access_token(identity=str(admin.id))
    return (
        jsonify(
            {
                "message": "Admin created successfully",
                "token": token,
                "user": {
                    "id": admin.id,
                    "email": admin.email,
                    "name": admin.name,
                },
            }
        ),
        201,
    )


# =============================================================================
# DASHBOARD METRICS — GET /admin/dashboard-metrics
# =============================================================================


@admin_bp.route("/dashboard-metrics", methods=["GET"])
@admin_required
def dashboard_metrics():
    """Return real-time dashboard metrics."""
    now = datetime.now(timezone.utc)
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    week_start = today_start - timedelta(days=7)
    month_start = today_start.replace(day=1)

    total_users = User.query.count()
    active_daily = User.query.filter(User.last_login_at >= today_start).count()
    active_weekly = User.query.filter(User.last_login_at >= week_start).count()
    total_jobs = Job.query.count()
    total_applications = Application.query.count()
    failed_applications = Application.query.filter_by(status="failed").count()

    conversion_rate = 0
    if total_jobs > 0:
        conversion_rate = round((total_applications / total_jobs) * 100, 2)

    revenue_daily = (
        db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0))
        .filter(Payment.status == "success", Payment.created_at >= today_start)
        .scalar()
    )
    revenue_monthly = (
        db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0))
        .filter(Payment.status == "success", Payment.created_at >= month_start)
        .scalar()
    )

    return jsonify(
        {
            "total_users": total_users,
            "active_users_daily": active_daily,
            "active_users_weekly": active_weekly,
            "total_jobs_discovered": total_jobs,
            "total_applications_sent": total_applications,
            "failed_applications": failed_applications,
            "conversion_rate": conversion_rate,
            "revenue_daily": float(revenue_daily),
            "revenue_monthly": float(revenue_monthly),
        }
    )


# =============================================================================
# USER MANAGEMENT — GET /admin/users, GET /admin/user/<id>
# =============================================================================


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    """List all users with optional search/filter."""
    search = request.args.get("search", "").strip()
    status_filter = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = User.query
    if search:
        query = query.filter(
            db.or_(
                User.email.ilike(f"%{search}%"),
                User.name.ilike(f"%{search}%"),
            )
        )
    if status_filter == "active":
        query = query.filter_by(is_active=True)
    elif status_filter == "inactive":
        query = query.filter_by(is_active=False)

    pagination = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "users": [u.to_dict() for u in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


@admin_bp.route("/user/<int:user_id>", methods=["GET"])
@admin_required
def get_user(user_id):
    """Get detailed user info including integrations, resumes, stats."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = user.to_dict()
    user_data["integrations"] = [i.to_dict() for i in user.integrations]
    user_data["resumes"] = [r.to_dict() for r in user.resumes]

    # Per-user stats
    user_data["total_jobs_discovered"] = (
        Application.query.filter_by(user_id=user_id)
        .with_entities(Application.job_id)
        .distinct()
        .count()
    )
    user_data["total_applications_sent"] = Application.query.filter_by(
        user_id=user_id
    ).count()

    # Keywords from resumes
    keywords = []
    for resume in user.resumes:
        if resume.keywords:
            try:
                keywords.extend(json.loads(resume.keywords))
            except (json.JSONDecodeError, TypeError):
                pass
    user_data["keywords"] = list(set(keywords))

    return jsonify(user_data)


@admin_bp.route("/user/disable", methods=["POST"])
@admin_required
def disable_user():
    """Activate or deactivate a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    user_id = data.get("user_id")
    action = data.get("action", "deactivate")  # activate | deactivate

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if action == "activate":
        user.is_active = True
    elif action == "deactivate":
        user.is_active = False
    else:
        return jsonify({"error": "Invalid action. Use activate or deactivate."}), 400

    db.session.commit()
    _log_system(
        "info", "admin", f"User {user.email} {action}d by admin"
    )

    return jsonify(
        {"message": f"User {action}d successfully", "user": user.to_dict()}
    )


@admin_bp.route("/user/reset-integrations", methods=["POST"])
@admin_required
def reset_user_integrations():
    """Reset all integrations for a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    user_id = data.get("user_id")
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    for integration in user.integrations:
        integration.status = "inactive"
        integration.credentials_set = False
    db.session.commit()

    _log_system(
        "info", "admin", f"Integrations reset for user {user.email}"
    )
    return jsonify({"message": "Integrations reset successfully"})


@admin_bp.route("/user/<int:user_id>/logs", methods=["GET"])
@admin_required
def get_user_logs(user_id):
    """Get activity logs for a specific user."""
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    # Get AI logs for user
    ai_logs = (
        AILog.query.filter_by(user_id=user_id)
        .order_by(AILog.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    # Get applications for user
    applications = (
        Application.query.filter_by(user_id=user_id)
        .order_by(Application.applied_at.desc())
        .limit(per_page)
        .all()
    )

    return jsonify(
        {
            "ai_logs": [log.to_dict() for log in ai_logs.items],
            "applications": [app.to_dict() for app in applications],
            "total_ai_logs": ai_logs.total,
        }
    )


# =============================================================================
# PAYMENT MANAGEMENT — GET /admin/payments
# =============================================================================


@admin_bp.route("/payments", methods=["GET"])
@admin_required
def list_payments():
    """List all payment transactions."""
    status_filter = request.args.get("status", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Payment.query
    if status_filter:
        query = query.filter_by(status=status_filter)

    pagination = query.order_by(Payment.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "payments": [p.to_dict() for p in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


@admin_bp.route("/payment/refund", methods=["POST"])
@admin_required
def refund_payment():
    """Manually trigger a refund for a payment."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    payment_id = data.get("payment_id")
    payment = db.session.get(Payment, payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    if payment.status == "refunded":
        return jsonify({"error": "Payment already refunded"}), 400

    payment.status = "refunded"
    db.session.commit()

    _log_system(
        "info",
        "admin",
        f"Payment {payment_id} refunded (amount: {payment.amount} {payment.currency})",
    )
    return jsonify(
        {"message": "Payment refunded successfully", "payment": payment.to_dict()}
    )


@admin_bp.route("/payment/flag", methods=["POST"])
@admin_required
def flag_payment():
    """Flag a payment as suspicious."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    payment_id = data.get("payment_id")
    payment = db.session.get(Payment, payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment.is_suspicious = not payment.is_suspicious
    db.session.commit()

    status = "flagged" if payment.is_suspicious else "unflagged"
    _log_system("warning", "admin", f"Payment {payment_id} {status} as suspicious")
    return jsonify(
        {"message": f"Payment {status}", "payment": payment.to_dict()}
    )


# =============================================================================
# JOB & APPLICATION TRACKING — GET /admin/jobs, GET /admin/applications
# =============================================================================


@admin_bp.route("/jobs", methods=["GET"])
@admin_required
def list_jobs():
    """List all scraped jobs."""
    platform = request.args.get("platform", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Job.query
    if platform:
        query = query.filter_by(platform=platform)

    pagination = query.order_by(Job.scraped_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Platform breakdown
    platform_counts = (
        db.session.query(Job.platform, db.func.count(Job.id))
        .group_by(Job.platform)
        .all()
    )

    return jsonify(
        {
            "jobs": [j.to_dict() for j in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "platform_breakdown": {p: c for p, c in platform_counts},
        }
    )


@admin_bp.route("/applications", methods=["GET"])
@admin_required
def list_applications():
    """List all applications with failure tracking."""
    status_filter = request.args.get("status", "")
    platform = request.args.get("platform", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)

    query = Application.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    if platform:
        query = query.filter_by(platform=platform)

    pagination = query.order_by(Application.applied_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    # Failure breakdown
    failure_counts = (
        db.session.query(
            Application.failure_reason, db.func.count(Application.id)
        )
        .filter(Application.status == "failed")
        .group_by(Application.failure_reason)
        .all()
    )

    # Platform breakdown
    platform_counts = (
        db.session.query(Application.platform, db.func.count(Application.id))
        .group_by(Application.platform)
        .all()
    )

    return jsonify(
        {
            "applications": [a.to_dict() for a in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
            "failure_breakdown": {
                (r or "unknown"): c for r, c in failure_counts
            },
            "platform_breakdown": {p: c for p, c in platform_counts},
        }
    )


# =============================================================================
# SYSTEM LOGS — GET /admin/system-logs
# =============================================================================


@admin_bp.route("/system-logs", methods=["GET"])
@admin_required
def list_system_logs():
    """List system logs with filtering."""
    level = request.args.get("level", "")
    source = request.args.get("source", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = SystemLog.query
    if level:
        query = query.filter_by(level=level)
    if source:
        query = query.filter_by(source=source)

    pagination = query.order_by(SystemLog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "logs": [log.to_dict() for log in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


# =============================================================================
# AI DECISION TRACKING — GET /admin/ai-logs
# =============================================================================


@admin_bp.route("/ai-logs", methods=["GET"])
@admin_required
def list_ai_logs():
    """List AI decision logs for debugging and quality improvement."""
    action_type = request.args.get("action_type", "")
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    query = AILog.query
    if action_type:
        query = query.filter_by(action_type=action_type)

    pagination = query.order_by(AILog.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify(
        {
            "ai_logs": [log.to_dict() for log in pagination.items],
            "total": pagination.total,
            "page": pagination.page,
            "pages": pagination.pages,
        }
    )


# =============================================================================
# CONTROL PANEL — POST /admin/system/pause, settings
# =============================================================================


@admin_bp.route("/system/pause", methods=["POST"])
@admin_required
def pause_system():
    """Pause or resume all automation globally or per-user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    scope = data.get("scope", "global")  # global | user
    paused = data.get("paused", True)

    if scope == "global":
        setting = AdminSetting.query.filter_by(
            key="global_automation_paused"
        ).first()
        if setting:
            setting.value = str(paused).lower()
        else:
            db.session.add(
                AdminSetting(key="global_automation_paused", value=str(paused).lower())
            )
        db.session.commit()
        _log_system(
            "warning",
            "admin",
            f"Global automation {'paused' if paused else 'resumed'} by admin",
        )
        return jsonify(
            {
                "message": f"Global automation {'paused' if paused else 'resumed'}",
                "paused": paused,
            }
        )
    elif scope == "user":
        user_id = data.get("user_id")
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        user.is_paused = paused
        db.session.commit()
        _log_system(
            "info",
            "admin",
            f"User {user.email} automation {'paused' if paused else 'resumed'}",
        )
        return jsonify(
            {
                "message": f"User automation {'paused' if paused else 'resumed'}",
                "user": user.to_dict(),
            }
        )
    else:
        return jsonify({"error": "Invalid scope. Use global or user."}), 400


@admin_bp.route("/settings", methods=["GET"])
@admin_required
def get_settings():
    """Get all admin settings."""
    settings = AdminSetting.query.all()
    return jsonify({"settings": {s.key: s.value for s in settings}})


@admin_bp.route("/settings", methods=["PUT"])
@admin_required
def update_settings():
    """Update admin settings."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    updated = []
    for key, value in data.items():
        setting = AdminSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = str(value)
            updated.append(key)
        else:
            db.session.add(AdminSetting(key=key, value=str(value)))
            updated.append(key)

    db.session.commit()
    _log_system("info", "admin", f"Settings updated: {', '.join(updated)}")
    return jsonify({"message": "Settings updated", "updated_keys": updated})


@admin_bp.route("/user/set-limit", methods=["POST"])
@admin_required
def set_user_limit():
    """Set daily application limit for a user."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    user_id = data.get("user_id")
    limit = data.get("limit", 50)

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user.daily_application_limit = limit
    db.session.commit()

    _log_system(
        "info",
        "admin",
        f"Daily application limit set to {limit} for user {user.email}",
    )
    return jsonify(
        {"message": f"Limit set to {limit}", "user": user.to_dict()}
    )


# =============================================================================
# PAGE ROUTES (HTML Templates)
# =============================================================================


@pages_bp.route("/")
def login_page():
    """Login page."""
    return render_template("login.html")


@pages_bp.route("/dashboard")
def dashboard_page():
    """Dashboard page."""
    return render_template("dashboard.html")


@pages_bp.route("/users")
def users_page():
    """Users management page."""
    return render_template("users.html")


@pages_bp.route("/payments")
def payments_page():
    """Payments page."""
    return render_template("payments.html")


@pages_bp.route("/jobs")
def jobs_page():
    """Jobs & Applications page."""
    return render_template("jobs.html")


@pages_bp.route("/system-logs")
def system_logs_page():
    """System logs page."""
    return render_template("system_logs.html")


@pages_bp.route("/settings")
def settings_page():
    """Settings / Controls page."""
    return render_template("settings.html")


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================


def _log_system(level, source, message, details=None):
    """Create a system log entry."""
    log = SystemLog(level=level, source=source, message=message, details=details)
    db.session.add(log)
    db.session.commit()
