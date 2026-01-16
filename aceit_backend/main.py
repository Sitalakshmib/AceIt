from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from routes import auth, aptitude, coding, progress, communication, interview, resume, stt
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
        "http://localhost:3000",
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

# Static files (for voice / TTS)
app.mount("/static", StaticFiles(directory="static"), name="static")

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
