from sqlalchemy import Column, Integer, String, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database_postgres import Base


class InterviewSession(Base):
    """Tracks interview sessions for analytics and history"""
    __tablename__ = "interview_sessions"
    
    id = Column(String, primary_key=True)  # UUID
    user_id = Column(String, nullable=False, index=True)
    interview_type = Column(String, nullable=False)  # technical, hr, video-practice
    topic = Column(String, nullable=True)  # realtime, python, java, sql, dotnet
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    question_count = Column(Integer, default=0)
    status = Column(String, default="active")  # active, completed, abandoned


class InterviewHistory(Base):
    """Tracks questions asked to prevent repetition"""
    __tablename__ = "interview_history"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, nullable=False, index=True)
    interview_type = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    question_text = Column(Text, nullable=False)
    asked_at = Column(DateTime, default=datetime.utcnow)
    
    # Composite index for efficient lookups
    __table_args__ = (
        Index('idx_user_topic', 'user_id', 'interview_type', 'topic'),
    )
