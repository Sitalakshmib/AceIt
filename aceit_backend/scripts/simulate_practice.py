from database_postgres import SessionLocal
from services.practice_service import PracticeService
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
import uuid
import sys

from models.user_sql import User
# Actually, let's check where User is defined. 
# It was imported in mock_test_sql.py as `from database_postgres import Base`... user = relationship("User")
# In interview.py: `req.user_id` is just string.
# In `PracticeService`, it queries `UserAptitudeProgress`.
# `UserAptitudeProgress` has `user_id = Column(String, ForeignKey("users.id"))`
# `users.id` implies table name `users`.
# I need to find the User model definition.
# `database_postgres.py`?

from database_postgres import SessionLocal, Base
# User model imported above


def run_simulation():
    db = SessionLocal()
    # Create fake user
    user_id = f"sim_{uuid.uuid4().hex[:8]}"
    try:
        # Try to insert raw SQL to avoid model import issues
        from sqlalchemy import text
        db.execute(text("INSERT INTO users (id, email, password, username) VALUES (:id, :email, 'pass', 'Sim User')"), 
                  {"id": user_id, "email": f"{user_id}@test.com"})
        db.commit()
    except Exception as e:
        print(f"User creation failed: {e}")
        db.rollback()
        return # Cannot proceed without user
        
    category = "Quantitative Ability"
    topic = "Time Speed Distance"
    
    print(f"--- STARTING SIMULATION for User: {user_id} ---")
    
    try:
        # 1. Start Fresh (Reset=True)
        print("\n[Step 1] Initial Request (Reset=True)")
        q1 = PracticeService.get_next_question(db, user_id, category, topic, reset=True)
        
        if not q1:
            print("❌ FAILURE: No questions returned for start!")
            return
            
        print(f"Q1 Difficulty: {q1['difficulty']}")
        if q1['difficulty'] != 'Easy':
            print("❌ FAILURE: Did not start with Easy!")
        else:
            print("✅ SUCCESS: Started with Easy.")

        # 2. Submit 4 Correct Answers (Should trigger Level Up to Medium)
        print("\n[Step 2] Submitting 4 Correct Answers...")
        current_q = q1
        
        for i in range(4):
            # Find correct answer
            # The service returns shuffled options, but also _shuffled_correct_idx hidden field if I look at code?
            # actually get_next_question returns _shuffled_correct_idx.
            correct_idx = current_q['_shuffled_correct_idx']
            
            # Submit
            # We need to pass shuffled_options to validate correctly
            PracticeService.submit_answer(
                db, user_id, current_q['question_id'], correct_idx, 10, current_q['options']
            )
            print(f"  - Answered Q{i+1} Correctly.")
            
            # Get next
            if i < 3:
                current_q = PracticeService.get_next_question(db, user_id, category, topic, reset=False)
                if current_q['difficulty'] != 'Easy':
                    print(f"  ❌ WARNING: Difficulty changed prematurely to {current_q['difficulty']} at Q{i+2}")

        # 5th Question should be Medium
        q5 = PracticeService.get_next_question(db, user_id, category, topic, reset=False)
        print(f"Q5 Difficulty: {q5['difficulty']}")
        
        if q5['difficulty'] == 'Medium':
            print("✅ SUCCESS: Difficulty moved to Medium after 4 correct.")
        else:
            print(f"❌ FAILURE: Difficulty is {q5['difficulty']} (Expected Medium).")

        # 3. Submit 4 Wrong Answers (Should trigger Level Down to Easy)
        print("\n[Step 3] Submitting 4 Wrong Answers at Medium...")
        current_q = q5
        
        for i in range(4):
            # Wrong answer (pick index != correct_idx)
            correct_idx = current_q['_shuffled_correct_idx']
            wrong_idx = (correct_idx + 1) % 4
            
            PracticeService.submit_answer(
                db, user_id, current_q['question_id'], wrong_idx, 10, current_q['options']
            )
            print(f"  - Answered Q{i+1} Incorrectly.")
            
            if i < 3:
                current_q = PracticeService.get_next_question(db, user_id, category, topic, reset=False)

        # 9th Question should be Easy
        q9 = PracticeService.get_next_question(db, user_id, category, topic, reset=False)
        print(f"Q9 Difficulty: {q9['difficulty']}")
        
        if q9['difficulty'] == 'Easy':
             print("✅ SUCCESS: Difficulty moved back to Easy after 4 wrong.")
        else:
             print(f"❌ FAILURE: Difficulty is {q9['difficulty']} (Expected Easy).")
             
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        db.query(QuestionAttempt).filter(QuestionAttempt.user_id == user_id).delete()
        db.query(UserAptitudeProgress).filter(UserAptitudeProgress.user_id == user_id).delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    run_simulation()
