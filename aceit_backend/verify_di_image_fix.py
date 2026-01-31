import requests
import json
import sys

BASE_URL = "http://localhost:8000"

def verify_di_images():
    # 1. Generate a user ID (dummy)
    user_id = "guest_user"
    
    # 2. Generate a Topic Wise Mock Test for Data Interpretation (Pie Chart is known to have images)
    print("Generating Mock Test...")
    payload = {
        "test_type": "topic_wise",
        "category": "Data Interpretation",
        "topic": "Pie Chart" # Matches the DB query result
    }
    
    try:
        response = requests.post(f"{BASE_URL}/mock-tests/generate", json=payload)
        response.raise_for_status()
        test_data = response.json()
        print(f"Test generated: {test_data['test_id']}")
        test_id = test_data['test_id']
    except Exception as e:
        print(f"Failed to generate test: {e}")
        return

    # 3. Start the test
    print("Starting Test...")
    try:
        start_payload = {"user_id": user_id}
        start_response = requests.post(f"{BASE_URL}/mock-tests/{test_id}/start", json=start_payload)
        start_response.raise_for_status()
        start_data = start_response.json()
        
        questions = start_data.get("questions", [])
        print(f"Received {len(questions)} questions.")
        
        # 4. Verify image_url is present in questions
        found_image = False
        for q in questions:
            if "image_url" in q:
                print(f"Question {q['id']} has 'image_url' key.")
                if q['image_url']:
                    print(f"  -> URL: {q['image_url']}")
                    found_image = True
                else:
                    print("  -> URL is None/Empty (might be expected for non-graph Qs, but DI should have it)")
            else:
                print(f"ERROR: Question {q['id']} uses DI topic but missing 'image_url' key in response!")
        
        if found_image:
            print("\nSUCCESS: 'image_url' is being sent in start_mock_test response.")
        else:
            print("\nWARNING: No non-empty image_url found. Check if seeded questions actually have URLs.")
            
    except Exception as e:
        print(f"Failed to start test: {e}")
        return

    # 5. Submit an answer verify Results (optional, but good for completeness)
    # We'll just submit one random answer and verify complete
    if questions:
        q = questions[0]
        print("\nSubmitting an answer...")
        submit_payload = {
            "attempt_id": start_data['attempt_id'],
            "question_id": q['id'],
            "user_answer": 0,
            "time_spent": 10
        }
        res = requests.post(f"{BASE_URL}/mock-tests/{test_id}/submit-answer", json=submit_payload)
        
        print("Completing test...")
        complete_payload = {"attempt_id": start_data['attempt_id']}
        comp_res = requests.post(f"{BASE_URL}/mock-tests/{test_id}/complete", json=complete_payload)
        
        print("Fetching Results...")
        results_res = requests.get(f"{BASE_URL}/mock-tests/{test_id}/results/{start_data['attempt_id']}")
        results_data = results_res.json()
        
        detailed = results_data.get("detailed_results", [])
        res_q = next((r for r in detailed if r['question_id'] == q['id']), None)
        
        if res_q and "image_url" in res_q:
             print(f"SUCCESS: 'image_url' found in get_test_results: {res_q['image_url']}")
        else:
             print("FAILURE: 'image_url' NOT found in get_test_results response.")

if __name__ == "__main__":
    verify_di_images()
