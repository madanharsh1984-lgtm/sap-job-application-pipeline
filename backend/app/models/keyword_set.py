"""
KeywordSet model — deduplicated, hashed keyword groups.

Each unique set of normalized keywords gets exactly ONE row.
Multiple users can map to the same keyword_set, ensuring Apify is called
only once per unique keyword combination.
"""

from datetime import datetime, timezone

from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.core.database import Base


class KeywordSet(Base):
    __tablename__ = "keyword_sets"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    keyword_hash: Mapped[str] = mapped_column(
        String(64), unique=True, nullable=False, index=True,
        comment="SHA-256 of sorted, normalized keywords"
    )
    normalized_keywords: Mapped[str] = mapped_column(
        Text, nullable=False,
        comment="JSON array of normalized keywords"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    # Relationships
    user_maps: Mapped[list["UserKeywordMap"]] = relationship(back_populates="keyword_set", lazy="selectin")  # noqa: F821
    jobs: Mapped[list["Job"]] = relationship(back_populates="keyword_set", lazy="selectin")  # noqa: F821
