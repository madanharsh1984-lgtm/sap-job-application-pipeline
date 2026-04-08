"""
Job model — scraped job results linked to a keyword set.

Jobs are stored centrally. All users whose keyword_set matches
get access to the same jobs — no duplicate scraping.
"""

from datetime import datetime, timezone

from sqlalchemy import ForeignKey, String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword_set_id: Mapped[int] = mapped_column(
        ForeignKey("keyword_sets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    external_id: Mapped[str | None] = mapped_column(
        String(255), nullable=True, index=True,
        comment="Apify dataset item ID or post URL for dedup"
    )
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    location: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    post_url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    job_data: Mapped[str] = mapped_column(
        Text, nullable=False,
        comment="Full JSON blob of scraped data"
    )
    source: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    keyword_set: Mapped["KeywordSet"] = relationship(back_populates="jobs")  # noqa: F821
