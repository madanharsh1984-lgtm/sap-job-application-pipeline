from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserKeywordMap(Base):
    __tablename__ = 'user_keyword_map'

    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    keyword_set_id = Column(Integer, ForeignKey('keyword_sets.id', ondelete='CASCADE'), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='keyword_mappings')
    keyword_set = relationship('KeywordSet', back_populates='user_mappings')
