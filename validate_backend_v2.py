import requests
import json
import time
import sys

BASE_URL = "http://localhost:8000"
TEST_EMAIL = f"validation_tester_{int(time.time())}@example.com"
TEST_PASSWORD = "TestPassword123"
TEST_USER = None
TOKEN = None

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

results = {
    "auth": False,
    "interview": False,
    "aptitude": False,
    "coding": False,
    "resume": False,
    "analytics": False
}

def log(message, status="INFO"):
    color = RESET
    if status == "PASS": color = GREEN
    elif status == "FAIL": color = RED
    elif status == "WARN": color = YELLOW
    print(f"{color}[{status}] {message}{RESET}")

def check_health():
    try:
        res = requests.get(f"{BASE_URL}/health")
        if res.status_code == 200:
            log("Backend is healthy", "PASS")
            return True
        else:
            log(f"Backend returned {res.status_code}", "FAIL")
            return False
    except Exception as e:
        log(f"Backend not reachable: {e}", "FAIL")
        return False

def test_auth():
    global TEST_USER, TOKEN
    log(f"Testing Auth with email: {TEST_EMAIL}")
    
    # Register
    payload = {
        "email": TEST_EMAIL,
        "username": "Validator",
        "password": TEST_PASSWORD
    }
    try:
        res = requests.post(f"{BASE_URL}/auth/register", json=payload)
        if res.status_code == 201:
            log("Registration successful", "PASS")
        elif res.status_code == 400 and "already registered" in res.text:
            log("User already registered (expected if validating again)", "WARN")
        else:
            log(f"Registration failed: {res.text}", "FAIL")
            return False

        # Login
        login_payload = {"email": TEST_EMAIL, "password": TEST_PASSWORD}
        res = requests.post(f"{BASE_URL}/auth/login", json=login_payload)
        if res.status_code == 200:
            data = res.json()
            TOKEN = data["access_token"]
            TEST_USER = data["user"]
            log(f"Login successful. UserID: {TEST_USER['id']}", "PASS")
            results["auth"] = True
            return True
        else:
            log(f"Login failed: {res.text}", "FAIL")
            return False

    except Exception as e:
        log(f"Auth loop exception: {e}", "FAIL")
        return False

def get_headers():
    return {"Authorization": f"Bearer {TOKEN}"}

def test_interview():
    if not results["auth"]: return
    log("Testing Interview Module...")
    try:
        # Start Interview
        start_payload = {
            "user_id": TEST_USER['id'],
            "interview_type": "hr",
            "topic": "behavioral",
            "resume_text": "Experienced software developer."
        }
        res = requests.post(f"{BASE_URL}/interview/start", json=start_payload, headers=get_headers())
        if res.status_code != 200:
            log(f"Start Interview failed: {res.text}", "FAIL")
            return

        data = res.json()
        session_id = data.get("session_id")
        log(f"Interview Started. SessionID: {session_id}", "PASS")

        # Answer Question (Mock)
        answer_payload = {
            "session_id": session_id,
            "text_answer": "I am a team player and love coding."
        }
        res = requests.post(f"{BASE_URL}/interview/answer", data=answer_payload, headers=get_headers())
        if res.status_code == 200:
            log("Submitted answer successfully", "PASS")
        else:
            log(f"Answer submission failed: {res.text}", "FAIL")

        # Get Results (May be empty/partial since we didn't finish, but endpoint should work)
        res = requests.get(f"{BASE_URL}/interview/results/{session_id}", headers=get_headers())
        if res.status_code == 200:
            log("Fetched interview results successfully", "PASS")
            results["interview"] = True
        else:
            log(f"Fetch results failed: {res.text}", "FAIL")

    except Exception as e:
        log(f"Interview test exception: {e}", "FAIL")

def test_aptitude():
    if not results["auth"]: return
    log("Testing Aptitude Module...")
    try:
        # Get Categories
        res = requests.get(f"{BASE_URL}/aptitude/categories", headers=get_headers())
        if res.status_code == 200:
            cats = res.json().get("categories", {})
            log(f"Fetched {len(cats)} categories", "PASS")
        
        # Get Questions
        res = requests.get(f"{BASE_URL}/aptitude/questions?count=2", headers=get_headers())
        if res.status_code == 200:
            qs = res.json()
            log(f"Fetched {len(qs)} practice questions", "PASS")
            
            if len(qs) > 0:
                # Submit Answer
                q_id = qs[0]['id']
                submit_payload = {
                    "user_id": TEST_USER['id'],
                    "answers": {q_id: 1} # Dummy answer index
                }
                res = requests.post(f"{BASE_URL}/aptitude/submit", json=submit_payload, headers=get_headers())
                if res.status_code == 200:
                    log("Aptitude submission successful", "PASS")
                    results["aptitude"] = True
                else:
                    log(f"Aptitude submit failed: {res.text}", "FAIL")
        else:
            log(f"Fetch questions failed: {res.text}", "FAIL")

    except Exception as e:
        log(f"Aptitude test exception: {e}", "FAIL")

def test_coding():
    if not results["auth"]: return
    log("Testing Coding Module...")
    try:
        # Get Problems
        res = requests.get(f"{BASE_URL}/coding/problems", headers=get_headers())
        if res.status_code != 200:
            log(f"Fetch coding problems failed: {res.text}", "FAIL")
            return

        probs = res.json()
        log(f"Fetched {len(probs)} coding problems", "PASS")
        
        if len(probs) > 0:
            # Pick a problem (Assuming at least one exists)
            p_id = probs[0]['id']
            
            # Submit Code (Run action)
            submit_payload = {
                "problemId": p_id,
                "code": "print('Hello World')",
                "language": "python",
                "user_id": TEST_USER['id'],
                "action": "run"
            }
            res = requests.post(f"{BASE_URL}/coding/submit", json=submit_payload, headers=get_headers())
            if res.status_code == 200:
                log("Coding submission (Run) successful", "PASS")
                results["coding"] = True
            else:
                log(f"Coding submit failed: {res.text}", "FAIL")

    except Exception as e:
        log(f"Coding test exception: {e}", "FAIL")

def test_resume():
    if not results["auth"]: return
    log("Testing Resume Module...")
    try:
        # Test Analysis via Text (skipping file upload complexity)
        payload = {
            "job_role": "software_developer",
            "user_id": TEST_USER['id'],
            "resume_text": "Software Developer with 5 years experience in Python and FastAPI."
        }
        # Note: resume/analyze expects form-data
        res = requests.post(f"{BASE_URL}/resume/analyze", data=payload, headers=get_headers())
        if res.status_code == 200:
            log("Resume text analysis successful", "PASS")
            results["resume"] = True
        else:
            log(f"Resume analysis failed: {res.text}", "FAIL")

    except Exception as e:
        log(f"Resume test exception: {e}", "FAIL")

def test_analytics():
    if not results["auth"]: return
    log("Testing Analytics/Dashboard...")
    try:
        uid = TEST_USER['id']
        res = requests.get(f"{BASE_URL}/analytics/dashboard/{uid}", headers=get_headers())
        if res.status_code == 200:
            log("Dashboard analytics fetched successfully", "PASS")
            results["analytics"] = True
        else:
            log(f"Dashboard fetch failed: {res.text}", "FAIL")

        # Unified
        res = requests.get(f"{BASE_URL}/analytics/unified/{uid}", headers=get_headers())
        if res.status_code == 200:
            log("Unified analytics fetched successfully", "PASS")
    except Exception as e:
        log(f"Analytics test exception: {e}", "FAIL")

if __name__ == "__main__":
    log("Starting AceIt Backend Validation...")
    
    if check_health():
        if test_auth():
            test_interview()
            test_aptitude()
            test_coding()
            test_resume()
            test_analytics()
    
    log("--------------------------------------------------")
    log("FINAL RESULTS:")
    all_pass = True
    for module, result in results.items():
        status = "PASS" if result else "FAIL"
        log(f"{module.upper()}: {status}", status)
        if not result: all_pass = False
    
    if all_pass:
        log("ALL TESTS PASSED!", "PASS")
        sys.exit(0)
    else:
        log("SOME TESTS FAILED.", "FAIL")
        sys.exit(1)
