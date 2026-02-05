from sqlalchemy.orm import Session
from database_postgres import SessionLocal
from services.mock_test_service import MockTestService
import traceback

def debug_results(attempt_id: str):
    db = SessionLocal()
    try:
        print(f"Debugging attempt: {attempt_id}")
        results = MockTestService.get_test_results(db, attempt_id)
        print("Success! Results:")
        print(results)
    except Exception as e:
        print("Caught Exception:")
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    # Use the attempt ID from the user's log
    debug_results("650ded47-45db-469c-83db-6471fc2e526a")
