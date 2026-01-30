import requests
import json
import time

BASE_URL = "http://localhost:8001/coding"

def test_get_problems():
    print("\n1. Testing GET /problems...")
    try:
        response = requests.get(f"{BASE_URL}/problems")
        if response.status_code == 200:
            problems = response.json()
            print(f"✅ Success! Retrieved {len(problems)} problems.")
            
            # Check for Premium Two Sum
            premium = next((p for p in problems if p["id"] == "premium-1"), None)
            if premium:
                print(f"✅ Found Premium Problem: {premium['title']}")
                if premium.get("is_premium"):
                    print("✅ Correctly marked as premium.")
            else:
                print("❌ 'two-sum' premium problem NOT found!")
                
            # Check for LeetCode
            lc = next((p for p in problems if str(p["id"]).startswith("lc-")), None)
            if lc:
                print(f"✅ Found LeetCode Problem: {lc['title']} ({lc['id']})")
            else:
                print("⚠️ No LeetCode problems found (API might be slow or empty)")
                
            return True
        else:
            print(f"❌ Failed: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_submit_correct_solution():
    print("\n2. Testing Submit CORRECT Solution (Two Sum)...")
    
    code = """
def solution(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []
"""
    payload = {
        "problemId": "premium-1",
        "code": code,
        "language": "python",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/submit", json=payload)
        if response.status_code == 200:
            result = response.json()
            print(f"Response: {json.dumps(result, indent=2)}")
            passed = result.get("passed_tests")
            total = result.get("total_tests")
            
            if passed == total and total == 15:
                print(f"✅ Correct Solution PASSED {passed}/{total} tests!")
                return True
            else:
                print(f"❌ Verification Failed. Expected 15/15, got {passed}/{total}")
                return False
        else:
            print(f"❌ Request Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def test_submit_incorrect_solution():
    print("\n3. Testing Submit INCORRECT Solution...")
    
    code = """
def solution(nums, target):
    return [0, 0] # Always wrong
"""
    payload = {
        "problemId": "premium-1",
        "code": code,
        "language": "python",
        "user_id": "test_user"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/submit", json=payload)
        if response.status_code == 200:
            result = response.json()
            passed = result.get("passed_tests")
            total = result.get("total_tests")
            
            if passed < total:
                print(f"✅ Incorrect Solution verified (Passed {passed}/{total})")
                return True
            else:
                print(f"❌ Unexpected Pass! Incorrect code shouldn't pass all tests.")
                return False
        else:
            print(f"❌ Request Failed: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verifying Coding Module...")
    
    if test_get_problems():
        if test_submit_correct_solution():
            test_submit_incorrect_solution()
