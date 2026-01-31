import json
import os

# In-memory database simulation
questions_data = [
    {
        "id": "code1",
        "title": "Fibonacci Sequence",
        "description": "Write a function to return the nth Fibonacci number.",
        "difficulty": "Easy",
        "examples": [],
        "starter_code": "def fibonacci(n):\n    pass",
        "test_cases": [1, 2, 3]
    },
    {
        "id": "code2",
        "title": "Palindrome Check",
        "description": "Check if a string is a palindrome.",
        "difficulty": "Easy",
        "examples": [],
        "starter_code": "def is_palindrome(s):\n    pass",
        "test_cases": ["aba"]
    }
]

PROGRESS_FILE = "progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []

def save_progress():
    try:
        with open(PROGRESS_FILE, "w") as f:
            json.dump(progress_data, f, indent=2, default=str)
    except Exception as e:
        print(f"Error saving progress: {e}")

progress_data = load_progress()
