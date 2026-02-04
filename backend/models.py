from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean
from datetime import datetime
from db import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(50), nullable=False)  
    title = Column(String(50), nullable=False)
    description = Column(Text, nullable=False)
    min_experience = Column(Integer, nullable=False)
    max_experience = Column(Integer, nullable=False)
    location = Column(String(50), nullable=False)
    mode = Column(String(50), nullable=False) 
    compensation = Column(Integer, nullable=False)
    compensation_type = Column(String(50), nullable=False)  
    is_open = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
