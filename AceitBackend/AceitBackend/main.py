from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, aptitude, coding, progress, communication, interview, resume

# Create the main FastAPI application
app = FastAPI(
    title="AceIT Backend API",
    description="Backend for AI-Powered Placement Preparation Platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all route modules
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(aptitude.router, prefix="/aptitude", tags=["Aptitude Tests"])
app.include_router(coding.router, prefix="/coding", tags=["Coding Practice"])
app.include_router(progress.router, prefix="/progress", tags=["Progress Tracking"])
app.include_router(communication.router, prefix="/communication", tags=["Communication Skills"])
app.include_router(interview.router, prefix="/interview", tags=["Mock Interviews"])
app.include_router(resume.router, prefix="/resume", tags=["Resume Analysis"])

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "AceIT Backend Server is Running!",
        "status": "active",
        "version": "1.0.0"
    }

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "aceit-backend"}

# Stats endpoint
@app.get("/stats")
async def get_stats():
    from database import questions_data
    coding = len([q for q in questions_data if 'title' in q])
    aptitude = len([q for q in questions_data if 'options' in q])
    interview = len([q for q in questions_data if q.get('type') == 'interview'])
    
    return {
        "total_questions": len(questions_data),
        "coding_problems": coding,
        "aptitude_questions": aptitude, 
        "interview_questions": interview,
        "breakdown_by_source": "Check terminal for detailed breakdown"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)