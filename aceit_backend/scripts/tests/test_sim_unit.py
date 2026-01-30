from services.sim_interview_engine import SimInterviewEngine
from dotenv import load_dotenv
import os

# Load env for GEMINI_API_KEY
load_dotenv()

def test_engine():
    print("🚀 Starting SimInterviewEngine UNIT Test...")
    
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ SKIPPING: GEMINI_API_KEY not found in env.")
        return

    engine = SimInterviewEngine()
    
    # 1. Start
    print("\n[1] Starting Interview...")
    res = engine.start_interview("user_unit", "Python Dev", "Backend Role")
    session_id = res["session_id"]
    print(f"✅ Started. Q: {res['question']}")
    
    # 2. Answer
    print("\n[2] Processing Answer...")
    engine.process_answer(session_id, "I love coding in Python.")
    print("✅ Answer recorded.")
    
    # 3. Next Question
    print("\n[3] Generating Next Question...")
    next_q = engine.generate_next_question(session_id)
    print(f"✅ Next Q: {next_q['question']}")
    print(f"   Score: {next_q['score']}")
    
    print("\n🎉 Unit Test Passed!")

if __name__ == "__main__":
    test_engine()
