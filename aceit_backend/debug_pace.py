from database_postgres import SessionLocal
from models.mock_test_sql import MockTestAttempt, MockTestResponse
from models.user_sql import User
from models.aptitude_sql import AptitudeQuestion
from sqlalchemy import func

def debug_pace_data():
    db = SessionLocal()
    try:
        # Get the latest 5 completed attempts
        attempts = db.query(MockTestAttempt).filter(
            MockTestAttempt.status == "completed"
        ).order_by(MockTestAttempt.completed_at.desc()).limit(5).all()
        
        print(f"{'Attempt ID':<40} | {'Time (s)':<10} | {'Total Qs':<10} | {'Correct':<10}")
        print("-" * 80)
        
        for a in attempts:
            # Count real responses for this attempt
            resp_count = db.query(func.count(MockTestResponse.id)).filter(
                MockTestResponse.attempt_id == a.id
            ).scalar()
            
            print(f"{a.id:<40} | {a.time_taken_seconds:<10} | {resp_count:<10} (out of {a.total_questions}) | {a.score:<10}")
            
            # Check individual response times
            responses = db.query(MockTestResponse).filter(MockTestResponse.attempt_id == a.id).all()
            total_sum = sum(r.time_spent_seconds or 0 for r in responses)
            print(f"  > Sum of response times: {total_sum}s")
            
            if resp_count > 0:
                avg_time = a.time_taken_seconds / resp_count
                pace = 60 / avg_time if avg_time > 0 else 0
                print(f"  > Calculated Avg Time: {avg_time:.2f}s/q | Pace: {pace:.2f}x")
            print("-" * 80)
            
    finally:
        db.close()

if __name__ == "__main__":
    debug_pace_data()
