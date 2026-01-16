import requests
import json
import time

BASE_URL = "http://localhost:8001/interview"
USER_ID = f"test_gemini_{int(time.time())}"

def test_semantic_evaluation():
    print(f"🚀 Testing Semantic Evaluation Integration for User: {USER_ID}")
    
    # 1. Start Interview
    print("\n[1] Starting Interview...")
    try:
        resp = requests.post(f"{BASE_URL}/start", json={"user_id": USER_ID, "interview_type": "hr"})
        if resp.status_code != 200:
            print(f"❌ Start Failed: {resp.text}")
            return
        
        data = resp.json()
        session_id = data["session_id"]
        current_q = data["current_question"]
        print(f"✅ Session Started: {session_id}")
        print(f"   Question: {current_q['text']}")
        
        # 2. Analyze Answer
        print("\n[2] Sending Answer for Semantic Analysis...")
        answer_text = "I believe my greatest strength is my ability to learn quickly. For example, in my last project, I learned React in two days to build the frontend."
        
        payload = {
            "session_id": session_id,
            "question_id": current_q["id"],
            "user_response_text": answer_text
        }
        
        start_time = time.time()
        resp = requests.post(f"{BASE_URL}/analyze", json=payload)
        duration = time.time() - start_time
        
        if resp.status_code != 200:
             print(f"❌ Analysis Failed: {resp.text}")
             return

        result = resp.json()
        print(f"✅ Analysis Received in {duration:.2f}s")
        
        scores = result.get("scores", {})
        print("\n--- Semantic Analysis Results ---")
        print(f"Overall Score: {result.get('score')}")
        print(f"Confidence: {scores.get('confidence')}")
        print(f"Clarity: {scores.get('clarity')}")
        print(f"Quality/Relevance: {scores.get('relevance')}")
        print(f"Strengths: {scores.get('strengths')}")
        print(f"Improvements: {scores.get('improvements')}")
        print(f"Feedback: {result.get('feedback')}")
        
        if "ai_next_question" in scores:
            print(f"AI Suggested Next Question: {scores['ai_next_question']}")
            
        # Verify Next Question Override
        next_q_obj = result.get("current_question", {})
        print(f"\nNext Question for UI: {next_q_obj.get('text')}")
        print(f"Next Question ID: {next_q_obj.get('id')}")
        
        if next_q_obj.get("id", "").startswith("ai_gen_"):
            print("✅ Verification Successful: Gemini Next Question was used (ID starts with ai_gen_).")
        else:
            print(f"⚠️ Verification Warning: Next question ID {next_q_obj.get('id')} does not appear to be AI generated via override.")

        if scores.get("confidence") is not None and scores.get("overall_score") > 0:
            print("✅ Verification Successful: Received semantic scores from Gemini.")
        else:
            print("\n⚠️ Verification Warning: Scores seem empty or default. Check backend logs for Gemini errors.")

        # Verify Analysis Engine Field
        engine = result.get("analysis_engine")
        print(f"\nAnalysis Engine: {engine}")
        if engine == "gemini":
            print("✅ Verification Successful: 'analysis_engine' field is present and set to 'gemini'.")
        else:
            print(f"⚠️ Verification Warning: 'analysis_engine' is '{engine}'. Expected 'gemini'.")

    except Exception as e:
        print(f"❌ Test Exception: {e}")

if __name__ == "__main__":
    test_semantic_evaluation()
