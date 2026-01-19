"""
Analytics API Routes

Endpoints for user analytics, performance metrics, and recommendations.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_postgres import get_db
from services.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/dashboard/{user_id}")
async def get_user_dashboard(user_id: str, db: Session = Depends(get_db)):
    """Get comprehensive user analytics dashboard"""
    try:
        analytics = AnalyticsService.generate_user_analytics(db, user_id)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate analytics: {str(e)}")


@router.get("/progress/{user_id}")
async def get_progress_history(user_id: str, days: int = 30, db: Session = Depends(get_db)):
    """
    Get user's progress over time
    
    Query params:
        - days: Number of days to look back (default: 30)
    """
    try:
        history = AnalyticsService.get_progress_history(db, user_id, days)
        return history
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get progress history: {str(e)}")


@router.get("/topic/{user_id}/{topic}")
async def get_topic_analytics(user_id: str, topic: str, db: Session = Depends(get_db)):
    """Get detailed analytics for a specific topic"""
    try:
        analytics = AnalyticsService.get_topic_analytics(db, user_id, topic)
        return analytics
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get topic analytics: {str(e)}")
