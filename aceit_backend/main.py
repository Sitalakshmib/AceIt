from dotenv import load_dotenv
load_dotenv()

# ✅ Global Monkey-patch for passlib/bcrypt 72-byte limit crash
# Intercepts bcrypt.hashpw to automatically truncate passwords to 72 bytes.
import bcrypt
original_hashpw = bcrypt.hashpw
def patched_hashpw(password, salt):
    if isinstance(password, str):
        password = password.encode('utf-8')
    if len(password) > 72:
        password = password[:72]
    return original_hashpw(password, salt)
bcrypt.hashpw = patched_hashpw

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, aptitude, coding, progress, communication, interview, resume, stt, mock_tests, analytics, gd_practice, tutor, video_presence
from contextlib import asynccontextmanager
import os

print("[INFO] GEMINI_API_KEY loaded:", bool(os.getenv("GEMINI_API_KEY")))

# Create FastAPI app
app = FastAPI(
    title="AceIT Backend API",
    description="Backend for AI-Powered Placement Preparation Platform",
    version="1.0.0"
)

# ✅ CORS MUST BE HERE (before routers)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(aptitude.router, prefix="/aptitude", tags=["Aptitude Tests"])
app.include_router(coding.router, prefix="/coding", tags=["Coding Practice"])
app.include_router(progress.router, prefix="/progress", tags=["Progress Tracking"])
app.include_router(communication.router, prefix="/communication", tags=["Communication Skills"])
app.include_router(interview.router, prefix="/interview", tags=["Mock Interviews"])
app.include_router(resume.router, prefix="/resume", tags=["Resume Analysis"])
app.include_router(stt.router, prefix="/stt", tags=["Speech To Text"])
app.include_router(tutor.router, prefix="/tutor", tags=["AI Tutor"])
app.include_router(mock_tests.router, prefix="/mock-tests", tags=["Mock Tests"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(gd_practice.router, prefix="/gd-practice", tags=["GD Practice"])
app.include_router(gd_practice.router, prefix="/gd_practice", tags=["GD Practice"])
app.include_router(video_presence.router, prefix="/video-presence", tags=["Video Presence"])

# Import here to avoid circular dependencies if any
from routes import interview_analytics
app.include_router(interview_analytics.router, prefix="/interview", tags=["Interview Analytics"])

@app.get("/")
async def root():
    return {
        "message": "AceIT Backend Server is Running!",
        "status": "active",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "aceit-backend"}

if __name__ == "__main__":
    import uvicorn
    # ✅ IMPORTANT: run on 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
