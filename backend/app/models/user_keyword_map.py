"""
UserKeywordMap — many-to-many link between users and keyword sets.

When a user's resume produces the same keyword hash as an existing set,
only a new mapping row is created (no duplicate Apify call).
"""

from datetime import datetime, timezone

from sqlalchemy import ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class UserKeywordMap(Base):
    __tablename__ = "user_keyword_map"
    __table_args__ = (
        UniqueConstraint("user_id", "keyword_set_id", name="uq_user_keyword"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    keyword_set_id: Mapped[int] = mapped_column(
        ForeignKey("keyword_sets.id", ondelete="CASCADE"), nullable=False, index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user: Mapped["User"] = relationship(back_populates="keyword_maps")  # noqa: F821
    keyword_set: Mapped["KeywordSet"] = relationship(back_populates="user_maps")  # noqa: F821
