import requests
import json

url = "http://localhost:8001/interview/start"

payloads = [
    {"user_id": "test_hr", "interview_type": "hr"},
    {"user_id": "test_tech", "interview_type": "technical", "tech_stack": "python"},
    {"user_id": "test_bad", "interview_type": "technical", "tech_stack": "java"} # Should fallback or fail
]

for p in payloads:
    print(f"Testing payload: {p}")
    try:
        res = requests.post(url, json=p)
        print(f"Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Error: {res.text}")
        else:
            print("Success")
    except Exception as e:
        print(f"Request failed: {e}")
    print("-" * 20)
