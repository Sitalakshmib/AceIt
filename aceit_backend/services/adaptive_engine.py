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
        Determine next difficulty using Batch Logic (Every 4 questions).
        
        Rules:
        - Only check when total attempts % 4 == 0.
        - Fetch last 4 attempts.
        - Accuracy >= 75% (3/4 or 4/4) -> Level Up.
        - Accuracy < 25% (0/4) -> Level Down.
        - Otherwise -> Stay.
        """
        
        # 0. Get total attempts to check batch boundary
        # We can count from QuestionAttempt table to be sure, or rely on caller?
        # Better to query DB for robustness.
        total_attempts = db.query(QuestionAttempt).filter(
            QuestionAttempt.user_id == user_id,
            QuestionAttempt.topic == topic,
            QuestionAttempt.context == "practice"
        ).count()
        
        # If not at batch boundary (4, 8, 12...), stay at current difficulty
        # Note: This function is called AFTER the current attempt is recorded.
        if total_attempts == 0 or total_attempts % 4 != 0:
            return current_difficulty
            
        # 1. Fetch last 4 attempts for this topic/user
        attempts = db.query(QuestionAttempt)\
            .filter(
                QuestionAttempt.user_id == user_id,
                QuestionAttempt.topic == topic,
                QuestionAttempt.context == "practice"
            )\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(4).all()
            
        if not attempts or len(attempts) < 4:
            return current_difficulty
            
        # 2. Calculate metrics
        correct_count = sum(1 for a in attempts if a.is_correct)
        accuracy = (correct_count / 4) * 100
        
        # 3. Difficulty Logic
        # Normalize input to ensure matching
        current_lower = current_difficulty.lower()
        
        try:
            current_index = AdaptiveEngine.DIFFICULTY_LEVELS.index(current_lower)
        except ValueError:
            return "easy"
            
        # LEVEL UP
        # Accuracy >= 75%
        if accuracy >= 75:
            if current_index < len(AdaptiveEngine.DIFFICULTY_LEVELS) - 1:
                return AdaptiveEngine.DIFFICULTY_LEVELS[current_index + 1]
                
        # LEVEL DOWN
        # Accuracy < 25%
        elif accuracy < 25:
            if current_index > 0:
                return AdaptiveEngine.DIFFICULTY_LEVELS[current_index - 1]
                
        return current_lower

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
        q_diff = question.difficulty.lower() if question.difficulty else "medium"
        
        if q_diff == "easy":
            progress.easy_total += 1
            if is_correct: progress.easy_correct += 1
        elif q_diff == "medium":
            progress.medium_total += 1
            if is_correct: progress.medium_correct += 1
        elif q_diff == "hard":
            progress.hard_total += 1
            if is_correct: progress.hard_correct += 1
            
        # Time tracking
        progress.total_time_spent_seconds += time_spent
        if progress.questions_attempted > 0:
            progress.average_time_per_question = (
                progress.total_time_spent_seconds / progress.questions_attempted
            )
        
        # Update overall accuracy
        if progress.questions_attempted > 0:
            progress.overall_accuracy = (progress.questions_correct / progress.questions_attempted) * 100

        # Calculate recent accuracy (last 10 questions)
        recent_attempts = db.query(QuestionAttempt)\
            .filter(
                QuestionAttempt.user_id == user_id,
                QuestionAttempt.topic == question.topic,
                QuestionAttempt.context == "practice"
            )\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(10).all()
        
        if recent_attempts:
            recent_correct = sum(1 for a in recent_attempts if a.is_correct)
            progress.recent_accuracy = (recent_correct / len(recent_attempts)) * 100
             
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
    
    # ========================================================================
    # MULTI-DIMENSIONAL ADAPTIVE INTELLIGENCE (4D)
    # ========================================================================
    
    @staticmethod
    def calculate_multidimensional_difficulty(
        db: Session,
        user_id: str,
        topic: str,
        category: str,
        performance_history: list = None
    ) -> dict:
        """
        Calculate difficulty across 4 dimensions:
        1. Difficulty Level (Beginner → Elite)
        2. Concept Depth (single → multi)
        3. Cognitive Load (low → very_high)
        4. Trap Density (low → high)
        
        Returns comprehensive difficulty profile for next question
        """
        from services.question_taxonomy import classify_user_tier, get_recommended_difficulty
        
        # Get user progress
        progress = get_or_create_progress(db, user_id, topic, category)
        if not progress:
            return {
                "difficulty_level": "Beginner",
                "concept_depth": "single",
                "cognitive_load": "low",
                "trap_density": "low",
                "time_pressure": "relaxed"
            }
        
        # Calculate overall accuracy and time ratio
        accuracy = 0
        if progress.questions_attempted > 0:
            accuracy = (progress.questions_correct / progress.questions_attempted) * 100
        
        avg_time_ratio = 1.0
        if progress.average_time_per_question > 0:
            # Assume expected time is 120 seconds (can be refined)
            avg_time_ratio = progress.average_time_per_question / 120
        
        # Classify user tier
        user_tier = classify_user_tier(accuracy, avg_time_ratio)
        base_difficulty = get_recommended_difficulty(user_tier)
        
        # Determine concept depth based on performance
        concept_depth = "single"
        if accuracy >= 70:
            concept_depth = "dual"
        if accuracy >= 85:
            concept_depth = "multi"
        
        # Determine cognitive load
        cognitive_load = "low"
        if progress.questions_attempted >= 10:
            if accuracy >= 60 and avg_time_ratio < 1.0:
                cognitive_load = "medium"
            if accuracy >= 75 and avg_time_ratio < 0.8:
                cognitive_load = "high"
            if accuracy >= 85 and avg_time_ratio < 0.7:
                cognitive_load = "very_high"
        
        # Determine trap density based on error patterns
        trap_density = "low"
        total_errors = (progress.conceptual_errors + progress.careless_errors + 
                       progress.overthinking_errors + progress.time_pressure_errors)
        
        if total_errors > 0:
            # If mostly conceptual errors, keep traps low
            conceptual_ratio = progress.conceptual_errors / total_errors
            if conceptual_ratio < 0.3:  # Low conceptual errors
                trap_density = "medium"
            if conceptual_ratio < 0.15 and accuracy >= 70:
                trap_density = "high"
        
        # Determine time pressure
        time_pressure = "relaxed"
        if avg_time_ratio < 1.0:
            time_pressure = "moderate"
        if avg_time_ratio < 0.8:
            time_pressure = "intense"
        
        return {
            "difficulty_level": base_difficulty,
            "concept_depth": concept_depth,
            "cognitive_load": cognitive_load,
            "trap_density": trap_density,
            "time_pressure": time_pressure,
            "user_tier": user_tier,
            "accuracy": round(accuracy, 2),
            "avg_time_ratio": round(avg_time_ratio, 2)
        }
    
    @staticmethod
    def analyze_error_patterns(
        db: Session,
        user_id: str,
        topic: str,
        recent_count: int = 20
    ) -> dict:
        """
        Analyze error patterns from recent attempts
        
        Categorizes errors into:
        - conceptual: wrong approach, formula misapplication
        - careless: calculation mistakes, sign errors
        - overthinking: correct approach but complicated unnecessarily
        - time_pressure: rushed answers, incomplete reasoning
        
        Returns error distribution and recommendations
        """
        # Fetch recent attempts
        attempts = db.query(QuestionAttempt)\
            .filter(
                QuestionAttempt.user_id == user_id,
                QuestionAttempt.topic == topic,
                QuestionAttempt.is_correct == False  # Only wrong answers
            )\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(recent_count).all()
        
        if not attempts:
            return {
                "total_errors": 0,
                "pattern_distribution": {},
                "dominant_pattern": None,
                "recommendation": "Keep practicing to build performance history"
            }
        
        # Analyze patterns (heuristic-based for now)
        error_counts = {
            "conceptual": 0,
            "careless": 0,
            "overthinking": 0,
            "time_pressure": 0,
            "unknown": 0
        }
        
        for attempt in attempts:
            # Heuristic classification based on time and difficulty
            time_spent = attempt.time_spent_seconds
            difficulty = attempt.difficulty_at_attempt
            
            # Expected time thresholds
            expected_times = {"easy": 60, "medium": 90, "hard": 120}
            expected = expected_times.get(difficulty, 90)
            
            if time_spent < expected * 0.5:
                # Too fast - likely rushed or careless
                error_counts["time_pressure"] += 1
            elif time_spent > expected * 1.5:
                # Too slow - likely overthinking
                error_counts["overthinking"] += 1
            elif time_spent > expected * 0.7 and time_spent < expected * 1.3:
                # Normal time but wrong - likely conceptual
                error_counts["conceptual"] += 1
            else:
                # Quick but not rushed - likely careless
                error_counts["careless"] += 1
        
        # Find dominant pattern
        dominant = max(error_counts.items(), key=lambda x: x[1])
        
        # Generate recommendation
        recommendations = {
            "conceptual": "Focus on understanding core concepts. Review theory before practicing.",
            "careless": "Slow down and double-check calculations. Practice accuracy drills.",
            "overthinking": "Trust your initial approach. Practice pattern recognition for faster solutions.",
            "time_pressure": "Work on time management. Practice with timer to build speed.",
            "unknown": "Continue practicing to establish clearer patterns."
        }
        
        return {
            "total_errors": len(attempts),
            "pattern_distribution": error_counts,
            "dominant_pattern": dominant[0],
            "dominant_count": dominant[1],
            "recommendation": recommendations.get(dominant[0], "Keep practicing")
        }
    
    @staticmethod
    def generate_follow_up_logic(
        is_correct: bool,
        time_spent: int,
        expected_time: int,
        current_difficulty: str,
        accuracy_history: float
    ) -> dict:
        """
        Generate adaptive follow-up instructions based on performance
        
        Args:
            is_correct: Whether answer was correct
            time_spent: Time taken in seconds
            expected_time: Expected time for this difficulty
            current_difficulty: Current difficulty level
            accuracy_history: Recent accuracy percentage
        
        Returns:
            Dictionary with if_correct and if_wrong strategies
        """
        time_ratio = time_spent / expected_time if expected_time > 0 else 1.0
        
        if is_correct:
            # Correct answer - determine how to increase challenge
            if time_ratio < 0.7:
                # Fast and correct - significantly increase difficulty
                strategy = {
                    "action": "increase_difficulty",
                    "adjustment": "Increase trap density and cognitive load. Add time constraints.",
                    "next_difficulty": AdaptiveEngine._get_next_level(current_difficulty),
                    "concept_depth": "increase",
                    "trap_density": "increase"
                }
            elif time_ratio < 1.2:
                # Normal time and correct - moderate increase
                strategy = {
                    "action": "moderate_increase",
                    "adjustment": "Introduce multi-concept questions or subtle traps.",
                    "next_difficulty": current_difficulty,
                    "concept_depth": "increase",
                    "trap_density": "maintain"
                }
            else:
                # Slow but correct - maintain difficulty, work on speed
                strategy = {
                    "action": "maintain_difficulty",
                    "adjustment": "Focus on pattern recognition and faster solution paths.",
                    "next_difficulty": current_difficulty,
                    "concept_depth": "maintain",
                    "trap_density": "decrease"
                }
            
            return {
                "if_correct": strategy,
                "if_wrong": None  # Not applicable
            }
        
        else:
            # Wrong answer - determine remedial focus
            if time_ratio < 0.7:
                # Fast and wrong - likely rushed or careless
                strategy = {
                    "action": "slow_down",
                    "adjustment": "Reduce time pressure. Focus on accuracy over speed.",
                    "remedial_focus": "accuracy_training",
                    "next_difficulty": current_difficulty,
                    "concept_depth": "maintain",
                    "trap_density": "decrease"
                }
            elif time_ratio > 1.5:
                # Slow and wrong - likely conceptual gap
                strategy = {
                    "action": "concept_revision",
                    "adjustment": "Review fundamental concepts. Reduce cognitive load.",
                    "remedial_focus": "concept_building",
                    "next_difficulty": AdaptiveEngine._get_prev_level(current_difficulty),
                    "concept_depth": "decrease",
                    "trap_density": "decrease"
                }
            else:
                # Normal time but wrong - likely trap or conceptual
                if accuracy_history < 50:
                    strategy = {
                        "action": "decrease_difficulty",
                        "adjustment": "Build confidence with easier questions. Focus on fundamentals.",
                        "remedial_focus": "foundation_building",
                        "next_difficulty": AdaptiveEngine._get_prev_level(current_difficulty),
                        "concept_depth": "decrease",
                        "trap_density": "decrease"
                    }
                else:
                    strategy = {
                        "action": "trap_awareness",
                        "adjustment": "Practice identifying common traps. Review solution strategies.",
                        "remedial_focus": "trap_recognition",
                        "next_difficulty": current_difficulty,
                        "concept_depth": "maintain",
                        "trap_density": "maintain"
                    }
            
            return {
                "if_correct": None,  # Not applicable
                "if_wrong": strategy
            }
    
    @staticmethod
    def _get_next_level(current: str) -> str:
        """Get next difficulty level"""
        levels = ["Beginner", "Intermediate", "Advanced", "Elite"]
        try:
            idx = levels.index(current)
            return levels[min(idx + 1, len(levels) - 1)]
        except ValueError:
            return "Intermediate"
    
    @staticmethod
    def _get_prev_level(current: str) -> str:
        """Get previous difficulty level"""
        levels = ["Beginner", "Intermediate", "Advanced", "Elite"]
        try:
            idx = levels.index(current)
            return levels[max(idx - 1, 0)]
        except ValueError:
            return "Beginner"
    
    @staticmethod
    def get_performance_signals(
        db: Session,
        user_id: str,
        topic: str,
        recent_count: int = 10
    ) -> dict:
        """
        Get performance signals for question generation
        
        Returns:
            Dictionary with accuracy_trend, time_trend, error_pattern
        """
        attempts = db.query(QuestionAttempt)\
            .filter(
                QuestionAttempt.user_id == user_id,
                QuestionAttempt.topic == topic
            )\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(recent_count).all()
        
        if not attempts or len(attempts) < 3:
            return {
                "accuracy_trend": "insufficient_data",
                "time_trend": "insufficient_data",
                "error_pattern": "insufficient_data"
            }
        
        # Calculate accuracy trend
        correct_count = sum(1 for a in attempts if a.is_correct)
        accuracy = (correct_count / len(attempts)) * 100
        
        if accuracy >= 80:
            accuracy_trend = "high"
        elif accuracy >= 60:
            accuracy_trend = "moderate"
        else:
            accuracy_trend = "low"
        
        # Calculate time trend
        avg_time = sum(a.time_spent_seconds for a in attempts) / len(attempts)
        
        if avg_time < 60:
            time_trend = "fast"
        elif avg_time < 120:
            time_trend = "normal"
        else:
            time_trend = "slow"
        
        # Analyze error pattern
        error_analysis = AdaptiveEngine.analyze_error_patterns(db, user_id, topic, recent_count)
        error_pattern = error_analysis.get("dominant_pattern", "unknown")
        
        return {
            "accuracy_trend": accuracy_trend,
            "time_trend": time_trend,
            "error_pattern": error_pattern,
            "recent_accuracy": round(accuracy, 2),
            "avg_time_seconds": round(avg_time, 2)
        }
