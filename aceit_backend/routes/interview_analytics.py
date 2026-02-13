"""
Interview Performance Analytics Routes

SCOPE: Analytics ONLY - aggregates existing interview session data
PURPOSE: Provide students with holistic interview performance insights

CRITICAL RULES:
- NO changes to interview logic or scoring
- NO re-computation of past scores
- ONLY reads existing session data
- Privacy-first: No raw transcripts, video, or audio

Author: AceIt Backend Team
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, List, Optional
from datetime import datetime
from services.sim_voice_interviewer import SimVoiceInterviewer
from routes.interview import get_engine

router = APIRouter()


@router.get("/analytics/{user_id}")
async def get_interview_analytics(user_id: str, engine: SimVoiceInterviewer = Depends(get_engine)):
    """
    Get comprehensive interview performance analytics for a user.
    
    Aggregates data from:
    - Technical interviews
    - HR behavioral interviews
    - Video presence interviews
    
    Returns analytics without modifying any interview data.
    """
    try:
        print(f"[InterviewAnalytics] Generating analytics for user: {user_id}")
        
        # Get all user sessions from in-memory store
        user_sessions = [
            session for session in engine.sessions.values()
            if session.get("user_id") == user_id
        ]
        
        if not user_sessions:
            return {
                "user_id": user_id,
                "has_data": False,
                "message": "No interview data available. Start your first interview to see analytics!",
                "overall": _get_empty_overall(),
                "technical": _get_empty_category(),
                "hr": _get_empty_category(),
                "video_presence": _get_empty_category(),
                "skill_insights": [],
                "recommendations": _get_empty_recommendations()
            }
        
        # Separate sessions by interview type
        technical_sessions = [s for s in user_sessions if s.get("interview_type") == "technical"]
        hr_sessions = [s for s in user_sessions if s.get("interview_type") == "hr"]
        video_sessions = [s for s in user_sessions if s.get("interview_type") == "video-practice"]
        
        # Aggregate metrics for each category
        technical_metrics = _aggregate_technical_interviews(technical_sessions)
        hr_metrics = _aggregate_hr_interviews(hr_sessions)
        video_metrics = _aggregate_video_presence(video_sessions)
        
        # Calculate overall summary
        overall_summary = _calculate_overall_summary(
            user_sessions, technical_metrics, hr_metrics, video_metrics
        )
        
        # Aggregate skill insights
        skill_insights = _calculate_skill_insights(
            technical_metrics, hr_metrics, video_metrics
        )
        
        # Generate recommendations
        recommendations = _generate_recommendations(
            technical_metrics, hr_metrics, video_metrics
        )
        
        return {
            "user_id": user_id,
            "has_data": True,
            "overall": overall_summary,
            "technical": technical_metrics,
            "hr": hr_metrics,
            "video_presence": video_metrics,
            "skill_insights": skill_insights,
            "recommendations": recommendations,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        print(f"[InterviewAnalytics] Error generating analytics: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to generate analytics: {str(e)}")


@router.get("/analytics/{user_id}/category/{category}")
async def get_category_analytics(
    user_id: str, 
    category: str, 
    engine: SimVoiceInterviewer = Depends(get_engine)
):
    """
    Get detailed analytics for a specific interview category.
    
    Args:
        user_id: User ID
        category: One of 'technical', 'hr', 'video-presence'
    """
    try:
        # Validate category
        valid_categories = ["technical", "hr", "video-presence"]
        if category not in valid_categories:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid category. Must be one of: {', '.join(valid_categories)}"
            )
        
        # Get user sessions
        user_sessions = [
            session for session in engine.sessions.values()
            if session.get("user_id") == user_id
        ]
        
        # Filter by category
        if category == "technical":
            sessions = [s for s in user_sessions if s.get("interview_type") == "technical"]
            metrics = _aggregate_technical_interviews(sessions)
        elif category == "hr":
            sessions = [s for s in user_sessions if s.get("interview_type") == "hr"]
            metrics = _aggregate_hr_interviews(sessions)
        else:  # video-presence
            sessions = [s for s in user_sessions if s.get("interview_type") == "video-practice"]
            metrics = _aggregate_video_presence(sessions)
        
        return {
            "user_id": user_id,
            "category": category,
            "metrics": metrics,
            "generated_at": datetime.utcnow().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"[InterviewAnalytics] Error getting category analytics: {e}")
        raise HTTPException(status_code=500, detail=str(e))



def _get_iso_timestamp(timestamp):
    """Safely get ISO timestamp from string or datetime."""
    if not timestamp:
        return None
    if isinstance(timestamp, str):
        return timestamp
    if hasattr(timestamp, 'isoformat'):
        return timestamp.isoformat()
    return str(timestamp)

# ============================================================================
# AGGREGATION FUNCTIONS
# ============================================================================


def _aggregate_technical_interviews(sessions: List[Dict]) -> Dict:
    """Aggregate metrics from technical interview sessions."""
    if not sessions:
        return _get_empty_category()
    
    # Calculate average score
    all_scores = []
    for session in sessions:
        scores = session.get("scores", [])
        if scores:
            all_scores.extend(scores)
    
    average_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    
    # Collect strengths and weaknesses
    strengths = []
    weaknesses = []
    
    for session in sessions:
        scores = session.get("scores", [])
        qa_pairs = session.get("qa_pairs", [])
        
        for qa in qa_pairs:
            score = qa.get("score", 0)
            question = qa.get("question", "")
            
            # Extract topic from question (simplified)
            if score >= 75:
                strengths.append(f"Strong answer (Score: {score})")
            elif score < 60:
                weaknesses.append(f"Needs improvement (Score: {score})")
    
    # Get weak areas
    weak_areas = []
    for session in sessions:
        weak_areas.extend(session.get("weak_areas", []))
    
    # Deduplicate and limit
    unique_weaknesses = list(set(weak_areas))[:3]
    
    # Calculate trend
    trend = _calculate_trend(sessions)
    
    # Get last interview date
    last_interview = None
    if sessions:
        start_times = [s.get("start_time") for s in sessions if s.get("start_time")]
        if start_times:
            last_interview = _get_iso_timestamp(max(start_times))

    
    return {
        "sessions_count": len(sessions),
        "average_score": average_score,
        "trend": trend,
        "last_interview": last_interview,
        "strengths": ["Strong technical understanding", "Clear explanations"] if average_score >= 70 else ["Keep practicing"],
        "improvement_areas": unique_weaknesses if unique_weaknesses else ["Continue building fundamentals"],
        "has_data": True
    }


def _aggregate_hr_interviews(sessions: List[Dict]) -> Dict:
    """Aggregate metrics from HR behavioral interview sessions."""
    if not sessions:
        return _get_empty_category()
    
    # Calculate average score
    all_scores = []
    for session in sessions:
        scores = session.get("scores", [])
        if scores:
            all_scores.extend(scores)
    
    average_score = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
    
    # Calculate trend
    trend = _calculate_trend(sessions)
    
    # Get last interview date
    last_interview = None
    if sessions:
        start_times = [s.get("start_time") for s in sessions if s.get("start_time")]
        if start_times:
            last_interview = _get_iso_timestamp(max(start_times))

    
    # Determine strengths and improvement areas based on score
    strengths = []
    improvement_areas = []
    
    if average_score >= 75:
        strengths = ["Clear communication", "Structured responses", "Good examples"]
        improvement_areas = ["Continue practicing STAR format"]
    elif average_score >= 60:
        strengths = ["Decent communication", "Honest responses"]
        improvement_areas = ["Provide more concrete examples", "Structure answers better"]
    else:
        strengths = ["Willingness to improve"]
        improvement_areas = ["Practice STAR format", "Prepare more examples", "Be more specific"]
    
    return {
        "sessions_count": len(sessions),
        "average_score": average_score,
        "trend": trend,
        "last_interview": last_interview,
        "strengths": strengths,
        "improvement_areas": improvement_areas,
        "has_data": True
    }


def _aggregate_video_presence(sessions: List[Dict]) -> Dict:
    """Aggregate metrics from video presence interview sessions."""
    if not sessions:
        return _get_empty_category()
    
    # Note: Video presence sessions may have different data structure
    # For now, we'll use a simplified approach
    
    # Calculate average score
    scores = []
    for s in sessions:
        # Check for scores array first
        session_scores = s.get("scores", [])
        if session_scores:
            scores.extend(session_scores)
        # Fallback to overall_score in indicators
        elif "indicators" in s:
            scores.append(s["indicators"].get("overall_score", 0))

    average_score = round(sum(scores) / len(scores), 1) if scores else 0
    
    # Calculate trend
    trend = _calculate_trend(sessions)
    
    # Get last interview date
    last_interview = None
    if sessions:
        start_times = [s.get("start_time") for s in sessions if s.get("start_time")]
        if start_times:
            last_interview = _get_iso_timestamp(max(start_times))

            
    # Aggregate feedback for strengths/weaknesses
    all_strengths = []
    all_improvements = []
    
    for s in sessions:
        # Check qa_pairs first (more granular)
        qa_pairs = s.get("qa_pairs", [])
        if qa_pairs:
            for qa in qa_pairs:
                qa_feedback = qa.get("feedback", {})
                if qa_feedback:
                    # strengths
                    for st in qa_feedback.get("strengths", []):
                        if isinstance(st, dict):
                            all_strengths.append(st.get("observation", str(st)))
                        else:
                            all_strengths.append(str(st))
                            
                    # improvements/tips
                    for imp in qa_feedback.get("improvement_tips", []):
                        all_improvements.append(str(imp))
                        
                    # faults
                    for f in qa_feedback.get("faults_detected", []):
                        all_improvements.append(str(f))
                    
        # Also check top-level session feedback (for completeness/legacy)
        feedback = s.get("feedback", {})
        if feedback:
            # Extract from newer structure (visual_metrics etc)
            visual = feedback.get("visual_analysis", {})
            if visual:
                all_strengths.extend(visual.get("strengths", []))
                all_improvements.extend(visual.get("improvement_suggestions", []))
                obs = visual.get("observations", [])
                if obs: all_strengths.extend(obs)
            
                # Legacy/Alternate structure fallback
                all_strengths.extend(feedback.get("visual_observations", []))
                
                # speech_observations are dicts: {"observation": "...", "explanation": "..."}
                speech_obs = feedback.get("speech_observations", [])
                for obs in speech_obs:
                    if isinstance(obs, dict):
                        all_strengths.append(obs.get("observation", ""))
                    else:
                        all_strengths.append(str(obs))
                        
                all_improvements.extend(feedback.get("improvement_tips", []))
                all_improvements.extend(feedback.get("faults_detected", []))
                
        # Deduplicate and limit (ensure all items are strings first)
        all_strengths = [str(s) for s in all_strengths if s]
        all_improvements = [str(i) for i in all_improvements if i]
        
        unique_strengths = list(set(all_strengths))[:3]
        unique_improvements = list(set(all_improvements))[:3]
    
    return {
        "sessions_count": len(sessions),
        "average_score": average_score,
        "trend": trend,
        "last_interview": last_interview,
        "strengths": unique_strengths if unique_strengths else ["Practicing presence", "Building confidence"],
        "improvement_areas": unique_improvements if unique_improvements else ["Continue practicing"],
        "has_data": True
    }



def _calculate_overall_summary(
    all_sessions: List[Dict],
    technical_metrics: Dict,
    hr_metrics: Dict,
    video_metrics: Dict
) -> Dict:
    """Calculate overall interview performance summary."""
    
    total_sessions = len(all_sessions)
    
    # Calculate combined average score
    scores_with_weights = []
    
    if technical_metrics["has_data"]:
        scores_with_weights.append((technical_metrics["average_score"], technical_metrics["sessions_count"]))
    if hr_metrics["has_data"]:
        scores_with_weights.append((hr_metrics["average_score"], hr_metrics["sessions_count"]))
    if video_metrics["has_data"]:
        scores_with_weights.append((video_metrics["average_score"], video_metrics["sessions_count"]))
    
    # Weighted average
    if scores_with_weights:
        total_weighted = sum(score * count for score, count in scores_with_weights)
        total_count = sum(count for _, count in scores_with_weights)
        combined_score = round(total_weighted / total_count, 1) if total_count > 0 else 0
    else:
        combined_score = 0
    
    # Determine overall trend
    trends = [
        technical_metrics.get("trend", "stable"),
        hr_metrics.get("trend", "stable"),
        video_metrics.get("trend", "stable")
    ]
    
    if "improving" in trends:
        overall_trend = "Improving"
    elif "declining" in trends:
        overall_trend = "Needs Focus"
    else:
        overall_trend = "Stable"
    
    # Get last interview date
    last_interview = None
    if all_sessions:
        start_times = [s.get("start_time") for s in all_sessions if s.get("start_time")]
        if start_times:
            try:
                last_interview = _get_iso_timestamp(max(start_times))
            except:
                last_interview = None

    
    return {
        "total_interviews": total_sessions,
        "combined_score": combined_score,
        "overall_trend": overall_trend,
        "last_interview": last_interview,
        "performance_rating": (
            "Excellent" if combined_score >= 85 else
            "Good" if combined_score >= 70 else
            "Fair" if combined_score >= 55 else
            "Needs Improvement"
        )
    }


def _calculate_skill_insights(
    technical_metrics: Dict,
    hr_metrics: Dict,
    video_metrics: Dict
) -> List[Dict]:
    """Calculate aggregated skill-level insights."""
    
    skills = []
    
    # Technical Explanation Quality (from technical interviews)
    tech_score = technical_metrics.get("average_score", 0) if technical_metrics["has_data"] else 0
    skills.append({
        "skill": "Technical Explanation Quality",
        "score": tech_score,
        "level": "Good" if tech_score >= 70 else "Moderate" if tech_score >= 50 else "Low",
        "has_data": technical_metrics["has_data"]
    })
    
    # Behavioral Communication (from HR interviews)
    hr_score = hr_metrics.get("average_score", 0) if hr_metrics["has_data"] else 0
    skills.append({
        "skill": "Behavioral Communication",
        "score": hr_score,
        "level": "Good" if hr_score >= 70 else "Moderate" if hr_score >= 50 else "Low",
        "has_data": hr_metrics["has_data"]
    })
    
    # Video Presence (Aggregated)
    video_score = video_metrics.get("average_score", 0) if video_metrics["has_data"] else 0
    skills.append({
        "skill": "Video Presence",
        "score": video_score,
        "level": "Good" if video_score >= 70 else "Moderate" if video_score >= 50 else "Low",
        "has_data": video_metrics["has_data"]
    })
    
    return skills


def _generate_recommendations(
    technical_metrics: Dict,
    hr_metrics: Dict,
    video_metrics: Dict
) -> Dict:
    """Generate focus areas and recommendations."""
    
    focus_areas = []
    cta_buttons = []
    
    # Analyze each category and generate recommendations
    if technical_metrics["has_data"]:
        if technical_metrics["average_score"] < 70:
            focus_areas.extend(technical_metrics.get("improvement_areas", [])[:2])
            cta_buttons.append({
                "label": "Practice Technical Interview",
                "action": "start_technical",
                "priority": "high"
            })
        else:
            cta_buttons.append({
                "label": "Practice Technical Interview",
                "action": "start_technical",
                "priority": "medium"
            })
    else:
        cta_buttons.append({
            "label": "Start Technical Interview",
            "action": "start_technical",
            "priority": "high"
        })
    
    if hr_metrics["has_data"]:
        if hr_metrics["average_score"] < 70:
            focus_areas.extend(hr_metrics.get("improvement_areas", [])[:2])
            cta_buttons.append({
                "label": "Practice HR Interview",
                "action": "start_hr",
                "priority": "high"
            })
        else:
            cta_buttons.append({
                "label": "Practice HR Interview",
                "action": "start_hr",
                "priority": "medium"
            })
    else:
        cta_buttons.append({
            "label": "Start HR Interview",
            "action": "start_hr",
            "priority": "high"
        })
    
    if video_metrics["has_data"]:
        focus_areas.extend(video_metrics.get("improvement_areas", [])[:1])
        cta_buttons.append({
            "label": "Practice Video Presence",
            "action": "start_video",
            "priority": "medium"
        })
    else:
        cta_buttons.append({
            "label": "Start Video Presence",
            "action": "start_video",
            "priority": "high"
        })
    
    # Limit focus areas to top 3
    focus_areas = focus_areas[:3]
    
    # If no specific focus areas, provide general recommendations
    if not focus_areas:
        focus_areas = [
            "Continue practicing all interview types",
            "Build consistency in your practice",
            "Focus on providing detailed examples"
        ]
    
    return {
        "focus_areas": focus_areas,
        "cta_buttons": cta_buttons,
        "general_advice": "Practice regularly to build confidence and improve your interview skills."
    }


def _calculate_trend(sessions: List[Dict]) -> str:
    """Calculate performance trend from sessions."""
    if len(sessions) < 2:
        return "stable"
    
    # Sort sessions by start time
    sorted_sessions = sorted(
        sessions,
        key=lambda s: str(s.get("start_time", ""))  # Compare as strings
    )

    
    # Compare first half vs second half
    mid = len(sorted_sessions) // 2
    
    first_half_scores = []
    second_half_scores = []
    
    for session in sorted_sessions[:mid]:
        scores = session.get("scores", [])
        if scores:
            first_half_scores.extend(scores)
    
    for session in sorted_sessions[mid:]:
        scores = session.get("scores", [])
        if scores:
            second_half_scores.extend(scores)
    
    if not first_half_scores or not second_half_scores:
        return "stable"
    
    first_avg = sum(first_half_scores) / len(first_half_scores)
    second_avg = sum(second_half_scores) / len(second_half_scores)
    
    if second_avg > first_avg + 5:
        return "improving"
    elif second_avg < first_avg - 5:
        return "declining"
    return "stable"


# ============================================================================
# EMPTY STATE HELPERS
# ============================================================================

def _get_empty_overall() -> Dict:
    """Return empty overall summary."""
    return {
        "total_interviews": 0,
        "combined_score": 0,
        "overall_trend": "N/A",
        "last_interview": None,
        "performance_rating": "No Data"
    }


def _get_empty_category() -> Dict:
    """Return empty category metrics."""
    return {
        "sessions_count": 0,
        "average_score": 0,
        "trend": "stable",
        "last_interview": None,
        "strengths": [],
        "improvement_areas": [],
        "has_data": False
    }


def _get_empty_recommendations() -> Dict:
    """Return empty recommendations."""
    return {
        "focus_areas": ["Start your first interview to get personalized recommendations"],
        "cta_buttons": [
            {"label": "Start Technical Interview", "action": "start_technical", "priority": "high"},
            {"label": "Start HR Interview", "action": "start_hr", "priority": "high"},
            {"label": "Start Video Presence", "action": "start_video", "priority": "high"}
        ],
        "general_advice": "Begin practicing to build your interview skills!"
    }
