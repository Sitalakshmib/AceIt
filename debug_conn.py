import requests
import sys

URL = "http://127.0.0.1:8000/health"

try:
    print(f"📡 Pinging {URL}...")
    resp = requests.get(URL, timeout=2)
    print(f"✅ Status Code: {resp.status_code}")
    print(f"✅ Response: {resp.text}")
    if resp.status_code == 200:
        sys.exit(0)
    else:
        sys.exit(1)
except Exception as e:
    print(f"❌ Connection Failed: {e}")
    sys.exit(1)
