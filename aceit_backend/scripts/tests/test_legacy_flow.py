from fastapi.testclient import TestClient
from main import app
from dotenv import load_dotenv

load_dotenv()

client = TestClient(app)

def test_legacy_flow():
    print("🚀 Testing LEGACY Frontend Flow...")
    
    # 1. Start Interview (Original Payload - No Resume/JD)
    print("\n[1] Starting Interview (Legacy Payload)...")
    start_payload = {
        "user_id": "legacy_user",
        "interview_type": "technical",
        "tech_stack": "python"
    }
    
    resp = client.post("/interview/start", json=start_payload)
    if resp.status_code != 200:
        print(f"❌ Failed to start: {resp.text}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    print(f"✅ Started. Session ID: {session_id}")
    print(f"   Question: {data['current_question']['text']}")
    print(f"   Topic: {data['current_question']['topic']}")
    
    # 2. Analyze Response (Original Payload)
    print("\n[2] Analyzing Response (Legacy Payload)...")
    analyze_payload = {
        "session_id": session_id,
        "question_id": data["current_question"]["id"],
        "user_response_text": "Python is a dynamic language."
    }
    
    resp = client.post("/interview/analyze", json=analyze_payload)
    
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
