"""
Mock Test Service

Handles generation, management, and scoring of mock aptitude tests.
Supports multiple test types:
- Full-length tests (30 questions, 30 minutes)
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
        Generate a full-length aptitude test (Elite CAT/GMAT Style)
        - 50 questions total
        - 60 minutes duration (aggressive timing)
        - Strict Difficulty Split: 20% Easy (10), 40% Medium (20), 40% Hard (20)
        - Diverse: Distributed across ALL available topics
        """
        # 1. Define configurations
        TOTAL_QUESTIONS = 30
        DURATION_MINUTES = 30
        
        # Difficulty counts (0% Easy, 50% Medium, 50% Hard)
        CNT_EASY = 0
        CNT_MEDIUM = int(TOTAL_QUESTIONS * 0.50) # 15
        CNT_HARD = int(TOTAL_QUESTIONS * 0.50)   # 15
        
        difficulty_targets = {
            "easy": CNT_EASY,
            "medium": CNT_MEDIUM,
            "hard": CNT_HARD
        }
        
        # 2. Fetch all available question IDs grouped by (Topic, Difficulty)
        #    This allows us to pick diversely.
        #    Structure: pool[difficulty][topic] = [id1, id2, ...]
        
        raw_questions = db.query(AptitudeQuestion.id, AptitudeQuestion.topic, AptitudeQuestion.difficulty).all()
        
        if not raw_questions:
            raise ValueError("No questions available in database to generate test.")

        pool = {
            "easy": {},
            "medium": {},
            "hard": {}
        }
        
        for qid, topic, diff in raw_questions:
            d_key = diff.lower() if diff else "medium"
            if d_key not in pool: d_key = "medium" # Fallback
            
            if topic not in pool[d_key]:
                pool[d_key][topic] = []
            pool[d_key][topic].append(qid)
            
        selected_question_ids = []
        
        # 3. Select questions for each difficulty tier
        for diff_level, target_count in difficulty_targets.items():
            level_pool = pool[diff_level] # {topic: [ids]}
            available_topics = list(level_pool.keys())
            
            if not available_topics:
                # If absolute zero questions for this difficulty, we track 0. 
                # (Ideally we should backfill from other difficulties, but strict requirement implies structure)
                continue
                
            level_selected = []
            
            # --- Round Robin Selection for Diversity ---
            # We cycle through topics picking 1 question from each unti target reached
            
            while len(level_selected) < target_count:
                # Shuffle topics to ensure random start point each pass
                random.shuffle(available_topics)
                added_in_this_pass = False
                
                for topic in available_topics:
                    if len(level_selected) >= target_count:
                        break
                        
                    topic_ids = level_pool[topic]
                    
                    # Find an ID not already selected (though unlikely in this flow unless duplicate topic names across diffs? No, logic is safe)
                    # We modify the list in place to "consume" questions
                    if topic_ids:
                        picked_id = topic_ids.pop(random.randrange(len(topic_ids)))
                        level_selected.append(picked_id)
                        added_in_this_pass = True
                
                if not added_in_this_pass:
                    # We ran out of questions in this difficulty across ALL topics
                    break
            
            selected_question_ids.extend(level_selected)
            
            # If we couldn't meet the target for this difficulty (e.g. need 20 hard, only have 5), 
            # we should technically backfill with Medium or Hard to keep total 50.
            # Let's simple-backfill from remaining pool of any difficulty if strict count failed
            
        # 4. Final Backfill (Safety Net)
        # If total < 50, randomly pick from ANY remaining questions not yet selected
        if len(selected_question_ids) < TOTAL_QUESTIONS:
            missing = TOTAL_QUESTIONS - len(selected_question_ids)
            all_ids = [q[0] for q in raw_questions]
            remaining = list(set(all_ids) - set(selected_question_ids))
            
            if len(remaining) >= missing:
                backfill = random.sample(remaining, missing)
                selected_question_ids.extend(backfill)
            else:
                selected_question_ids.extend(remaining) # Take all we have
        
        # 5. Final Shuffle
        random.shuffle(selected_question_ids)
        
        if not selected_question_ids:
             raise ValueError("Failed to generate any questions.")

        mock_test = MockTest(
            test_type="full_length",
            total_questions=len(selected_question_ids),
            duration_minutes=DURATION_MINUTES,
            difficulty_distribution={"easy": CNT_EASY, "medium": CNT_MEDIUM, "hard": CNT_HARD},
            question_ids=selected_question_ids
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
        difficulty_dist = {"easy": 0, "medium": 50, "hard": 50}
        question_ids = []
        
        # Calculate per-difficulty count (0% Easy, 50% Medium, 50% Hard)
        total_questions = 30
        easy_count = 0
        medium_count = int(total_questions * 0.5) # 15
        hard_count = int(total_questions * 0.5) # 15
        
        # Fetch questions for each difficulty
        for diff, diff_count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
            # DB uses Title Case for difficulty
            db_diff = diff.title()
            
            questions = db.query(AptitudeQuestion.id)\
                .filter(AptitudeQuestion.category == category)\
                .filter(func.lower(AptitudeQuestion.difficulty) == db_diff.lower())\
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
        difficulty_dist = {"easy": 0, "medium": 50, "hard": 50}
        question_ids = []
        
        # Calculate per-difficulty count (0% Easy, 50% Medium, 50% Hard)
        total_questions = 20
        easy_count = 0
        medium_count = int(total_questions * 0.5) # 10
        hard_count = int(total_questions * 0.5) # 10
        
        # Fetch questions for each difficulty
        for diff, diff_count in [("easy", easy_count), ("medium", medium_count), ("hard", hard_count)]:
            # DB uses Title Case for difficulty
            db_diff = diff.title()
            
            questions = db.query(AptitudeQuestion.id)\
                .filter(AptitudeQuestion.category == category)\
                .filter(AptitudeQuestion.topic == topic)\
                .filter(func.lower(AptitudeQuestion.difficulty) == db_diff.lower())\
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
        user_answer: int = None,
        time_spent: int = 0,
        answer_text: str = None
    ):
        """
        Submit answer for a question in mock test
        
        Args:
            db: Database session
            attempt_id: Mock test attempt ID
            question_id: Question ID
            user_answer: User's selected answer index (Optional)
            time_spent: Time spent on question in seconds
            answer_text: User's selected answer text (Preferred for shuffled options)
        """
        question = db.query(AptitudeQuestion).filter(AptitudeQuestion.id == question_id).first()
        if not question:
            raise ValueError(f"Question {question_id} not found")
        
        # Resolve user_answer index if text is provided
        if answer_text is not None:
            try:
                # Find the index of the text in the original options list
                # This maps the shuffled selection back to the canonical index
                user_answer = question.options.index(answer_text)
            except ValueError:
                # Text not found in options? Treat as wrong or handle error
                # For safety, if text mismatch, we can set -1 or None
                user_answer = -1
        
        if user_answer is None:
             raise ValueError("Either user_answer (index) or answer_text must be provided")

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
        
        print(f"[MOCK_TEST] Completing attempt {attempt_id} (Test: {attempt.mock_test_id})")

        responses = db.query(MockTestResponse)\
            .filter(MockTestResponse.attempt_id == attempt_id).all()
        
        # --- SYNC TO PROGRESS TRACKING ---
        from models.aptitude_sql import UserAptitudeProgress
        
        # Batch fetch all questions involved in this attempt
        question_ids = [r.question_id for r in responses]
        questions_map = {q.id: q for q in db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()}
        
        # Group responses by (category, topic) for efficient batch updating
        progress_updates = {}
        topic_performance = {}
        category_performance = {} # Track this for return dict
        score = 0
        
        # --- PRECISE TIMING CALCULATION ---
        # Fetch test for duration limit
        test = db.query(MockTest).filter(MockTest.id == attempt.mock_test_id).first()
        max_duration_sec = (test.duration_minutes * 60) if test else 3600 # Default 1hr if missing
        
        completion_time = datetime.datetime.utcnow()
        wall_clock_duration = (completion_time - attempt.started_at).total_seconds()
        
        # Final accurate total time taken (capped by test limit)
        total_time_taken_taken = min(wall_clock_duration, max_duration_sec)
        
        # For legacy compatibility, we still track individual question times in total_sum_of_responses,
        # but the primary reported time will now be total_time_taken_taken.
        total_sum_of_responses = 0
        
        for r in responses:
            q = questions_map.get(r.question_id)
            if not q:
                continue
                
            # Basic stats
            total_sum_of_responses += (r.time_spent_seconds or 0)
            if r.is_correct:
                score += 1
                
            # Topic performance (for return dict)
            t_key = q.topic or "Miscellaneous"
            if t_key not in topic_performance:
                topic_performance[t_key] = {"correct": 0, "total": 0}
            topic_performance[t_key]["total"] += 1
            if r.is_correct:
                topic_performance[t_key]["correct"] += 1
                
            # Category performance (for return dict)
            c_key = q.category or "General"
            if c_key not in category_performance:
                category_performance[c_key] = {"correct": 0, "total": 0}
            category_performance[c_key]["total"] += 1
            if r.is_correct:
                category_performance[c_key]["correct"] += 1
            
            # Progress tracking stats
            cat = q.category or "General"
            topic = q.topic or "Miscellaneous"
            key = (cat, topic)
            if key not in progress_updates:
                progress_updates[key] = {
                    "attempted": 0, "correct": 0, "time": 0,
                    "easy_total": 0, "easy_correct": 0,
                    "medium_total": 0, "medium_correct": 0,
                    "hard_total": 0, "hard_correct": 0
                }
            
            stats = progress_updates[key]
            stats["attempted"] += 1
            stats["time"] += (r.time_spent_seconds or 0)
            if r.is_correct:
                stats["correct"] += 1
                
            diff_raw = q.difficulty or "medium"
            diff = diff_raw.lower()
            if diff == "easy":
                stats["easy_total"] += 1
                if r.is_correct: stats["easy_correct"] += 1
            elif diff == "medium":
                stats["medium_total"] += 1
                if r.is_correct: stats["medium_correct"] += 1
            elif diff == "hard":
                stats["hard_total"] += 1
                if r.is_correct: stats["hard_correct"] += 1

        # Apply updates to UserAptitudeProgress (Batch Fetching)
        user_id = attempt.user_id
        update_keys = list(progress_updates.keys())
        topics = [k[1] for k in update_keys]
        categories = list(set([k[0] for k in update_keys]))
        
        # Fetch all potential progress records for these categories/topics
        existing_progress_list = db.query(UserAptitudeProgress).filter(
            UserAptitudeProgress.user_id == user_id,
            UserAptitudeProgress.category.in_(categories),
            UserAptitudeProgress.topic.in_(topics)
        ).all()
        
        progress_map = {(p.category, p.topic): p for p in existing_progress_list}
        
        for (cat, topic), stats in progress_updates.items():
            progress = progress_map.get((cat, topic))
            
            if not progress:
                progress = UserAptitudeProgress(
                    user_id=user_id, topic=topic, category=cat, current_difficulty="easy"
                )
                db.add(progress)
            
            progress.questions_attempted = (progress.questions_attempted or 0) + stats["attempted"]
            progress.questions_correct = (progress.questions_correct or 0) + stats["correct"]
            progress.total_time_spent_seconds = (progress.total_time_spent_seconds or 0) + stats["time"]
            progress.easy_total = (progress.easy_total or 0) + stats["easy_total"]
            progress.easy_correct = (progress.easy_correct or 0) + stats["easy_correct"]
            progress.medium_total = (progress.medium_total or 0) + stats["medium_total"]
            progress.medium_correct = (progress.medium_correct or 0) + stats["medium_correct"]
            progress.hard_total = (progress.hard_total or 0) + stats["hard_total"]
            progress.hard_correct = (progress.hard_correct or 0) + stats["hard_correct"]
            
            if progress.questions_attempted > 0:
                progress.average_time_per_question = progress.total_time_spent_seconds / progress.questions_attempted
                progress.overall_accuracy = (progress.questions_correct / progress.questions_attempted) * 100
            
            progress.last_practiced = datetime.datetime.utcnow()
            
        # Update attempt record
        attempt.score = score
        attempt.accuracy_percentage = (score / attempt.total_questions) * 100 if attempt.total_questions > 0 else 0
        attempt.time_taken_seconds = total_sum_of_responses
        attempt.completed_at = datetime.datetime.utcnow()
        attempt.status = "completed"
        
        db.commit()
        
        # Calculate final accuracies for topic/category results
        for t in topic_performance.values():
            t["accuracy"] = (t["correct"] / t["total"] * 100) if t["total"] > 0 else 0
        for c in category_performance.values():
            c["accuracy"] = (c["correct"] / c["total"] * 100) if c["total"] > 0 else 0

        avg_time = total_sum_of_responses / attempt.total_questions if attempt.total_questions > 0 else 0

        return {
            "score": score,
            "total": attempt.total_questions,
            "accuracy": attempt.accuracy_percentage,
            "time_taken": total_sum_of_responses,
            "average_time_per_question": avg_time,
            "category_performance": category_performance,
            "topic_performance": topic_performance
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
        
        # Batch fetch all questions involved
        question_ids = [r.question_id for r in responses]
        questions_map = {q.id: q for q in db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()}
        
        detailed_results = []
        for response in responses:
            question = questions_map.get(response.question_id)
            if question:
                detailed_results.append({
                    "question_id": question.id,
                    "question_text": question.question,
                    "your_answer": response.answer_text if response.answer_text else (question.options[response.user_answer] if response.user_answer is not None and response.user_answer < len(question.options) else "Not Answered"),
                    "correct_answer": question.options[question.correct_answer] if question.correct_answer is not None and question.correct_answer < len(question.options) else "Unknown",
                    "is_correct": response.is_correct,
                    "explanation": question.answer_explanation,
                    "time_spent": response.time_spent_seconds,
                    "category": question.category,
                    "topic": question.topic,
                    "difficulty": question.difficulty,
                    "image_url": question.image_url
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
