from sqlalchemy import Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    keyword_set_id = Column(Integer, ForeignKey('keyword_sets.id', ondelete='CASCADE'), nullable=False, index=True)
    job_data = Column(Text, nullable=False)

    keyword_set = relationship('KeywordSet', back_populates='jobs')
