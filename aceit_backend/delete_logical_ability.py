
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.aptitude_sql import AptitudeQuestion
from models.analytics_sql import QuestionAttempt
from models.mock_test_sql import MockTestResponse
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def delete_category(category_name):
    # Get IDs first
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.category == category_name).all()
    q_ids = [q.id for q in questions]
    count = len(q_ids)
    
    print(f"[{category_name}] Found {count} questions.")
    
    if count > 0:
        # Delete referencing QuestionAttempts
        deleted_attempts = db.query(QuestionAttempt)\
            .filter(QuestionAttempt.question_id.in_(q_ids))\
            .delete(synchronize_session=False)
        print(f"[{category_name}] Deleted {deleted_attempts} practice attempts.")
        
        # Delete referencing MockTestResponses
        deleted_responses = db.query(MockTestResponse)\
            .filter(MockTestResponse.question_id.in_(q_ids))\
            .delete(synchronize_session=False)
        print(f"[{category_name}] Deleted {deleted_responses} mock test responses.")

        # Delete Questions
        deleted_questions = db.query(AptitudeQuestion)\
            .filter(AptitudeQuestion.category == category_name)\
            .delete(synchronize_session=False)
            
        db.commit()
        print(f"[{category_name}] Deleted {deleted_questions} questions.")
        
        # Verify
        new_count = db.query(AptitudeQuestion).filter(AptitudeQuestion.category == category_name).count()
        print(f"[{category_name}] Remaining count: {new_count}")
    else:
        print(f"[{category_name}] No questions to delete.")

if __name__ == "__main__":
    print("--- Deleting Logical Ability Questions ---")
    delete_category("Logical Ability")
    delete_category("Logical Reasoning") # Also check/delete this if needed
    print("--- Check Complete ---")
