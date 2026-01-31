import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from database_postgres import SessionLocal
from services.mock_test_service import MockTestService
from models.aptitude_sql import AptitudeQuestion

def verify_elite_mock_test():
    db = SessionLocal()
    try:
        print("Generating Elite Mock Test...")
        mock_test = MockTestService.generate_full_length_test(db)
        
        print(f"\n--- Verification Report ---")
        print(f"Test ID: {mock_test.id}")
        print(f"Total Questions: {mock_test.total_questions}")
        print(f"Duration: {mock_test.duration_minutes} minutes")
        
        # 1. Verify Count
        if mock_test.total_questions != 60:
            print(f"❌ FAILED: Expected 60 questions, got {mock_test.total_questions}")
        else:
            print(f"✅ PASSED: Total questions count is 60")
            
        # 2. Verify Difficulty Split
        q_ids = mock_test.question_ids
        questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(q_ids)).all()
        q_map = {q.id: q for q in questions}
        
        counts = {"easy": 0, "medium": 0, "hard": 0}
        topics = set()
        categories = set()
        
        for qid in q_ids:
            q = q_map.get(qid)
            if q:
                diff = q.difficulty.lower() if q.difficulty else "medium"
                counts[diff] = counts.get(diff, 0) + 1
                topics.add(q.topic)
                categories.add(q.category)
        
        print(f"\nDifficulty Breakdown:")
        print(f"  Easy:   {counts['easy']} (Target: 12)")
        print(f"  Medium: {counts['medium']} (Target: 24)")
        print(f"  Hard:   {counts['hard']} (Target: 24)")
        
        if counts['easy'] == 12 and counts['medium'] == 24 and counts['hard'] == 24:
             print(f"✅ PASSED: Difficulty split matches 20/40/40 exactly (12/24/24)")
        else:
             print(f"⚠️ WARNING: Difficulty split deviation (likely due to insufficient pool)")

        # 3. Verify Diversity
        print(f"\nDiversity Check:")
        print(f"  Unique Topics Covered: {len(topics)}")
        print(f"  Categories Covered: {len(categories)}")
        print(f"  Example Topics: {list(topics)[:5]}...")
        
        if len(topics) > 10:
             print(f"✅ PASSED: High topic diversity detected")
        else:
             print(f"⚠️ WARNING: Low topic diversity")

    except Exception as e:
        print(f"❌ CRITICAL ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    verify_elite_mock_test()
