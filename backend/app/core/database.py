import time

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.settings import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def wait_for_database() -> None:
    attempts = max(settings.DB_STARTUP_MAX_ATTEMPTS, 1)
    delay = max(settings.DB_STARTUP_RETRY_SECONDS, 0.1)
    last_error: Exception | None = None
    for _ in range(attempts):
        try:
            with engine.connect() as connection:
                connection.execute(text('SELECT 1'))
            return
        except Exception as exc:  # pragma: no cover - startup retry path
            last_error = exc
            time.sleep(delay)
    if last_error is not None:
        raise last_error


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
