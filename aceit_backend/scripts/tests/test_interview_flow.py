import requests
import json

BASE_URL = "http://localhost:8001/interview"
USER_ID = "test_user_123"

def run_test():
    print("🚀 Starting Interview Module Test...")
    
    # 1. Start Interview
    print("\n[1] Starting Interview...")
    resp = requests.post(f"{BASE_URL}/start", json={"user_id": USER_ID, "interview_type": "hr"})
    if resp.status_code != 200:
        print(f"❌ Start Failed: {resp.text}")
        return
    
    data = resp.json()
    session_id = data["session_id"]
    current_q = data["current_question"]
    print(f"✅ Session Started: {session_id}")
    print(f"   First Question: {current_q['text']}")
    print(f"   Keywords Required: {current_q.get('keywords')}")

    # 2. Submit GOOD Answer
    print("\n[2] Submitting GOOD Answer...")
    # Construct answer with required keywords
    keywords = current_q.get("keywords", [])
    good_answer = f"I am very passionate about this role. My background in {keywords[0] if keywords else 'tech'} has prepared me well. I believe in {keywords[1] if len(keywords)>1 else 'learning'} and teamwork. I have graduated recently."
    # Make it long enough
    good_answer += " " * 50 # Padding to ensure length score isn't 0 if logic counts chars/words
    good_answer += " I am definitely sure about my skills."

    resp = requests.post(f"{BASE_URL}/analyze", json={
        "session_id": session_id,
        "question_id": current_q["id"],
        "user_response_text": good_answer
    })
    data = resp.json()
    print(f"   Feedback: {data['feedback']}")
    print(f"   Score: {data['score']}")
    
    if data['score'] > 60:
        print("✅ Correctly scored high for good answer.")
    else:
        print("❌ Score too low for good answer.")

    current_q = data["current_question"]
    print(f"   Next Question: {current_q.get('text', 'None')}")

    # 3. Submit BAD Answer
    print("\n[3] Submitting BAD Answer...")
    bad_answer = "I don't know. Maybe."
    
    resp = requests.post(f"{BASE_URL}/analyze", json={
        "session_id": session_id,
        "question_id": current_q["id"] if current_q else "none",
        "user_response_text": bad_answer
    })
    data = resp.json()
    print(f"   Feedback: {data['feedback']}")
    print(f"   Score: {data['score']}")
    
    if data['score'] < 50:
        print("✅ Correctly scored low for bad answer.")
    else:
        print("❌ Score too high for bad answer.")

    print("\n✅ Test Complete!")

if __name__ == "__main__":
    run_test()
