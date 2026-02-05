from database_postgres import SessionLocal, Base
from services.practice_service import PracticeService
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from models.user_sql import User
import uuid
import sys
from sqlalchemy import text

def run_simulation():
    db = SessionLocal()
    # Create fake user
    user_id = f"sim_sliding_{uuid.uuid4().hex[:8]}"
    try:
        db.execute(text("INSERT INTO users (id, email, password, username) VALUES (:id, :email, 'pass', 'Sliding User')"), 
                  {"id": user_id, "email": f"{user_id}@test.com"})
        db.commit()
    except Exception as e:
        print(f"User creation failed: {e}")
        db.rollback()
        return
        
    category = "Quantitative Ability"
    topic = "Time Speed Distance"
    
    print(f"--- STARTING SLIDING WINDOW SIMULATION for User: {user_id} ---")
    
    try:
        # 1. Start Fresh (Reset=True)
        print("\n[Step 1] Initial Request (Reset=True)")
        q1 = PracticeService.get_next_question(db, user_id, category, topic, reset=True)
        print(f"Q1 Difficulty: {q1['difficulty']}")
        
        # 2. Submit 4 WRONG Answers (Should stay at Easy)
        print("\n[Step 2] Submitting 4 WRONG Answers...")
        current_q = q1
        for i in range(4):
            correct_idx = current_q['_shuffled_correct_idx']
            wrong_idx = (correct_idx + 1) % 4
            PracticeService.submit_answer(db, user_id, current_q['question_id'], wrong_idx, 10, current_q['options'])
            print(f"  - Q{i+1} WRONG. Overall Acc so far: {((0)/(i+1))*100}%")
            current_q = PracticeService.get_next_question(db, user_id, category, topic, reset=False)
            
        print(f"Next Question (Q5) Difficulty: {current_q['difficulty']}")
        if current_q['difficulty'].lower() == 'easy':
            print("✅ Status: Stayed at Easy after 4 failures.")
        else:
            print(f"❌ ERROR: Moved to {current_q['difficulty']} despite failures!")

        # 3. Submit 3 CORRECT Answers (Total 7, Last 4 = [W, C, C, C] -> 75%)
        # User requirement: "in the next 4 3 are correct then he will move right... because in this window he got the threshold"
        # Window of 4: Q4(W), Q5(C), Q6(C), Q7(C) -> 3/4 = 75%. Threshold check!
        print("\n[Step 3] Submitting 3 CORRECT Answers (Last 4 = 3/4 = 75%)...")
        for i in range(3):
            correct_idx = current_q['_shuffled_correct_idx']
            PracticeService.submit_answer(db, user_id, current_q['question_id'], correct_idx, 10, current_q['options'])
            print(f"  - Q{i+5} CORRECT.")
            current_q = PracticeService.get_next_question(db, user_id, category, topic, reset=False)
        
        print(f"Next Question (Q8) Difficulty: {current_q['difficulty']}")
        if current_q['difficulty'].lower() == 'medium':
            print("✅ SUCCESS: Difficulty moved to Medium after 3/4 Correct in window!")
        else:
            print(f"❌ FAILURE: Still at {current_q['difficulty']}. Needs >= 75% in last 4.")

        # 4. Verify Overall Accuracy (Cumulative)
        # 3 Correct out of 7 Attempts = 42.8%
        # Let's check the feedback of the last answer
        last_feedback = PracticeService.submit_answer(db, user_id, current_q['question_id'], current_q['_shuffled_correct_idx'], 10, current_q['options'])
        overall_acc = last_feedback['adaptive_feedback']['overall_accuracy']
        print(f"\n[Step 4] Verifying Cumulative Display")
        print(f"Overall Accuracy returned: {overall_acc}%")
        expected_acc = round((4/8)*100, 1) # 4 correct out of 8 attempts
        print(f"Expected Cumulative Accuracy: {expected_acc}%")
        
        if abs(overall_acc - expected_acc) < 0.5:
             print("✅ SUCCESS: Displayed accuracy is cumulative.")
        else:
             print("❌ FAILURE: Displayed accuracy does not match cumulative total.")
             
    except Exception as e:
        print(f"❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.query(QuestionAttempt).filter(QuestionAttempt.user_id == user_id).delete()
        db.query(UserAptitudeProgress).filter(UserAptitudeProgress.user_id == user_id).delete()
        db.commit()
        db.close()

if __name__ == "__main__":
    run_simulation()
