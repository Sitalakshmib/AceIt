import os
import sys
import traceback
from fastapi.testclient import TestClient

# Add current dir to path
sys.path.append(os.getcwd())

try:
    from main import app
    from database_postgres import SessionLocal
    from models.mock_test_sql import MockTestAttempt
except Exception as e:
    print(f"Import failed: {e}")
    sys.exit(1)

client = TestClient(app)

def debug_dashboard():
    print("\n--- Debugging /analytics/dashboard/{user_id} ---")
    user_id = "2da06b5a-35cf-422c-8fa0-d6e60cc42cc4" # From user screenshot
    try:
        response = client.get(f"/analytics/dashboard/{user_id}")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 500:
            print("Internal Server Error details:")
            print(response.json())
        else:
            print("Response success!")
            # print(response.json())
    except Exception:
        print("Exception occurred during request:")
        traceback.print_exc()

def debug_categories():
    print("\n--- Debugging /aptitude/categories ---")
    try:
        response = client.get("/aptitude/categories")
        print(f"Status Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
        else:
            print("Categories fetched successfully!")
    except Exception:
        print("Exception occurred during request:")
        traceback.print_exc()

def check_nulls():
    print("\n--- Checking for potential NULL values in database ---")
    db = SessionLocal()
    try:
        # Check MockTestAttempt
        null_completed = db.query(MockTestAttempt).filter(MockTestAttempt.status == "completed", MockTestAttempt.completed_at == None).count()
        print(f"Completed MockTestAttempts with NULL completed_at: {null_completed}")
        
        # Check for other potential issues
        from models.aptitude_sql import UserAptitudeProgress
        null_time = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.total_time_spent_seconds == None).count()
        print(f"UserAptitudeProgress with NULL total_time_spent_seconds: {null_time}")
        
        null_streak = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.streak == None).count()
        print(f"UserAptitudeProgress with NULL streak: {null_streak}")

        null_accuracy = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.overall_accuracy == None).count()
        print(f"UserAptitudeProgress with NULL overall_accuracy: {null_accuracy}")
        
    except Exception as e:
        print(f"DB Check failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_nulls()
    debug_categories()
    debug_dashboard()
