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
import random


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
        
        # --- DIVERSITY LOGIC ---
        # Get the last 3 questions attempted to ensure broader diversity
        recent_attempts = db.query(QuestionAttempt.question_id).filter(
            QuestionAttempt.user_id == user_id,
            QuestionAttempt.category == category,
            QuestionAttempt.context == "practice"
        )
        if topic:
            recent_attempts = recent_attempts.filter(QuestionAttempt.topic == topic)
        recent_attempts = recent_attempts.order_by(QuestionAttempt.attempted_at.desc()).limit(3).all()
        recent_question_ids = [row[0] for row in recent_attempts]
        
        # Build concept frequency map from recent history
        concept_freq = {}
        if recent_question_ids:
            recent_questions = db.query(AptitudeQuestion.primary_concepts).filter(
                AptitudeQuestion.id.in_(recent_question_ids)
            ).all()
            for q in recent_questions:
                if q.primary_concepts:
                    for concept in q.primary_concepts:
                        concept_freq[concept] = concept_freq.get(concept, 0) + 1
        
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
        
        # Get a pool of candidate questions (limit 50 for better selection pool)
        candidates = query.order_by(func.random()).limit(50).all()
        
        # --- SELECT DIVERSE QUESTION ---
        question = None
        if candidates:
            if concept_freq:
                # Score candidates by concept overlap (Lower score = More diverse)
                candidate_scores = []
                for c in candidates:
                    score = 0
                    q_concepts = c.primary_concepts or []
                    for concept in q_concepts:
                        score += concept_freq.get(concept, 0)
                    
                    # Add small random jitter to break ties randomly
                    score += random.random() * 0.5
                    candidate_scores.append((score, c))
                
                # Sort by score (ascending) and pick the best one
                candidate_scores.sort(key=lambda x: x[0])
                question = candidate_scores[0][1]
            else:
                # No recent history, just pick randomly
                question = random.choice(candidates)
        
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
        
        # --- RUNTIME SHUFFLE LOGIC ---
        # Create a shuffled copy of options
        original_options = list(question.options) if question.options else []
        shuffled_options = original_options.copy()
        random.shuffle(shuffled_options)
        
        # Create mapping from shuffled index to original index
        # This allows submit_answer to validate correctly
        original_correct_idx = question.correct_answer
        shuffled_correct_idx = shuffled_options.index(original_options[original_correct_idx]) if 0 <= original_correct_idx < len(original_options) else 0
        
        # Return question without correct answer, but with shuffled options
        return {
            "question_id": question.id,
            "question": question.question,
            "options": shuffled_options,
            "category": question.category,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "image_url": question.image_url,
            # Hidden field for answer validation (frontend should NOT use this)
            "_shuffled_correct_idx": shuffled_correct_idx
        }
    
    @staticmethod
    def submit_answer(
        db: Session,
        user_id: str,
        question_id: str,
        user_answer: int,
        time_spent: int,
        shuffled_options: list = None
    ) -> Dict:
        """
        Submit answer and get instant feedback.
        
        Args:
            db: Database session
            user_id: User ID
            question_id: Question ID
            user_answer: Selected answer index (in the shuffled options order)
            time_spent: Time spent in seconds
            shuffled_options: The shuffled options as displayed to the user
            
        Returns:
            Feedback dict with correctness, explanation, and adaptive info
        """
        # Get question
        question = db.query(AptitudeQuestion).filter(
            AptitudeQuestion.id == question_id
        ).first()
        
        if not question:
            raise ValueError(f"Question {question_id} not found")
        
        # --- HANDLE SHUFFLED OPTIONS VALIDATION ---
        original_options = list(question.options) if question.options else []
        original_correct_idx = question.correct_answer
        correct_text = original_options[original_correct_idx] if 0 <= original_correct_idx < len(original_options) else ""
        
        # If frontend sent shuffled_options, use those. Otherwise, assume no shuffling.
        if shuffled_options and len(shuffled_options) > 0:
            # User selected from shuffled options
            selected_text = shuffled_options[user_answer] if 0 <= user_answer < len(shuffled_options) else ""
            is_correct = (selected_text == correct_text)
            
            # Find the correct answer index in the shuffled order for feedback
            try:
                shuffled_correct_idx = shuffled_options.index(correct_text)
            except ValueError:
                shuffled_correct_idx = original_correct_idx
        else:
            # Fallback: no shuffling, use original logic
            is_correct = (original_correct_idx == user_answer)
            shuffled_correct_idx = original_correct_idx
            shuffled_options = original_options
        
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
                
        # Return instant feedback with shuffled options order preserved
        return {
            "is_correct": is_correct,
            "user_answer": user_answer,
            "correct_answer": shuffled_correct_idx,  # Index in the shuffled order
            "explanation": question.answer_explanation,
            "options": shuffled_options,  # Return the same shuffled order for consistency
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
