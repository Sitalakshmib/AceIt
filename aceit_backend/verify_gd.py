import requests
import time

# Wait a moment for reload if needed (optional, but good practice in this flow)
time.sleep(2)

url = "http://localhost:8000/gd/generate"
payload = {"topic": "AI in banking"}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    print(response.json())
except Exception as e:
    print(f"Request failed: {e}")
