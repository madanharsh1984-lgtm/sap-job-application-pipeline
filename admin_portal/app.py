# =============================================================================
# app.py — Flask Application Factory for Admin Portal
# =============================================================================

import os
import secrets

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from admin_portal.models import AdminSetting, db


def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(
        __name__,
        template_folder=os.path.join(
            os.path.dirname(__file__), "templates"
        ),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )

    # ── Configuration ─────────────────────────────────────────────────────
    base_dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "admin_portal.db")

    app.config.update(
        {
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JWT_SECRET_KEY": os.environ.get(
                "ADMIN_JWT_SECRET", secrets.token_hex(32)
            ),
            "JWT_ACCESS_TOKEN_EXPIRES": 3600,  # 1 hour
        }
    )

    if test_config:
        app.config.update(test_config)

    # ── Extensions ────────────────────────────────────────────────────────
    CORS(app)
    db.init_app(app)
    JWTManager(app)

    # ── Register Blueprints ───────────────────────────────────────────────
    from admin_portal.routes import admin_bp, pages_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(pages_bp)

    # ── Create Tables & Seed Defaults ─────────────────────────────────────
    with app.app_context():
        db.create_all()
        _seed_defaults()

    return app


def _seed_defaults():
    """Seed default admin settings if they don't exist."""
    defaults = {
        "global_automation_paused": "false",
        "default_daily_application_limit": "50",
        "scraping_frequency_minutes": "60",
    }
    for key, value in defaults.items():
        existing = AdminSetting.query.filter_by(key=key).first()
        if not existing:
            db.session.add(AdminSetting(key=key, value=value))
    db.session.commit()
