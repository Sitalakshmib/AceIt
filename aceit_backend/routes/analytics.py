from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_postgres import get_db
from services.ai_analytics_service import AIAnalyticsService
from services.analytics_service import AnalyticsService
from typing import List, Dict, Optional
import json

router = APIRouter()

@router.get("/daily-progress")
def get_daily_progress(user_id: str, days: int = 7, db: Session = Depends(get_db)):
    """
    Get daily mock test accuracy trends.
    """
    try:
        data = AIAnalyticsService.get_daily_mock_progress(db, user_id, days)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch daily progress: {str(e)}")

@router.get("/mock-report")
def get_mock_performance_report(user_id: str, db: Session = Depends(get_db)):
    """
    Get detailed strength/weakness report based on mock tests.
    """
    try:
        report = AIAnalyticsService.get_mock_topic_performance(db, user_id)
        return {"status": "success", "data": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch mock report: {str(e)}")

@router.get("/ai-coach")
def get_ai_coach_advice(user_id: str, db: Session = Depends(get_db)):
    """
    Get AI-powered tutoring and strategic advice.
    """
    try:
        advice = AIAnalyticsService.generate_ai_insight(db, user_id)
        return {"status": "success", "data": advice}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch AI advice: {str(e)}")

@router.get("/overall-summary")
def get_overall_summary(user_id: str, db: Session = Depends(get_db)):
    """
    Get high-level summary cards.
    """
    try:
        summary = AIAnalyticsService.get_overall_summary(db, user_id)
        return {"status": "success", "data": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch summary: {str(e)}")

@router.get("/dashboard/{user_id}")
def get_analytics_dashboard(user_id: str, db: Session = Depends(get_db)):
    """
    Get comprehensive analytics dashboard for a user.
    """
    try:
        data = AnalyticsService.generate_user_analytics(db, user_id)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch dashboard: {str(e)}")

@router.get("/progress/{user_id}")
def get_analytics_progress(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get progress history over time.
    """
    try:
        data = AnalyticsService.get_progress_history(db, user_id, days)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch progress: {str(e)}")

@router.get("/topic/{user_id}/{topic}")
def get_analytics_topic(user_id: str, topic: str, db: Session = Depends(get_db)):
    """
    Get detailed analytics for a specific topic.
    """
    try:
        data = AnalyticsService.get_topic_analytics(db, user_id, topic)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch topic analytics: {str(e)}")

# --- COACH CHATBOT ROUTES (SIM VOICE PATTERN) ---
from services.sim_aptitude_coach import SimAptitudeCoach
from fastapi import UploadFile, File, Form, Response, Depends
import shutil
import os

_coach_engine = None
def get_coach_engine():
    global _coach_engine
    if _coach_engine is None:
        _coach_engine = SimAptitudeCoach()
    return _coach_engine

@router.post("/coach/start")
def start_coach_session(
    user_id: str = Form(...),
    db: Session = Depends(get_db),
    engine: SimAptitudeCoach = Depends(get_coach_engine)
):
    try:
        return engine.start_session(user_id, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coach/answer")
def process_coach_answer(
    session_id: str = Form(...),
    text_message: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
    engine: SimAptitudeCoach = Depends(get_coach_engine)
):
    try:
        temp_file = None
        if audio_file:
            temp_file = f"temp_coach_{session_id}_{audio_file.filename}"
            with open(temp_file, "wb") as buffer:
                shutil.copyfileobj(audio_file.file, buffer)
        
        result = engine.process_message(session_id, db, audio_file_path=temp_file, text_message=text_message)
        
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
            
        return result
    except Exception as e:
        if temp_file and os.path.exists(temp_file):
            try: os.remove(temp_file)
            except: pass
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/coach/audio")
def generate_coach_audio(
    text: str = Form(...)
):
    """
    Generate audio for a specific text on-demand.
    Used for the 'Replay' feature in the chat.
    """
    try:
        from services.voice_service import voice_service
        audio_url = voice_service.synthesize(text)
        return {"status": "success", "audio_url": audio_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
