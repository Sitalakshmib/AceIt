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
def get_user_dashboard(user_id: str, db: Session = Depends(get_db)):
    """Get comprehensive user analytics dashboard"""
    try:
        print(f"[DEBUG] Dashboard request started for user: {user_id}")
        analytics = AnalyticsService.generate_user_analytics(db, user_id)
        print(f"[DEBUG] Dashboard generation successful for user: {user_id}")
        return analytics
    except Exception as e:
        print(f"[ERROR] Dashboard failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate analytics: {str(e)}")


@router.get("/unified/{user_id}")
def get_unified_analytics(user_id: str, db: Session = Depends(get_db)):
    """Get unified analytics across all modules (Aptitude, Coding, Interviews)"""
    try:
        print(f"[DEBUG] Unified analytics request started for user: {user_id}")
        from services.unified_analytics_service import UnifiedAnalyticsService
        analytics = UnifiedAnalyticsService.get_unified_analytics(db, user_id)
        print(f"[DEBUG] Unified analytics generation successful for user: {user_id}")
        return {"status": "success", "data": analytics}
    except Exception as e:
        print(f"[ERROR] Unified analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate unified analytics: {str(e)}")


@router.get("/gd/{user_id}")
def get_gd_analytics(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get detailed GD (Group Discussion) performance analytics for the dashboard card.
    Returns dimension scores, trend data, topic breakdown, and improvement insights.
    """
    try:
        from models.gd_resume_sql import GDSession
        from sqlalchemy import func
        import datetime

        cutoff = datetime.datetime.utcnow() - datetime.timedelta(days=days)

        # All GD sessions within the window
        rows = (
            db.query(GDSession)
            .filter(GDSession.user_id == user_id, GDSession.practiced_at >= cutoff)
            .order_by(GDSession.practiced_at.asc())
            .all()
        )

        # All-time sessions count
        total_all_time = db.query(func.count(GDSession.id)).filter(
            GDSession.user_id == user_id
        ).scalar() or 0

        if not rows:
            return {
                "status": "success",
                "data": {
                    "has_data": False,
                    "total_sessions": total_all_time,
                    "sessions_in_window": 0,
                    "average_score": 0,
                    "average_clarity": 0,
                    "average_coherence": 0,
                    "average_relevance": 0,
                    "weakest_dimension": None,
                    "trend": [],
                    "topic_breakdown": [],
                    "last_practiced": None,
                    "days_window": days,
                },
            }

        # Dimension averages
        def safe_avg(vals):
            vals = [v for v in vals if v is not None]
            return round(sum(vals) / len(vals), 2) if vals else 0

        avg_clarity = safe_avg([r.clarity_score for r in rows])
        avg_coherence = safe_avg([r.coherence_score for r in rows])
        avg_relevance = safe_avg([r.relevance_score for r in rows])
        avg_overall = safe_avg([r.overall_score for r in rows])

        # Weakest dimension
        dimensions = {
            "Clarity": avg_clarity,
            "Coherence": avg_coherence,
            "Relevance": avg_relevance,
        }
        weakest_dim = min(dimensions, key=dimensions.get) if any(dimensions.values()) else None

        # Trend data — last 10 sessions chronologically
        trend = [
            {
                "date": r.practiced_at.strftime("%Y-%m-%d"),
                "overall_score": round(r.overall_score, 2) if r.overall_score else 0,
                "clarity_score": round(r.clarity_score, 2) if r.clarity_score else 0,
                "coherence_score": round(r.coherence_score, 2) if r.coherence_score else 0,
                "relevance_score": round(r.relevance_score, 2) if r.relevance_score else 0,
                "topic": r.topic,
            }
            for r in rows[-10:]
        ]

        # Topic breakdown
        topic_map: Dict = {}
        for r in rows:
            key = r.topic[:40] if r.topic else "Unknown"
            if key not in topic_map:
                topic_map[key] = {"count": 0, "scores": []}
            topic_map[key]["count"] += 1
            if r.overall_score is not None:
                topic_map[key]["scores"].append(r.overall_score)

        topic_breakdown = [
            {
                "topic": t,
                "sessions": info["count"],
                "avg_score": safe_avg(info["scores"]),
            }
            for t, info in sorted(topic_map.items(), key=lambda x: -x[1]["count"])
        ][:10]

        last_practiced = rows[-1].practiced_at.isoformat() if rows else None

        return {
            "status": "success",
            "data": {
                "has_data": True,
                "total_sessions": total_all_time,
                "sessions_in_window": len(rows),
                "average_score": avg_overall,
                "average_clarity": avg_clarity,
                "average_coherence": avg_coherence,
                "average_relevance": avg_relevance,
                "weakest_dimension": weakest_dim,
                "trend": trend,
                "topic_breakdown": topic_breakdown,
                "last_practiced": last_practiced,
                "days_window": days,
            },
        }

    except Exception as e:
        print(f"[ERROR] GD analytics failed: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate GD analytics: {str(e)}")



@router.get("/progress/{user_id}")
def get_progress_history(user_id: str, days: int = 30, db: Session = Depends(get_db)):

    """
    Get progress history over time.
    """
    try:
        data = AnalyticsService.get_progress_history(db, user_id, days)
        return {"status": "success", "data": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch progress: {str(e)}")

@router.get("/topic/{user_id}/{topic}")
def get_topic_analytics(user_id: str, topic: str, db: Session = Depends(get_db)):
    """Get detailed analytics for a specific topic"""

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
