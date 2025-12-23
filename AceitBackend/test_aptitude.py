import requests
import json

# Test getting topics
print("Testing /aptitude/topics endpoint...")
response = requests.get("http://localhost:8000/aptitude/topics")
print("Topics:", response.json())

# Test getting questions without user ID
print("\nTesting /aptitude/questions endpoint (random questions)...")
response = requests.get("http://localhost:8000/aptitude/questions?count=3")
questions = response.json()
print("Sample questions:")
for q in questions[:2]:  # Show first 2 questions
    print(f"  - ID: {q['id']}, Topic: {q['topic']}, Difficulty: {q['difficulty']}")

# Test getting questions for specific topic
print("\nTesting /aptitude/questions endpoint (percentage topic)...")
response = requests.get("http://localhost:8000/aptitude/questions?topic=percentage&count=2")
questions = response.json()
print("Percentage questions:")
for q in questions:
    print(f"  - ID: {q['id']}, Difficulty: {q['difficulty']}")
    print(f"    Question: {q['question']}")
    print(f"    Correct answer index: {q['correct']}")

# Test submitting answers
print("\nTesting /aptitude/submit endpoint...")
payload = {
    "user_id": "user123",
    "answers": {
        questions[0]["id"]: questions[0]["correct"],  # Correct answer
        questions[1]["id"]: 0  # Incorrect answer (always choosing first option)
    },
    "topic": "percentage"
}

response = requests.post("http://localhost:8000/aptitude/submit", json=payload)
print("Submit response:", response.json())

# Test getting user proficiency
print("\nTesting /aptitude/proficiency endpoint...")
response = requests.get("http://localhost:8000/aptitude/proficiency/user123")
proficiency = response.json()
print("User proficiency:", json.dumps(proficiency, indent=2))

# Test getting questions with user ID (adaptive)
print("\nTesting /aptitude/questions endpoint (adaptive for user123)...")
response = requests.get("http://localhost:8000/aptitude/questions?user_id=user123&topic=percentage&count=2")
questions = response.json()
print("Adaptive questions for user123:")
for q in questions:
    print(f"  - ID: {q['id']}, Difficulty: {q['difficulty']}")
    print(f"    Question: {q['question']}")