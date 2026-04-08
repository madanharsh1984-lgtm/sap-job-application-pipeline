from sqlalchemy import Column, Integer, Text

from app.core.database import Base


class Job(Base):
    __tablename__ = 'jobs'

    id = Column(Integer, primary_key=True, index=True)
    keyword_group = Column(Text, nullable=False)
    job_data = Column(Text, nullable=False)
