
import sys
import os
import random
from unittest.mock import MagicMock

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), "aceit_backend"))

from services.adaptive_engine import AdaptiveEngine

USER_ID = "test_user"
TOPIC = "test_topic"

# Mock DB Session
db = MagicMock()

# Global state for attempts
attempts_history = []

class MockAttempt:
    def __init__(self, is_correct, difficulty):
        self.is_correct = is_correct
        self.difficulty_at_attempt = difficulty
        self.user_id = USER_ID
        self.topic = TOPIC
        self.context = "practice"
        self.attempted_at = 1 # Dummy sort key

def record_attempts(count, is_correct, difficulty):
    for i in range(count):
        attempts_history.append(MockAttempt(is_correct, difficulty))
    print(f"Recorded {count} {difficulty} attempts (Correct: {is_correct})")

def setup_mocks():
    # Mock for count()
    # It seems SQLAlchemy chaining is complex to mock exactly, 
    # but AdaptiveEngine calls: db.query(QuestionAttempt).filter(...).count()
    # and .all()
    
    # We can mock the return value of filter() to return a mock query object
    query_mock = MagicMock()
    
    def filter_side_effect(*args, **kwargs):
        return query_mock
        
    db.query.return_value = query_mock
    query_mock.filter.side_effect = filter_side_effect
    query_mock.order_by.return_value = query_mock
    query_mock.limit.return_value = query_mock
    
    # Mock count()
    query_mock.count.side_effect = lambda: len(attempts_history)
    
    # Mock all() for limit(4)
    # The code calls limit(4).all() to get last 4.
    # We should return the last 4 from attempts_history reversed (since order_by desc)
    def all_side_effect():
        # logic to guess if it is the attempts query
        # Just return last 4 reversed
        return list(reversed(attempts_history[-4:]))
        
    query_mock.all.side_effect = all_side_effect

setup_mocks()

def check_next_difficulty(current):
    # In strict testing, we'd need to ensure the query arguments match, 
    # but for this verification, we assume the engine makes the correct queries 
    # and we provide the state via the side_effects.
    
    next_diff = AdaptiveEngine.calculate_next_difficulty(db, USER_ID, TOPIC, current)
    print(f"Total Attempts: {len(attempts_history)} | Current: {current} -> Next: {next_diff}")
    return next_diff

print("--- TEST START ---")

# 1. Start: 0 attempts. Expect Easy.
diff = check_next_difficulty("easy")
assert diff == "easy"

# 2. Submit 3 Correct (Total 3). Should stay Easy (not batch end).
record_attempts(3, True, "easy")
diff = check_next_difficulty("easy")
assert diff == "easy"

# 3. Submit 1 Correct (Total 4). Accuracy 100%. Should go Medium.
record_attempts(1, True, "easy")
diff = check_next_difficulty("easy")
assert diff == "medium"

# 4. Start Next Batch. Submit 1 Wrong (Total 5). Should stay Medium.
record_attempts(1, False, "medium")
diff = check_next_difficulty("medium")
assert diff == "medium"

# 5. Submit 3 more Wrong (Total 8). Last 4 are ALL Wrong (0%). Should go Easy.
record_attempts(3, False, "medium")
diff = check_next_difficulty("medium")
assert diff == "easy"

# 6. Submit 4 Mixed (2 Correct, 2 Wrong). Accuracy 50%. Should Stay Easy.
# Wait, if we are at Easy, 50% means Stay Easy.
# Last call returned "easy". We simulate "user continues at easy".
record_attempts(2, True, "easy")
record_attempts(2, False, "easy")
# Total is 12 attempts.
diff = check_next_difficulty("easy")
assert diff == "easy"

print("--- TEST PASSED ---")
