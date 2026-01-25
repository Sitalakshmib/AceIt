"""
Practice Mode Service

Handles IndiaBIX-style practice mode with instant feedback:
- One question at a time
- No question repetition per user/topic
- Instant feedback after answer selection
- Adaptive difficulty progression
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_, func
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from typing import Dict, Optional
import datetime


class PracticeService:
    """Service for managing practice mode question flow"""
    
    @staticmethod
    def get_next_question(
        db: Session,
        user_id: str,
        category: str,
        topic: Optional[str] = None
    ) -> Optional[Dict]:
        """
        Get next unattempted question for user in practice mode.
        
        Args:
            db: Database session
            user_id: User ID
            category: Question category
            topic: Optional specific topic
            
        Returns:
            Question dict without correct answer, or None if no questions available
        """
        # Get user's progress for adaptive difficulty
        progress = db.query(UserAptitudeProgress).filter(
            and_(
                UserAptitudeProgress.user_id == user_id,
                UserAptitudeProgress.category == category,
                UserAptitudeProgress.topic == topic if topic else True
            )
        ).first()
        
        # Determine difficulty level
        if progress:
            difficulty = progress.current_difficulty
        else:
            difficulty = "easy"  # Start with easy for new users
        
        # Get IDs of questions already attempted by this user in this topic
        attempted_query = db.query(QuestionAttempt.question_id).filter(
            QuestionAttempt.user_id == user_id,
            QuestionAttempt.category == category,
            QuestionAttempt.context == "practice"
        )
        
        if topic:
            attempted_query = attempted_query.filter(QuestionAttempt.topic == topic)
        
        attempted_ids = [row[0] for row in attempted_query.all()]
        
        # Query for unattempted questions at current difficulty
        query = db.query(AptitudeQuestion).filter(
            AptitudeQuestion.category == category,
            AptitudeQuestion.difficulty == difficulty
        )
        
        if topic:
            query = query.filter(AptitudeQuestion.topic == topic)
        
        # Exclude attempted questions
        if attempted_ids:
            query = query.filter(~AptitudeQuestion.id.in_(attempted_ids))
        
        # Get random question
        question = query.order_by(func.random()).first()
        
        # If no questions at current difficulty, try other difficulties
        if not question:
            for fallback_diff in ["easy", "medium", "hard"]:
                if fallback_diff == difficulty:
                    continue
                    
                query = db.query(AptitudeQuestion).filter(
                    AptitudeQuestion.category == category,
                    AptitudeQuestion.difficulty == fallback_diff
                )
                
                if topic:
                    query = query.filter(AptitudeQuestion.topic == topic)
                
                if attempted_ids:
                    query = query.filter(~AptitudeQuestion.id.in_(attempted_ids))
                
                question = query.order_by(func.random()).first()
                if question:
                    break
        
        if not question:
            return None
        
        # Return question without correct answer
        return {
            "question_id": question.id,
            "question": question.question,
            "options": question.options,
            "category": question.category,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "image_url": question.image_url  # Include chart image for Data Interpretation
        }
    
    @staticmethod
    def submit_answer(
        db: Session,
        user_id: str,
        question_id: str,
        user_answer: int,
        time_spent: int
    ) -> Dict:
        """
        Submit answer and get instant feedback.
        
        Args:
            db: Database session
            user_id: User ID
            question_id: Question ID
            user_answer: Selected answer index
            time_spent: Time spent in seconds
            
        Returns:
            Feedback dict with correctness, explanation, and adaptive info
        """
        # Get question
        question = db.query(AptitudeQuestion).filter(
            AptitudeQuestion.id == question_id
        ).first()
        
        if not question:
            raise ValueError(f"Question {question_id} not found")
        
        # Check correctness
        is_correct = (question.correct_answer == user_answer)
        
        # Update user progress via Adaptive Engine (centralized logic)
        from services.adaptive_engine import AdaptiveEngine, get_or_create_progress
        
        # Get state before update (to detect difficulty change for feedback)
        progress_before = get_or_create_progress(db, user_id, question.topic, question.category)
        old_difficulty = progress_before.current_difficulty if progress_before else "easy"
        
        # Update progress (records attempt + calculates sliding window difficulty)
        AdaptiveEngine.update_progress(db, user_id, question, is_correct, time_spent)
        
        # Get state after update
        progress_after = get_or_create_progress(db, user_id, question.topic, question.category)
        new_difficulty = progress_after.current_difficulty if progress_after else old_difficulty
        
        # Generate adaptive message
        adaptive_message = None
        if new_difficulty != old_difficulty:
            if new_difficulty == "medium" and old_difficulty == "easy":
                adaptive_message = "Great job! Moving to medium difficulty."
            elif new_difficulty == "hard" and old_difficulty == "medium":
                adaptive_message = "Excellent! Moving to hard difficulty."
            elif new_difficulty == "medium" and old_difficulty == "hard":
                adaptive_message = "Let's try medium difficulty questions."
            elif new_difficulty == "easy" and old_difficulty == "medium":
                adaptive_message = "Let's practice with easier questions."
                
        # Return instant feedback
        return {
            "is_correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": question.correct_answer,
            "explanation": question.answer_explanation,
            "options": question.options,
            "adaptive_feedback": {
                "old_difficulty": old_difficulty,
                "new_difficulty": new_difficulty,
                "consecutive_correct": progress_after.consecutive_correct if progress_after else 0,
                "consecutive_incorrect": progress_after.consecutive_incorrect if progress_after else 0,
                "message": adaptive_message,
                "overall_accuracy": round(progress_after.overall_accuracy, 1) if progress_after else 0.0,
                "questions_attempted": progress_after.questions_attempted if progress_after else 0
            }
        }
