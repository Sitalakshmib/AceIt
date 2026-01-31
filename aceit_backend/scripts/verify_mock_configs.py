
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.mock_test_service import MockTestService
from models.aptitude_sql import AptitudeQuestion
from models.mock_test_sql import MockTest, Base

load_dotenv()

def get_session():
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(bind=engine)
    return SessionLocal()

def verify_configs():
    db = get_session()
    try:
        print("--- Verifying Mock Test Configurations ---")
        
        # 1. Topic Test (Expecting 20)
        # We need a topic with questions. Let's find one.
        topic = db.query(AptitudeQuestion.topic).first()[0]
        category = db.query(AptitudeQuestion.category).filter(AptitudeQuestion.topic == topic).first()[0]
        
        print(f"Testing Topic Test for: {topic} ({category})")
        topic_test = MockTestService.generate_topic_test(db, category, topic)
        print(f"Topic Test: {topic_test.total_questions} questions (Expected 20)")
        print(f"Duration: {topic_test.duration_minutes} mins (Expected 20)")
        
        if topic_test.total_questions != 20:
             print("❌ Topic Test Failed!")
        else:
             print("✅ Topic Test Passed")

        # 2. Section Test (Expecting 30)
        print(f"\nTesting Section Test for: {category}")
        section_test = MockTestService.generate_section_test(db, category)
        print(f"Section Test: {section_test.total_questions} questions (Expected 30)")
        print(f"Duration: {section_test.duration_minutes} mins (Expected 30)")
        
        if section_test.total_questions != 30:
             print("❌ Section Test Failed!")
        else:
             print("✅ Section Test Passed")

        # 3. Full Length (Expecting 100)
        print(f"\nTesting Full Length Test")
        full_test = MockTestService.generate_full_length_test(db)
        print(f"Full Test: {full_test.total_questions} questions (Expected 100)")
        print(f"Duration: {full_test.duration_minutes} mins (Expected 90)")
        
        if full_test.total_questions != 100:
             print("❌ Full Test Failed!")
        else:
             print("✅ Full Test Passed")
             
    except Exception as e:
        print(f"❌ Error: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_configs()
