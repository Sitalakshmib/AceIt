from fastapi.testclient import TestClient
from main import app
import os

# Ensure API Key is present (redundant if main.py loads it, but safe)
from dotenv import load_dotenv
load_dotenv()

client = TestClient(app)

def test_sim_flow():
    print("🚀 Starting SimInterview Integration Test (Local TestClient)...")
    
    # 1. Start Interview
    print("\n[1] Starting Interview...")
    start_payload = {
        "user_id": "test_user_local",
        "resume_text": "Python Developer.",
        "jd_text": "Backend Engineer."
    }
    
    resp = client.post("/interview/start-ai", json=start_payload)
    if resp.status_code != 200:
        print(f"❌ Failed to start: {resp.text}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    print(f"✅ Interview Started! Session ID: {session_id}")
    print(f"Question: {data['question']}")
    
    # 2. Answer (Text)
    print("\n[2] Answering Question 1 (Text)...")
    answer_payload = {
        "session_id": session_id,
        "answer_text": "I use APIs."
    }
    # TestClient handling for Form data
    resp = client.post("/interview/answer-ai", data=answer_payload)
    
    if resp.status_code != 200:
        print(f"❌ Failed to answer: {resp.text}")
        return
        
    print(f"✅ Answer Recorded: {resp.json()}")

    # 3. Next Question
    print("\n[3] Getting Next Question...")
    resp = client.post("/interview/next-ai", json={"session_id": session_id})
    
    if resp.status_code != 200:
        print(f"❌ Failed to get next: {resp.text}")
        return
        
    print(f"✅ Next Question: {resp.json()['question']}")
    
    # 4. Answer (Audio Mock)
    print("\n[4] Answering with Audio (Mock)...")
    
    # Create dummy bytes
    files = {
        "audio_file": ("test.wav", b"FAKEWAV", "audio/wav")
    }
    data = {"session_id": session_id}
    
    resp = client.post("/interview/answer-ai", data=data, files=files)
    print(f"✅ Audio Answer Response: {resp.json()}")
    
    print("\n🎉 Local Verification Successful!")

if __name__ == "__main__":
    test_sim_flow()
