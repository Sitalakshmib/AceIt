import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.interview import generate_next_question_logic, QUESTION_BANK

# Mock data
mock_q = {"id": "test_1", "text": "test"}
mock_session = {
    "type": "hr",
    "topic": "general",
    "difficulty_level": "medium",
    "history": [] # No history yet
}

def test_transition(score, current_diff, expected_diff):
    print(f"\n--- Testing Score: {score} | Current: {current_diff} ---")
    mock_session["difficulty_level"] = current_diff
    analysis = {"overall_score": score}
    
    next_q = generate_next_question_logic(mock_q, analysis, mock_session)
    
    if not next_q:
        print("❌ FAIL: No question returned")
        return

    # Check which bucket the question came from
    # We find the new diff from the session object which is updated in place
    new_diff = mock_session["difficulty_level"]
    print(f"Context: {next_q.get('ai_context')}")
    print(f"Result Level: {new_diff}")
    
    if new_diff == expected_diff:
        print("✅ PASS")
    else:
        print(f"❌ FAIL (Expected {expected_diff}, got {new_diff})")

# 1. High Score (>75) -> Increase
test_transition(80, "easy", "medium")
test_transition(85, "medium", "hard")
test_transition(90, "hard", "hard") # Cap at hard

# 2. Mid Score (50-74) -> Maintain
test_transition(60, "easy", "easy")
test_transition(70, "medium", "medium")
test_transition(74, "hard", "hard")

# 3. Low Score (<50) -> Decrease
test_transition(40, "hard", "medium")
test_transition(30, "medium", "easy")
test_transition(20, "easy", "easy") # Cap at easy
