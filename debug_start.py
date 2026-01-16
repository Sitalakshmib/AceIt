import requests
import sys

URL = "http://127.0.0.1:8000/interview/start"
PAYLOAD = {
    "user_id": "debug_user",
    "resume_text": "Python Developer",
    "jd_text": "Backend Engineer"
}

try:
    print(f"📡 Posting to {URL}...")
    resp = requests.post(URL, json=PAYLOAD, timeout=10) # Longer timeout for LLM
    print(f"✅ Status Code: {resp.status_code}")
    print(f"✅ Response: {resp.text}")
    
    if resp.status_code == 200:
        print("✅ Interview Start Logic Works!")
        sys.exit(0)
    else:
        print("❌ Endpoint returned error.")
        sys.exit(1)

except Exception as e:
    print(f"❌ Request Failed: {e}")
    sys.exit(1)
