from sqlalchemy import Column, String, Integer, Float, DateTime, Text, Index
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from datetime import datetime
import uuid
from database_postgres import Base


class GDSession(Base):
    """Tracks Group Discussion practice sessions and AI feedback"""
    __tablename__ = "gd_sessions"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    topic = Column(Text, nullable=False)
    user_input = Column(Text, nullable=True)           # user's GD response text
    time_taken_seconds = Column(Integer, default=0)

    # Scores (0-10 scale)
    clarity_score = Column(Float, nullable=True)
    coherence_score = Column(Float, nullable=True)
    relevance_score = Column(Float, nullable=True)
    overall_score = Column(Float, nullable=True)       # average of the 3 scores

    # AI Feedback
    feedback = Column(Text, nullable=True)
    strengths = Column(ARRAY(String), default=list)
    improvements = Column(ARRAY(String), default=list)
    topic_points = Column(JSONB, default=list)         # list of study point strings

    practiced_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_gd_user_id', 'user_id'),
    )


class ResumeAnalysis(Base):
    """Tracks resume analysis sessions"""
    __tablename__ = "resume_analyses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, nullable=False, index=True)
    job_role = Column(String, nullable=True)

    # Scores
    overall_score = Column(Float, nullable=True)
    ats_score = Column(Float, nullable=True)
    skills_match_score = Column(Float, nullable=True)

    # Analysis results (stored as JSON for flexibility)
    matched_skills = Column(ARRAY(String), default=list)
    missing_skills = Column(ARRAY(String), default=list)
    suggestions = Column(JSONB, default=list)          # list of feedback strings
    ats_analysis = Column(JSONB, nullable=True)        # full ats analysis blob
    ai_analysis = Column(JSONB, nullable=True)         # Gemini AI feedback blob

    analyzed_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        Index('idx_resume_user_id', 'user_id'),
    )
