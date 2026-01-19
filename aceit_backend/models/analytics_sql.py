from sqlalchemy import Column, String, Integer, Boolean, ARRAY, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from database_postgres import Base
import datetime
import uuid

class QuestionAttempt(Base):
    """Individual question attempt history for analytics"""
    __tablename__ = "question_attempts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    question_id = Column(String, ForeignKey("aptitude_questions.id"))
    user_answer = Column(Integer)
    is_correct = Column(Boolean)
    time_spent_seconds = Column(Integer)
    difficulty_at_attempt = Column(String)
    category = Column(String)  # Added for filtering
    topic = Column(String)  # Added for filtering
    context = Column(String)  # "practice", "mock_test"
    attempted_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserAnalytics(Base):
    """Aggregated user analytics and performance metrics"""
    __tablename__ = "user_analytics"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), unique=True)
    
    # Overall stats
    total_questions_attempted = Column(Integer, default=0)
    total_correct = Column(Integer, default=0)
    overall_accuracy = Column(Float, default=0.0)
    total_time_spent_seconds = Column(Integer, default=0)
    
    # Category performance (JSON)
    category_stats = Column(JSON, default={})
    
    # Strengths and weaknesses
    strong_topics = Column(ARRAY(String), default=[])
    weak_topics = Column(ARRAY(String), default=[])
    
    # Mock test stats
    mock_tests_taken = Column(Integer, default=0)
    average_mock_score = Column(Float, default=0.0)
    best_mock_score = Column(Integer, default=0)
    
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

