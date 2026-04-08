"""
Resume model — stores uploaded resume data per user.
"""

from datetime import datetime, timezone

from sqlalchemy import ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class Resume(Base):
    __tablename__ = "resumes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    parsed_data: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON string of parsed fields
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="resumes")  # noqa: F821
