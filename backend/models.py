from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from database import Base

class StudentRecord(Base):
    __tablename__ = "student_records"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    branch = Column(String)
    role = Column(String)
    match_percentage = Column(Float)
    burnout_score = Column(Integer)
    burnout_risk = Column(String)
    recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)