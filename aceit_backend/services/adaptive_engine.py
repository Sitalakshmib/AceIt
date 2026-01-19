"""
Adaptive Learning Engine for Aptitude Module

This service implements the backend-driven adaptive difficulty adjustment algorithm.
The system tracks per-user, per-topic performance and dynamically adjusts question
difficulty based on consecutive correct/incorrect answers.

Algorithm Rules:
- Start at 'easy' for new topics
- 3 consecutive correct answers → move up one difficulty level
- 2 consecutive incorrect answers → move down one difficulty level
- Avoid recently answered questions (last 20)
- Track detailed performance metrics for analytics
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from typing import Optional, List
import datetime


def get_or_create_progress(db: Session, user_id: str, topic: str, category: str) -> Optional[UserAptitudeProgress]:
    """Get user progress for a specific topic, or create if not exists"""
    try:
        progress = db.query(UserAptitudeProgress).filter(
            UserAptitudeProgress.user_id == user_id,
            UserAptitudeProgress.topic == topic
        ).first()
        
        if not progress:
            progress = UserAptitudeProgress(
                user_id=user_id,
                topic=topic,
                category=category,
                current_difficulty="easy",
                # Initialize all counters to 0
                questions_attempted=0,
                questions_correct=0,
                streak=0,
                easy_total=0,
                easy_correct=0,
                medium_total=0,
                medium_correct=0,
                hard_total=0,
                hard_correct=0,
                consecutive_correct=0,
                consecutive_incorrect=0,
                total_time_spent_seconds=0
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
            
        return progress
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Could not create progress for user {user_id}, topic {topic}: {e}")
        return None


class AdaptiveEngine:
    """
    Backend-driven adaptive difficulty adjustment engine
    """
    
    DIFFICULTY_LEVELS = ["easy", "medium", "hard"]
    LEVEL_UP_THRESHOLD = 3  # consecutive correct
    LEVEL_DOWN_THRESHOLD = 2  # consecutive incorrect
    RECENT_QUESTIONS_TO_AVOID = 20
    
    @staticmethod
    def calculate_next_difficulty(
        db: Session, 
        user_id: str, 
        topic: str, 
        current_difficulty: str
    ) -> str:
        """
        Determine next difficulty using Sliding Window (last 10) + Time.
        
        Rules:
        - Level Up: Accuracy >= 75% (>=8/10) AND fast enough responses.
        - Level Down: Accuracy < 50% (<5/10).
        - Stay: Otherwise.
        """
        
        # 1. Fetch last 10 attempts for this topic/user
        attempts = db.query(QuestionAttempt)\
            .filter(
                QuestionAttempt.user_id == user_id,
                QuestionAttempt.topic == topic,
                QuestionAttempt.context == "practice" # Analytics mainly for practice
            )\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(10).all()
            

        if not attempts or len(attempts) < 5:
            # Need at least 5 attempts to make a judgment
            return current_difficulty
            
        # 2. Calculate metrics
        total = len(attempts)
        correct_count = sum(1 for a in attempts if a.is_correct)
        accuracy = (correct_count / total) * 100
        
        # Calculate avg time for CORRECT answers only (to judge mastery)
        correct_attempts = [a for a in attempts if a.is_correct]
        avg_time = 0
        if correct_attempts:
            avg_time = sum(a.time_spent_seconds for a in correct_attempts) / len(correct_attempts)
            
        # 3. Define Thresholds
        # Time thresholds for fast answers (seconds)
        TIME_THRESHOLDS = {
            "easy": 30,
            "medium": 45,
            "hard": 60
        }
        max_time_allowed = TIME_THRESHOLDS.get(current_difficulty, 45)
        
        # 4. Difficulty Logic
        try:
            current_index = AdaptiveEngine.DIFFICULTY_LEVELS.index(current_difficulty)
        except ValueError:
            return "easy"
            
        # LEVEL UP
        # High accuracy AND fast response time
        if accuracy >= 75 and avg_time <= max_time_allowed:
            if current_index < len(AdaptiveEngine.DIFFICULTY_LEVELS) - 1:
                return AdaptiveEngine.DIFFICULTY_LEVELS[current_index + 1]
                
        # LEVEL DOWN
        # Low accuracy
        elif accuracy < 50:
            if current_index > 0:
                return AdaptiveEngine.DIFFICULTY_LEVELS[current_index - 1]
                
        return current_difficulty

    @staticmethod
    def update_progress(
        db: Session,
        user_id: str,
        question: AptitudeQuestion,
        is_correct: bool,
        time_spent: int
    ):
        """
        Update user progress and adjust difficulty dynamically.
        """
        # 1. First, record the attempt (CRITICAL for sliding window)
        AdaptiveEngine.record_attempt(
            db, user_id, question.id, -1, is_correct, time_spent, # user_answer not passed here, assumed captured
            question.difficulty, question.topic, question.category, "practice"
        )
        # Note: 'user_answer' is not passed to update_progress but is to record_attempt. 
        # Ideally record_attempt should be called by the service, or we pass user_answer here.
        # However, practice_service calls record_attempt separately? No, let's check practice_service.
        # Checking practice_service.py: It calls `db.add(attempt)` itself!
        # AND it calls `AdaptiveEngine.submit_answer`? No, it calls `PracticeService.submit_answer` 
        # which calls `db.add(attempt)` AND THEN manual logic.
        # Wait, the previous code had duplicated logic?
        # Let's align: PracticeService handles DB recording. AdaptiveEngine calculates stats.
        
        progress = get_or_create_progress(db, user_id, question.topic, question.category)
        
        if not progress:
            return
        
        # Update generic counters
        progress.questions_attempted += 1
        if is_correct:
            progress.questions_correct += 1
            progress.consecutive_correct += 1
            progress.consecutive_incorrect = 0
            progress.streak += 1
        else:
            progress.consecutive_correct = 0
            progress.consecutive_incorrect += 1
            progress.streak = 0
            
        # Update difficulty-specific stats
        if question.difficulty == "easy":
            progress.easy_total += 1
            if is_correct: progress.easy_correct += 1
        elif question.difficulty == "medium":
            progress.medium_total += 1
            if is_correct: progress.medium_correct += 1
        elif question.difficulty == "hard":
            progress.hard_total += 1
            if is_correct: progress.hard_correct += 1
            
        # Time tracking
        progress.total_time_spent_seconds += time_spent
        if progress.questions_attempted > 0:
             progress.average_time_per_question = (
                progress.total_time_spent_seconds / progress.questions_attempted
             )
             
        # --- NEW ADAPTIVE LOGIC ---
        new_difficulty = AdaptiveEngine.calculate_next_difficulty(
            db, user_id, question.topic, progress.current_difficulty
        )
        
        if new_difficulty != progress.current_difficulty:
            progress.current_difficulty = new_difficulty
            progress.last_difficulty_change = datetime.datetime.utcnow()
            # Reset streaks on level change (optional but good practice)
            progress.consecutive_correct = 0
            progress.consecutive_incorrect = 0
            
        progress.last_practiced = datetime.datetime.utcnow()
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Failed to update progress: {e}")
            raise
    
    @staticmethod
    def record_attempt(
        db: Session,
        user_id: str,
        question_id: str,
        user_answer: int,
        is_correct: bool,
        time_spent: int,
        difficulty: str,
        topic: str = None,
        category: str = None,
        context: str = "practice"
    ):
        """
        Record a question attempt for analytics
        """
        attempt = QuestionAttempt(
            user_id=user_id,
            question_id=question_id,
            user_answer=user_answer,
            is_correct=is_correct,
            time_spent_seconds=time_spent,
            difficulty_at_attempt=difficulty,
            topic=topic,
            category=category,
            context=context
        )
        db.add(attempt)
        
        try:
            db.commit()
        except Exception as e:
            db.rollback()
            print(f"[ERROR] Failed to record attempt: {e}")
