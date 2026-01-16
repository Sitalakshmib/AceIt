
import os
import sys

# Add parent directory to path to import services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.ai_interviewer import AIInterviewer

def test_ai_interviewer():
    print("Testing AI Interviewer...")
    interviewer = AIInterviewer()
    
    # Test 1: Generate First Question
    print("\n--- Test 1: Generate First Question ---")
    try:
        q1 = interviewer.generate_first_question("technical", "python", "easy")
        print("Result:", q1)
        if "next_question" in q1:
            print("✅ First question generated structure is correct.")
        else:
            print("❌ First question generated structure is INCORRECT.")
    except Exception as e:
        print(f"❌ Error generating first question: {e}")

    # Test 2: Analyze and Generate Next
    print("\n--- Test 2: Analyze and Generate Next ---")
    history = [{"question": {"text": "What is Python?"}, "answer": "It is a programming language."}]
    try:
        q2 = interviewer.analyze_and_generate_next(history, "It is dynamically typed.", "technical", "python", "easy")
        print("Result:", q2)
        if "next_question" in q2 and "score" in q2:
             print("✅ Next question generated structure is correct.")
        else:
             print("❌ Next question generated structure is INCORRECT.")

    except Exception as e:
        print(f"❌ Error generating next question: {e}")

if __name__ == "__main__":
    # Mock API Key if not present to test logic flow (it will use fallback or fail gracefully)
    if "GEMINI_API_KEY" not in os.environ:
        print("⚠️ No GEMINI_API_KEY found. Expecting fallback behaviors or errors from Google API.")
    
    test_ai_interviewer()
