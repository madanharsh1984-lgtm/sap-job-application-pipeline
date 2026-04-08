from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class KeywordSet(Base):
    __tablename__ = 'keyword_sets'

    id = Column(Integer, primary_key=True, index=True)
    keyword_hash = Column(String(64), unique=True, nullable=False, index=True)
    normalized_keywords = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    jobs = relationship('Job', back_populates='keyword_set', cascade='all, delete-orphan')
    user_mappings = relationship('UserKeywordMap', back_populates='keyword_set', cascade='all, delete-orphan')
