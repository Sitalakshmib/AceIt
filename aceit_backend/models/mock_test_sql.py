from sqlalchemy import Column, String, Integer, Boolean, ARRAY, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from database_postgres import Base
import datetime
import uuid

class MockTest(Base):
    """Represents a generated mock test"""
    __tablename__ = "mock_tests"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    test_type = Column(String)  # "full_length", "section_wise", "topic_wise"
    category = Column(String, nullable=True)  # For section-wise tests
    topic = Column(String, nullable=True)  # For topic-wise tests
    total_questions = Column(Integer)
    duration_minutes = Column(Integer)
    difficulty_distribution = Column(JSON)  # {"easy": 40, "medium": 40, "hard": 20}
    question_ids = Column(ARRAY(String))  # Ordered list of question IDs
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_active = Column(Boolean, default=True)

class MockTestAttempt(Base):
    """Tracks user attempts at mock tests"""
    __tablename__ = "mock_test_attempts"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    mock_test_id = Column(String, ForeignKey("mock_tests.id"))
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    time_taken_seconds = Column(Integer, nullable=True)
    score = Column(Integer, default=0)
    total_questions = Column(Integer)
    accuracy_percentage = Column(Float, default=0.0)
    status = Column(String, default="in_progress")  # "in_progress", "completed", "abandoned"
    
    user = relationship("User")
    mock_test = relationship("MockTest")

class MockTestResponse(Base):
    """Individual question responses in mock tests"""
    __tablename__ = "mock_test_responses"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    attempt_id = Column(String, ForeignKey("mock_test_attempts.id"))
    question_id = Column(String, ForeignKey("aptitude_questions.id"))
    user_answer = Column(Integer, nullable=True)
    is_correct = Column(Boolean, nullable=True)
    time_spent_seconds = Column(Integer, default=0)
    answered_at = Column(DateTime, nullable=True)
    
    attempt = relationship("MockTestAttempt")
    question = relationship("AptitudeQuestion")
