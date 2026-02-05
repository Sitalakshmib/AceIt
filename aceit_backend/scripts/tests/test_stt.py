import requests

URL = "http://localhost:8001/stt/transcribe"
FILE_PATH = "test_audio.wav"

# Create a dummy wav file if not exists (just empty or random header to test connection, 
# though whisper will fail on invalid file, we want to see IF it runs or 500s)
with open(FILE_PATH, "wb") as f:
    f.write(b'RIFF$\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00\x01\x00D\xac\x00\x00\x88X\x01\x00\x02\x00\x10\x00data\x00\x00\x00\x00')

print(f"📡 Testing STT Endpoint: {URL}")
try:
    with open(FILE_PATH, "rb") as f:
        files = {"file": (FILE_PATH, f, "audio/wav")}
        resp = requests.post(URL, files=files)
        
    print(f"Status Code: {resp.status_code}")
    print(f"Response: {resp.text}")
except Exception as e:
    print(f"❌ Connection Error: {e}")
