import json
import os
import requests
import uuid
from datetime import datetime

# Configuration
API_URL = "http://localhost:8000"
USER_ID = "test_user_persistence_verify"
SESSIONS_FILE = "d:/AceIt/aceit_backend/data/interview_sessions.json"

def create_dummy_session():
    """Create a dummy interview session directly in the JSON file"""
    print(f"1. Creating dummy session for user: {USER_ID}")
    
    session_id = str(uuid.uuid4())
    session_data = {
        session_id: {
            "id": session_id,
            "user_id": USER_ID,
            "interview_type": "technical",
            "topic": "python",
            "start_time": datetime.now().isoformat(),
            "status": "completed",
            "scores": [85, 90, 75],
            "qa_pairs": [
                {"question": "Q1", "answer": "A1", "score": 85},
                {"question": "Q2", "answer": "A2", "score": 90},
                {"question": "Q3", "answer": "A3", "score": 75}
            ],
            "weak_areas": ["Decorators"]
        }
    }
    
    # Load existing or create new
    if os.path.exists(SESSIONS_FILE):
        with open(SESSIONS_FILE, 'r') as f:
            existing = json.load(f)
        existing.update(session_data)
        final_data = existing
    else:
        final_data = session_data
        
    # Write to file
    with open(SESSIONS_FILE, 'w') as f:
        json.dump(final_data, f, indent=2)
        
    print(f"   Saved session to {SESSIONS_FILE}")
    return session_id

def check_analytics():
    """Call the analytics endpoint and verify data is returned"""
    print(f"2. Check analytics for user: {USER_ID}")
    try:
        response = requests.get(f"{API_URL}/interview/analytics/{USER_ID}")
        if response.status_code == 200:
            data = response.data if hasattr(response, 'data') else response.json()
            print("   Analytics Response Received:")
            print(f"   - Has Data: {data.get('has_data')}")
            print(f"   - Technical Sessions: {data.get('technical', {}).get('sessions_count')}")
            print(f"   - Average Score: {data.get('technical', {}).get('average_score')}")
            
            if data.get('has_data') and data.get('technical', {}).get('sessions_count') >= 1:
                return True
            else:
                print("   [FAIL] Analytics returned but no data found (expected from file)")
                return False
        else:
            print(f"   [FAIL] API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"   [FAIL] Request failed: {e}")
        return False

if __name__ == "__main__":
    # Ensure directory exists
    os.makedirs(os.path.dirname(SESSIONS_FILE), exist_ok=True)
    
    print("--- STARTING VERIFICATION ---")
    create_dummy_session()
    
    # Note: Since the backend loads the file ON STARTUP, pushing to the file directly 
    # might not be picked up immediately if the backend only reads once.
    # However, my implementation of `_load_sessions` is called in `__init__`.
    # But `SimVoiceInterviewer` is a singleton created at module level or dependency.
    # If the backend is ALREADY running, it won't reload the file unless I restart it 
    # or if I modify the code to reload on request (which I didn't).
    
    print("\n   NOTE: If the backend is already running, it might not see this file change instantly")
    print("   unless the singleton is re-instantiated or I implemented a reload mechanism.")
    print("   Let's check if it picks it up (if the singleton initialization happens per request or if I restart).")
    
    # Actually, fastAPI dependency `get_engine` uses a global variable `_engine`.
    # It is initialized once.
    # So writing to the file manually WONT work for a running server unless I restart it.
    
    # BUT, since I modified the code, the dev server (uvicorn) should auto-reload!
    # So by the time I run this, the server should have reloaded and picked up the changes.
    
    import time
    time.sleep(2) # Give a moment
    
    success = check_analytics()
    
    if success:
        print("\n[SUCCESS] Verification Passed! Persistence is working.")
    else:
        print("\n[WARNING] Verification checks failed or data not picked up.")
        print("This might be because the server didn't reload or the user ID didn't match.")
