import requests
import json

BASE_URL = "http://localhost:8000"

def test_legacy_flow():
    print("🚀 Testing LEGACY Frontend Flow (Network)...")
    
    # 1. Start Interview (Original Payload)
    print("\n[1] Starting Interview (Legacy Payload)...")
    start_payload = {
        "user_id": "legacy_user_net",
        "interview_type": "technical",
        "tech_stack": "python"
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/interview/start", json=start_payload)
        
        if resp.status_code != 200:
            print(f"❌ Failed to start: {resp.text}")
            return
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    print(f"✅ Started. Session ID: {session_id}")
    print(f"   Question: {data['current_question']['text']}")
    
    # 2. Analyze Response
    print("\n[2] Analyzing Response (Legacy Payload)...")
    analyze_payload = {
        "session_id": session_id,
        "question_id": data["current_question"]["id"],
        "user_response_text": "Python uses indentation."
    }
    
    resp = requests.post(f"{BASE_URL}/interview/analyze", json=analyze_payload)
    
    if resp.status_code != 200:
        print(f"❌ Failed to analyze: {resp.text}")
        return
        
    data = resp.json()
    print(f"✅ Analysis Complete.")
    print(f"   Next Question: {data['current_question']['text']}")
    print(f"   Score: {data['score']}")
    
    print("\n🎉 Legacy Flow Verified!")

if __name__ == "__main__":
    test_legacy_flow()
