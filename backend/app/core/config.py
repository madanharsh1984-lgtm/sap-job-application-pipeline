"""
Application configuration via environment variables.
"""

from pydantic import model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """All configuration loaded from environment / .env file."""

    # ── Application ──────────────────────────────────────────────────────
    APP_NAME: str = "JobAccelerator AI"
    DEBUG: bool = False

    # ── Database ─────────────────────────────────────────────────────────
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/jobaccelerator"
    DATABASE_URL_SYNC: str = "postgresql+psycopg2://postgres:postgres@localhost:5432/jobaccelerator"

    # ── Redis ────────────────────────────────────────────────────────────
    REDIS_URL: str = "redis://localhost:6379/0"

    # ── Celery ───────────────────────────────────────────────────────────
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # ── JWT Auth ─────────────────────────────────────────────────────────
    SECRET_KEY: str = ""  # REQUIRED — validated at startup
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ── Apify ────────────────────────────────────────────────────────────
    APIFY_TOKEN: str = ""
    APIFY_ACTOR_ID: str = "harvestapi~linkedin-post-search"
    APIFY_BASE_URL: str = "https://api.apify.com/v2"
    APIFY_MAX_POSTS: int = 50
    APIFY_POLL_INTERVAL: int = 10
    APIFY_MAX_POLL_WAIT: int = 300

    # ── CORS ─────────────────────────────────────────────────────────────
    CORS_ORIGINS: str = "http://localhost:3000"

    # ── Keyword cache TTL (seconds) ──────────────────────────────────────
    KEYWORD_CACHE_TTL: int = 86400  # 24 hours

    @model_validator(mode="after")
    def validate_secret_key(self) -> "Settings":
        """Fail fast if SECRET_KEY is empty — prevents insecure JWT signing."""
        if not self.SECRET_KEY:
            raise ValueError(
                "SECRET_KEY is required. Set it via environment variable or .env file."
            )
        return self

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
