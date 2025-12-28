from sqlalchemy import Column, String, Integer, Boolean, ARRAY, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from database_postgres import Base
import datetime
import uuid

class AptitudeQuestion(Base):
    __tablename__ = "aptitude_questions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    question = Column(String)
    options = Column(ARRAY(String))
    correct_answer = Column(Integer)  # Index of the correct option
    answer_explanation = Column(String)
    topic = Column(String)  # e.g., "percentage", "blood_relations"
    category = Column(String)  # "Quantitative", "Logical", "Verbal"
    difficulty = Column(String)  # "easy", "medium", "hard"
    source = Column(String, default="generated")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class UserAptitudeProgress(Base):
    __tablename__ = "user_aptitude_progress"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"))
    topic = Column(String)
    category = Column(String)
    
    # Performance metrics
    questions_attempted = Column(Integer, default=0)
    questions_correct = Column(Integer, default=0)
    current_difficulty = Column(String, default="easy")
    streak = Column(Integer, default=0)  # Correct answer streak
    
    # Level tracking
    easy_correct = Column(Integer, default=0)
    easy_total = Column(Integer, default=0)
    medium_correct = Column(Integer, default=0)
    medium_total = Column(Integer, default=0)
    hard_correct = Column(Integer, default=0)
    hard_total = Column(Integer, default=0)
    
    last_practiced = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User")
