import sys
import os
import random
import uuid

# Add current directory to path
sys.path.append(os.getcwd())

from database_postgres import SessionLocal
from services.mock_test_service import MockTestService
from models.aptitude_sql import UserAptitudeProgress, AptitudeQuestion
from models.user_sql import User

def verify_submissions():
    db = SessionLocal()
    
    # 0. Get or Create Valid User
    user_email = "test_verify@example.com"
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        user = User(
            email=user_email,
            username="VerificationUser",
            password="hashed_password_dummy"
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"✅ Created New Verification User: {user.id}")
    else:
        print(f"✅ Using Existing Verification User: {user.id}")
    
    user_id = user.id
    print(f"Starting Verification with User ID: {user_id}")
    
    try:
        # 1. Ensure we have questions...
        # (Assuming DB has questions based on previous context, if not, we might fail here, 
        # but let's assume standard environment with seeds)
        q_count = db.query(AptitudeQuestion).count()
        print(f"Total Questions in DB: {q_count}")
        if q_count < 10:
             print("WARNING: Not enough questions. Verification might fail.")

        # Get valid category/topic from DB to ensure we have questions
        valid_q = db.query(AptitudeQuestion.category, AptitudeQuestion.topic).filter(AptitudeQuestion.topic != None).first()
        if not valid_q:
            print("❌ No questions with topics found!")
            return
            
        valid_cat, valid_topic = valid_q
        print(f"Using Category: {valid_cat}, Topic: {valid_topic}")

        # Types to test
        test_types = [
            ("topic_wise", valid_cat, valid_topic),
            ("section_wise", valid_cat, None),
            ("full_length", None, None)
        ]

        for t_type, cat, topic in test_types:
            print(f"\n--- Testing {t_type} ---")
            
            # 1. Generate Test
            try:
                if t_type == "full_length":
                    test = MockTestService.generate_full_length_test(db)
                elif t_type == "section_wise":
                    test = MockTestService.generate_section_test(db, cat)
                else:
                    test = MockTestService.generate_topic_test(db, cat, topic)
                print(f"✅ Generated Test ID: {test.id}. Questions: {test.total_questions}, Time: {test.duration_minutes}m")
                 
                if test.total_questions == 0:
                    print("❌ SKIPPING: Test generated with 0 questions.")
                    continue

            except Exception as e:
                print(f"❌ Failed to generate {t_type}: {e}")
                continue

            # 2. Start Test
            try:
                # FIX: use start_attempt instead of start_test_attempt
                # signature: start_attempt(db, user_id, mock_test_id)
                attempt = MockTestService.start_attempt(db, user_id, test.id)
                print(f"✅ Started Attempt ID: {attempt.id}")
            except Exception as e:
                print(f"❌ Failed to start {t_type}: {e}")
                continue

            # 3. Submit Answers (Simulate taking the test)
            # Answer 5 questions randomly
            questions = test.question_ids
            for i, qid in enumerate(questions[:5]):
                try:
                    # Simulate time spent
                    time_spent = random.randint(10, 60)
                    # Random answer index (0-3)
                    answer_idx = random.randint(0, 3)
                    
                    MockTestService.submit_answer(
                        db, attempt.id, qid, answer_idx, time_spent
                    )
                except Exception as e:
                    print(f"❌ Failed to submit answer for Q{i}: {e}")
            print(f"✅ Submitted 5 answers")

            # 4. Complete Test
            try:
                results = MockTestService.complete_attempt(db, attempt.id)
                print(f"✅ Completed Test. Results: Score={results['score']}/{results['total']}, Accuracy={results['accuracy']}%")
                
                # Validation
                if results['total'] != test.total_questions:
                    print(f"❌ Result Mismatch: Expected {test.total_questions} total, got {results['total']}")
                
                if results['time_taken'] <= 0:
                    print(f"❌ Result Mismatch: Invalid time_taken {results['time_taken']}")
                    
            except Exception as e:
                print(f"❌ Failed to complete {t_type}: {e}")
                import traceback
                traceback.print_exc()

        # 5. Check Progress Updates
        print("\n--- Verifying Progress Updates ---")
        progress = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.user_id == user_id).all()
        if progress:
             print(f"✅ Found {len(progress)} progress records for user.")
             for p in progress:
                 print(f"   - {p.category}/{p.topic}: {p.questions_attempted} attempts, {p.total_time_spent_seconds}s total time")
        else:
             print("❌ No progress records found! (Persistence Bug might still exist)")

    finally:
        db.close()

if __name__ == "__main__":
    verify_submissions()
