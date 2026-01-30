import requests
import time

URL = "http://localhost:8001/interview/analyze"
SESSION_ID = "test_session_debug"

# create session first
requests.post("http://localhost:8001/interview/start", json={"user_id": "debug", "interview_type": "hr"})

print("⏱️  Sending Analyze Request...")
start = time.time()
try:
    resp = requests.post(URL, json={
        "session_id": "debug_123456", # Might 404 if session logic is strict, let's fix
        "question_id": "hr_e_1",
        "user_response_text": "I am a passionate developer with experience in Python.",
        "video_metrics": {"face_visible_pct": 0.9},
        "speech_metrics": {"audio_duration_seconds": 5}
    })
    elapsed = time.time() - start
    print(f"✅ Response Time: {elapsed:.2f}s")
    print(f"Status: {resp.status_code}")
    if resp.status_code == 200:
        print("Feedback:", resp.json().get("feedback"))
    else:
        print("Error:", resp.text)
except Exception as e:
    print(f"❌ Error: {e}")
