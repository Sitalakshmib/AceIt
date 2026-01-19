"""
Cleanup Aptitude Questions:
Deletes all existing questions and re-seeds only the initial 87 manually curated questions.
"""

import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database_postgres import SessionLocal
from models.analytics_sql import QuestionAttempt
from models.mock_test_sql import MockTest, MockTestAttempt, MockTestResponse
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from scripts.create_aptitude_tables import APTITUDE_QUESTIONS as INITIAL_77
from scripts.seed_comprehensive_questions import ADDITIONAL_QUESTIONS as INITIAL_ADDITIONAL_10

def cleanup():
    db = SessionLocal()
    try:
        print("Cleaning up aptitude module data...")
        
        # 1. Clear related tables first (FK order)
        print("Clearing mock test responses...")
        db.query(MockTestResponse).delete()
        
        print("Clearing mock test attempts...")
        db.query(MockTestAttempt).delete()
        
        print("Clearing mock tests...")
        db.query(MockTest).delete()
        
        print("Clearing individual question attempts...")
        db.query(QuestionAttempt).delete()
        
        print("Clearing user progress metrics...")
        db.query(UserAptitudeProgress).delete()
        
        # 2. Delete all questions
        print("Deleting all aptitude questions...")
        num_deleted = db.query(AptitudeQuestion).delete()
        print(f"Deleted {num_deleted} questions.")
        
        # 3. Re-seed the 87 questions
        total_initial = INITIAL_77 + INITIAL_ADDITIONAL_10
        print(f"Re-seeding {len(total_initial)} initial manual questions...")
        
        for q_data in total_initial:
            new_q = AptitudeQuestion(**q_data)
            db.add(new_q)
            
        db.commit()
        print("Cleanup complete. Database now contains only the initial questions.")
        
    except Exception as e:
        db.rollback()
        print(f"Error during cleanup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    cleanup()
