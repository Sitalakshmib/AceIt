"""
Mock Test Service

Handles generation, management, and scoring of mock aptitude tests.
Supports multiple test types:
- Full-length tests (100 questions, 90 minutes)
- Section-wise tests (30 questions, 30 minutes)
- Topic-wise tests (20 questions, 20 minutes)
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from models.mock_test_sql import MockTest, MockTestAttempt, MockTestResponse
from models.aptitude_sql import AptitudeQuestion
from typing import Dict, List
import random
import datetime


class MockTestService:
    """Service for generating and managing mock tests"""
    
    @staticmethod
    def generate_full_length_test(db: Session) -> MockTest:
        """
        Generate a full-length aptitude test
        - 100 questions total
        - 90 minutes duration
        - Balanced across all available categories
        """
        # Get all distinct categories
        all_categories = db.query(AptitudeQuestion.category).distinct().all()
        all_categories = [c[0] for c in all_categories]
        
        if not all_categories:
            raise ValueError("No questions available in the database")

        # Basic distribution across all categories
        per_category_count = 100 // len(all_categories)
        remainder = 100 % len(all_categories)
        
        distribution = {cat: per_category_count for cat in all_categories}
        # Add remainder to the categories with most questions
        if remainder > 0:
            top_cats = db.query(AptitudeQuestion.category, func.count(AptitudeQuestion.id))\
                .group_by(AptitudeQuestion.category)\
                .order_by(func.count(AptitudeQuestion.id).desc())\
                .limit(remainder).all()
            for cat, _ in top_cats:
                distribution[cat] += 1

        difficulty_dist = {"easy": 20, "medium": 40, "hard": 40}
        question_ids = []
        
        for category, count in distribution.items():
            # Calculate per-difficulty count (20% Easy, 40% Medium, 40% Hard)
            easy_count = int(count * 0.2)
            medium_count = int(count * 0.4)
            hard_count = count - easy_count - medium_count
            
            # Fetch questions for each difficulty
            for diff, diff_count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
                questions = db.query(AptitudeQuestion.id)\
                    .filter(AptitudeQuestion.category == category)\
                    .filter(AptitudeQuestion.difficulty == diff)\
                    .order_by(func.random())\
                    .limit(diff_count).all()
                
                # If not enough questions of this difficulty, take from any other difficulty in same category
                if len(questions) < diff_count:
                    missing = diff_count - len(questions)
                    backfill_ids = [q.id for q in questions]
                    more_questions = db.query(AptitudeQuestion.id)\
                        .filter(AptitudeQuestion.category == category)\
                        .filter(AptitudeQuestion.id.notin_(backfill_ids))\
                        .order_by(func.random())\
                        .limit(missing).all()
                    questions.extend(more_questions)
                
                question_ids.extend([q.id for q in questions])
        
        # Shuffle to mix categories
        random.shuffle(question_ids)
        
        # Ensure we have at least SOME questions if not 100
        if not question_ids:
             raise ValueError("Failed to generate any questions for the test")

        mock_test = MockTest(
            test_type="full_length",
            total_questions=len(question_ids),
            duration_minutes=90,
            difficulty_distribution=difficulty_dist,
            question_ids=question_ids
        )
        db.add(mock_test)
        db.commit()
        db.refresh(mock_test)
        
        return mock_test
    
    @staticmethod
    def generate_section_test(db: Session, category: str) -> MockTest:
        """
        Generate section-wise test
        - 30 questions from specified category
        - 30 minutes duration
        - Balanced difficulty distribution
        """
        difficulty_dist = {"easy": 20, "medium": 40, "hard": 40}
        question_ids = []
        
        # Calculate per-difficulty count (20% Easy, 40% Medium, 40% Hard)
        total_questions = 30
        easy_count = int(total_questions * 0.2)
        medium_count = int(total_questions * 0.4)
        hard_count = total_questions - easy_count - medium_count
        
        # Fetch questions for each difficulty
        for diff, diff_count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
            questions = db.query(AptitudeQuestion.id)\
                .filter(AptitudeQuestion.category == category)\
                .filter(AptitudeQuestion.difficulty == diff)\
                .order_by(func.random())\
                .limit(diff_count).all()
            
            # Backfill if not enough of this difficulty
            if len(questions) < diff_count:
                missing = diff_count - len(questions)
                backfill_ids = [q.id for q in questions]
                more_questions = db.query(AptitudeQuestion.id)\
                    .filter(AptitudeQuestion.category == category)\
                    .filter(AptitudeQuestion.id.notin_(backfill_ids))\
                    .order_by(func.random())\
                    .limit(missing).all()
                questions.extend(more_questions)

            question_ids.extend([q.id for q in questions])
        
        random.shuffle(question_ids)
        
        mock_test = MockTest(
            test_type="section_wise",
            category=category,
            total_questions=len(question_ids),
            duration_minutes=30,
            difficulty_distribution=difficulty_dist,
            question_ids=question_ids
        )
        db.add(mock_test)
        db.commit()
        db.refresh(mock_test)
        
        return mock_test
    
    @staticmethod
    def generate_topic_test(db: Session, category: str, topic: str) -> MockTest:
        """
        Generate topic-wise test
        - 20 questions from specified topic
        - 20 minutes duration
        - Balanced difficulty distribution
        """
        difficulty_dist = {"easy": 20, "medium": 40, "hard": 40}
        question_ids = []
        
        # Calculate per-difficulty count (2 Easy, 4 Medium, 4 Hard for 10 questions)
        total_questions = 10
        easy_count = 2
        medium_count = 4
        hard_count = 4
        
        # Fetch questions for each difficulty
        for diff, diff_count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
            questions = db.query(AptitudeQuestion.id)\
                .filter(AptitudeQuestion.category == category)\
                .filter(AptitudeQuestion.topic == topic)\
                .filter(AptitudeQuestion.difficulty == diff)\
                .order_by(func.random())\
                .limit(diff_count).all()
            
            # Backfill if not enough of this difficulty
            if len(questions) < diff_count:
                missing = diff_count - len(questions)
                backfill_ids = [q.id for q in questions]
                more_questions = db.query(AptitudeQuestion.id)\
                    .filter(AptitudeQuestion.category == category)\
                    .filter(AptitudeQuestion.topic == topic)\
                    .filter(AptitudeQuestion.id.notin_(backfill_ids))\
                    .order_by(func.random())\
                    .limit(missing).all()
                questions.extend(more_questions)

            question_ids.extend([q.id for q in questions])
        
        random.shuffle(question_ids)
        
        mock_test = MockTest(
            test_type="topic_wise",
            category=category,
            topic=topic,
            total_questions=len(question_ids),
            duration_minutes=20,
            difficulty_distribution=difficulty_dist,
            question_ids=question_ids
        )
        db.add(mock_test)
        db.commit()
        db.refresh(mock_test)
        
        return mock_test
    
    @staticmethod
    def start_attempt(db: Session, user_id: str, mock_test_id: str) -> MockTestAttempt:
        """
        Start a mock test attempt
        
        Args:
            db: Database session
            user_id: User ID
            mock_test_id: Mock test ID
            
        Returns:
            MockTestAttempt object
        """
        test = db.query(MockTest).filter(MockTest.id == mock_test_id).first()
        if not test:
            raise ValueError(f"Mock test {mock_test_id} not found")
        
        attempt = MockTestAttempt(
            user_id=user_id,
            mock_test_id=mock_test_id,
            total_questions=test.total_questions,
            status="in_progress"
        )
        db.add(attempt)
        db.commit()
        db.refresh(attempt)
        return attempt
    
    @staticmethod
    def submit_answer(
        db: Session,
        attempt_id: str,
        question_id: str,
        user_answer: int,
        time_spent: int
    ):
        """
        Submit answer for a question in mock test
        
        Args:
            db: Database session
            attempt_id: Mock test attempt ID
            question_id: Question ID
            user_answer: User's selected answer index
            time_spent: Time spent on question in seconds
        """
        question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found")
        
        is_correct = (question.correct_answer == user_answer)
        
        # Check if response already exists (update if so)
        existing_response = db.query(MockTestResponse)\
            .filter(MockTestResponse.attempt_id == attempt_id)\
            .filter(MockTestResponse.question_id == question_id)\
            .first()
        
        if existing_response:
            existing_response.user_answer = user_answer
            existing_response.is_correct = is_correct
            existing_response.time_spent_seconds = time_spent
            existing_response.answered_at = datetime.datetime.utcnow()
        else:
            response = MockTestResponse(
                attempt_id=attempt_id,
                question_id=question_id,
                user_answer=user_answer,
                is_correct=is_correct,
                time_spent_seconds=time_spent,
                answered_at=datetime.datetime.utcnow()
            )
            db.add(response)
        
        db.commit()
    
    @staticmethod
    def complete_attempt(db: Session, attempt_id: str) -> Dict:
        """
        Complete and score a mock test attempt
        
        Args:
            db: Database session
            attempt_id: Mock test attempt ID
            
        Returns:
            Dictionary with score, accuracy, and timing information
        """
        attempt = db.query(MockTestAttempt).filter(MockTestAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError(f"Attempt {attempt_id} not found")
        
        responses = db.query(MockTestResponse)\
            .filter(MockTestResponse.attempt_id == attempt_id).all()
        
        # Calculate score
        score = sum(1 for r in responses if r.is_correct)
        total_time = sum(r.time_spent_seconds for r in responses if r.time_spent_seconds)
        
        # Update attempt
        attempt.score = score
        attempt.accuracy_percentage = (score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
        attempt.time_taken_seconds = total_time
        attempt.completed_at = datetime.datetime.utcnow()
        attempt.status = "completed"
        
        db.commit()
        
        # Calculate category-wise performance
        category_performance = {}
        for response in responses:
            question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == response.question_id).first()
            if question:
                cat = question.category
                if cat not in category_performance:
                    category_performance[cat] = {"correct": 0, "total": 0}
                category_performance[cat]["total"] += 1
                if response.is_correct:
                    category_performance[cat]["correct"] += 1
        
        # Calculate accuracy per category
        for cat in category_performance:
            total = category_performance[cat]["total"]
            correct = category_performance[cat]["correct"]
            category_performance[cat]["accuracy"] = (correct / total) * 100 if total > 0 else 0
        
        return {
            "score": score,
            "total": attempt.total_questions,
            "accuracy": attempt.accuracy_percentage,
            "time_taken": total_time,
            "category_performance": category_performance
        }
    
    @staticmethod
    def get_test_results(db: Session, attempt_id: str) -> Dict:
        """
        Get detailed results for a completed mock test
        
        Args:
            db: Database session
            attempt_id: Mock test attempt ID
            
        Returns:
            Dictionary with detailed results including all questions and answers
        """
        attempt = db.query(MockTestAttempt).filter(MockTestAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError(f"Attempt {attempt_id} not found")
        
        responses = db.query(MockTestResponse)\
            .filter(MockTestResponse.attempt_id == attempt_id).all()
        
        detailed_results = []
        for response in responses:
            question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == response.question_id).first()
            if question:
                detailed_results.append({
                    "question_id": question.id,
                    "question": question.question,
                    "options": question.options,
                    "user_answer": response.user_answer,
                    "correct_answer": question.correct_answer,
                    "is_correct": response.is_correct,
                    "explanation": question.answer_explanation,
                    "category": question.category,
                    "topic": question.topic,
                    "difficulty": question.difficulty,
                    "time_spent": response.time_spent_seconds
                })
        
        return {
            "attempt_id": attempt_id,
            "score": attempt.score,
            "total": attempt.total_questions,
            "accuracy": attempt.accuracy_percentage,
            "time_taken": attempt.time_taken_seconds,
            "started_at": attempt.started_at.isoformat() if attempt.started_at else None,
            "completed_at": attempt.completed_at.isoformat() if attempt.completed_at else None,
            "detailed_results": detailed_results
        }
