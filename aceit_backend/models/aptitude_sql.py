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
    image_url = Column(String, nullable=True)  # For Data Interpretation charts/graphs
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    # Additional metadata for analytics
    tags = Column(ARRAY(String), default=list)
    times_attempted = Column(Integer, default=0)
    times_correct = Column(Integer, default=0)
    average_time_seconds = Column(Float, default=0.0)
    last_used = Column(DateTime, nullable=True)

    # ===== ELITE METADATA =====
    # Conceptual depth
    primary_concepts = Column(ARRAY(String), default=list)  # ["concept1", "concept2"]
    trap_explanation = Column(String, nullable=True)  # Why wrong options are tempting
    optimal_solution_strategy = Column(String, nullable=True)  # Fastest reasoning path
    common_mistake = Column(String, nullable=True)  # What average students do wrong
    time_to_solve_sec = Column(Integer, default=120)  # Expected solve time
    
    # Multi-dimensional difficulty
    concept_depth = Column(String, default="single")  # single, dual, multi, meta
    cognitive_load = Column(String, default="low")  # low, medium, high, very_high
    trap_density = Column(String, default="low")  # low, medium, high
    
    # Follow-up logic (stored as JSON string)
    follow_up_logic = Column(String, nullable=True)  # JSON: {if_correct, if_wrong}
    
    # Quality metrics
    discriminatory_index = Column(Float, default=0.0)  # How well it separates top performers
    elite_accuracy_rate = Column(Float, default=0.0)  # Accuracy among elite users (80%+ overall)

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
    
    # Adaptive state tracking
    consecutive_correct = Column(Integer, default=0)
    consecutive_incorrect = Column(Integer, default=0)
    last_difficulty_change = Column(DateTime, nullable=True)
    
    # Time tracking
    total_time_spent_seconds = Column(Integer, default=0)
    average_time_per_question = Column(Float, default=0.0)
    
    # Performance trends
    recent_accuracy = Column(Float, default=0.0)  # Last 10 questions
    overall_accuracy = Column(Float, default=0.0)
    
    # ===== ERROR PATTERN TRACKING =====
    conceptual_errors = Column(Integer, default=0)  # Wrong approach, formula misapplication
    careless_errors = Column(Integer, default=0)  # Calculation mistakes, sign errors
    overthinking_errors = Column(Integer, default=0)  # Correct approach but overcomplicated
    time_pressure_errors = Column(Integer, default=0)  # Rushed answers, incomplete reasoning
    
    # ===== MULTI-DIMENSIONAL STATE =====
    current_concept_depth = Column(String, default="single")  # single, dual, multi, meta
    current_cognitive_load = Column(String, default="low")  # low, medium, high, very_high
    current_trap_density = Column(String, default="low")  # low, medium, high
    
    # Performance classification
    user_tier = Column(String, default="developing")  # developing, competent, advanced, elite
    
    last_practiced = Column(DateTime, default=datetime.datetime.utcnow)

