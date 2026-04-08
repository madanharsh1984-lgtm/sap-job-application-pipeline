"""
User model — represents a registered platform user.
"""

from datetime import datetime, timezone

from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    resumes: Mapped[list["Resume"]] = relationship(back_populates="user", lazy="selectin")  # noqa: F821
    keyword_maps: Mapped[list["UserKeywordMap"]] = relationship(back_populates="user", lazy="selectin")  # noqa: F821
