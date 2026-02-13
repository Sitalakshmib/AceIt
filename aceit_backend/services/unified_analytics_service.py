"""
Unified Analytics Service

Aggregates practice activity and performance data across all modules:
- Aptitude Training
- Coding Practice
- Interview Modules (Technical, HR, Video Presence, GD Practice)

This service ONLY reads existing data and does NOT modify any module logic.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from models.aptitude_sql import UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from models.mock_test_sql import MockTestAttempt
from models.user_coding_progress import UserCodingProgress
from models.coding_problem_sql import CodingProblem
from models.interview_models import InterviewSession


class UnifiedAnalyticsService:
    """Aggregate analytics across all practice modules"""
    
    @staticmethod
    def get_unified_analytics(db: Session, user_id: str) -> Dict:
        """
        Generate unified analytics dashboard aggregating all modules.
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Dictionary with unified analytics data
        """
        print(f"[UnifiedAnalytics] Generating analytics for user: {user_id}")
        
        # Get data from each module
        aptitude_data = UnifiedAnalyticsService._get_aptitude_summary(db, user_id)
        coding_data = UnifiedAnalyticsService._get_coding_summary(db, user_id)
        interview_data = UnifiedAnalyticsService._get_interview_summary(user_id)
        
        # Calculate overall summary
        overall_summary = UnifiedAnalyticsService._calculate_overall_summary(
            aptitude_data, coding_data, interview_data
        )
        
        # Module-wise performance
        module_performance = UnifiedAnalyticsService._get_module_performance(
            aptitude_data, coding_data, interview_data
        )
        
        # Skill breakdown (aggregated)
        skill_breakdown = UnifiedAnalyticsService._aggregate_skill_breakdown(
            aptitude_data, coding_data, interview_data
        )
        
        # Weak areas and recommendations
        weak_areas = UnifiedAnalyticsService._identify_weak_areas(
            aptitude_data, coding_data, interview_data
        )
        
        # Recent activity timeline
        recent_activity = UnifiedAnalyticsService._get_recent_activity(
            db, user_id, aptitude_data, coding_data, interview_data
        )
        
        return {
            "user_id": user_id,
            "overall_summary": overall_summary,
            "module_performance": module_performance,
            "skill_breakdown": skill_breakdown,
            "weak_areas": weak_areas,
            "recent_activity": recent_activity,
            "generated_at": datetime.utcnow().isoformat()
        }
    
    @staticmethod
    def _get_aptitude_summary(db: Session, user_id: str) -> Dict:
        """Extract aptitude module summary from existing data"""
        try:
            # Get progress records
            progress_records = db.query(UserAptitudeProgress)\
                .filter(UserAptitudeProgress.user_id == user_id).all()
            
            # Get mock test attempts
            mock_attempts = db.query(MockTestAttempt)\
                .filter(MockTestAttempt.user_id == user_id)\
                .filter(MockTestAttempt.status == "completed").all()
            
            # Calculate stats
            total_questions = sum(p.questions_attempted or 0 for p in progress_records)
            total_correct = sum(p.questions_correct or 0 for p in progress_records)
            accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
            total_time_minutes = sum(p.total_time_spent_seconds or 0 for p in progress_records) // 60
            
            # Get last practiced date
            last_practiced = None
            if progress_records:
                last_dates = [p.last_practiced for p in progress_records if p.last_practiced]
                last_practiced = max(last_dates) if last_dates else None
            
            # Identify weak topics (accuracy < 60%)
            weak_topics = [
                p.topic for p in progress_records 
                if p.overall_accuracy < 60 and p.questions_attempted >= 5
            ]
            
            return {
                "sessions_count": len(mock_attempts),
                "total_questions": total_questions,
                "accuracy": round(accuracy, 1),
                "total_time_minutes": total_time_minutes,
                "average_score": round(sum(a.accuracy_percentage for a in mock_attempts) / len(mock_attempts), 1) if mock_attempts else 0,
                "last_practiced": last_practiced.isoformat() if last_practiced else None,
                "weak_topics": weak_topics[:3],
                "has_data": len(progress_records) > 0 or len(mock_attempts) > 0
            }
        except Exception as e:
            print(f"[UnifiedAnalytics] Error getting aptitude summary: {e}")
            return {
                "sessions_count": 0,
                "total_questions": 0,
                "accuracy": 0,
                "total_time_minutes": 0,
                "average_score": 0,
                "last_practiced": None,
                "weak_topics": [],
                "has_data": False
            }
    
    @staticmethod
    def _get_coding_summary(db: Session, user_id: str) -> Dict:
        """Extract coding module summary from existing data"""
        try:
            # Get all coding progress records
            progress_records = db.query(UserCodingProgress)\
                .filter(UserCodingProgress.user_id == user_id).all()
            
            # Get total problems in database
            total_db_problems = db.query(CodingProblem).count()
            
            # Calculate stats
            total_attempted = len(progress_records)
            total_solved = sum(1 for p in progress_records if p.is_solved)
            success_rate = (total_solved / total_attempted * 100) if total_attempted > 0 else 0
            
            # Progress percentage based on total database problems
            progress_percentage = (total_solved / total_db_problems * 100) if total_db_problems > 0 else 0
            
            total_attempts = sum(p.attempts or 0 for p in progress_records)
            
            # Get last practiced date
            last_practiced = None
            if progress_records:
                last_dates = [p.last_submission_date for p in progress_records if p.last_submission_date]
                last_practiced = max(last_dates) if last_dates else None
            
            return {
                "sessions_count": total_attempted,
                "problems_attempted": total_attempted,
                "problems_solved": total_solved,
                "total_problems": total_db_problems,
                "success_rate": round(success_rate, 1),
                "progress_percentage": round(progress_percentage, 1),
                "total_attempts": total_attempts,
                "last_practiced": last_practiced.isoformat() if last_practiced else None,
                "has_data": total_attempted > 0
            }
        except Exception as e:
            print(f"[UnifiedAnalytics] Error getting coding summary: {e}")
            return {
                "sessions_count": 0,
                "problems_attempted": 0,
                "problems_solved": 0,
                "total_problems": 0,
                "success_rate": 0,
                "progress_percentage": 0,
                "total_attempts": 0,
                "last_practiced": None,
                "has_data": False
            }
    
    @staticmethod
    def _get_interview_summary(user_id: str) -> Dict:
        """
        Extract interview module summary from in-memory sessions.
        
        Note: Interview sessions are stored in-memory only. Data will be lost on server restart.
        """
        try:
            # Import the singleton interviewer engine
            from routes.interview import get_engine
            
            engine = get_engine()
            
            # Filter sessions for this user
            user_sessions = [
                session for session in engine.sessions.values()
                if session.get("user_id") == user_id
            ]
            
            if not user_sessions:
                return {
                    "total_sessions": 0,
                    "technical_sessions": 0,
                    "hr_sessions": 0,
                    "video_presence_sessions": 0,
                    "technical_score": 0,
                    "hr_score": 0,
                    "video_presence_score": 0,
                    "average_score": 0,
                    "last_practiced": None,
                    "weak_areas": [],
                    "has_data": False
                }
            
            # Helper for category averaging
            def _get_cat_avg(sessions):
                scores = []
                for s in sessions:
                    s_scores = s.get("scores", [])
                    if s_scores:
                        scores.extend(s_scores)
                    elif "indicators" in s: # Video presence fallback
                        scores.append(s["indicators"].get("overall_score", 0))
                return round(sum(scores) / len(scores), 1) if scores else 0

            # Categorize by interview type
            technical_sessions = [s for s in user_sessions if s.get("interview_type") == "technical"]
            hr_sessions = [s for s in user_sessions if s.get("interview_type") == "hr"]
            video_sessions = [s for s in user_sessions if s.get("interview_type") == "video-practice"]
            
            # Calculate average scores
            tech_score = _get_cat_avg(technical_sessions)
            hr_score = _get_cat_avg(hr_sessions)
            video_score = _get_cat_avg(video_sessions)
            overall_score = _get_cat_avg(user_sessions)
            
            # Collect weak areas
            weak_areas = []
            for session in user_sessions:
                weak_areas.extend(session.get("weak_areas", []))
            weak_areas = list(set(weak_areas))[:3]  # Unique, top 3
            
            # Get last practiced date (Safely handle both string and datetime)
            last_practiced = None
            start_times = [s.get("start_time") for s in user_sessions if s.get("start_time")]
            if start_times:
                latest = max(start_times)
                # Ensure it's returned as an ISO string
                if isinstance(latest, str):
                    last_practiced = latest
                elif hasattr(latest, "isoformat"):
                    last_practiced = latest.isoformat()
                else:
                    last_practiced = str(latest)
            
            return {
                "total_sessions": len(user_sessions),
                "technical_sessions": len(technical_sessions),
                "hr_sessions": len(hr_sessions),
                "video_presence_sessions": len(video_sessions),
                "technical_score": tech_score,
                "hr_score": hr_score,
                "video_presence_score": video_score,
                "average_score": overall_score,
                "last_practiced": last_practiced,
                "weak_areas": weak_areas,
                "has_data": len(user_sessions) > 0
            }
        except Exception as e:
            print(f"[UnifiedAnalytics] Error getting interview summary: {e}")
            import traceback
            traceback.print_exc()
            return {
                "total_sessions": 0,
                "technical_sessions": 0,
                "hr_sessions": 0,
                "video_presence_sessions": 0,
                "technical_score": 0,
                "hr_score": 0,
                "video_presence_score": 0,
                "average_score": 0,
                "last_practiced": None,
                "weak_areas": [],
                "has_data": False
            }
    
    @staticmethod
    def _calculate_overall_summary(aptitude_data: Dict, coding_data: Dict, interview_data: Dict) -> Dict:
        """Calculate overall practice summary across all modules"""
        total_sessions = (
            aptitude_data["sessions_count"] +
            coding_data["sessions_count"] +
            interview_data["total_sessions"]
        )
        
        total_time_minutes = aptitude_data["total_time_minutes"]
        
        # Calculate modules used
        modules_used = []
        if aptitude_data["has_data"]:
            modules_used.append("Aptitude")
        if coding_data["has_data"]:
            modules_used.append("Coding")
        if interview_data["has_data"]:
            modules_used.append("Interviews")
        
        # Calculate practice streak (based on last practiced dates)
        # Check if user practiced today or yesterday
        today = datetime.now().date()
        yesterday = today - timedelta(days=1)
        
        last_dates = []
        if aptitude_data["last_practiced"]:
            last_dates.append(datetime.fromisoformat(aptitude_data["last_practiced"]).date())
        if coding_data["last_practiced"]:
            last_dates.append(datetime.fromisoformat(coding_data["last_practiced"]).date())
        if interview_data["last_practiced"]:
            last_dates.append(datetime.fromisoformat(interview_data["last_practiced"]).date())
            
        practice_streak = 0
        if last_dates:
            most_recent = max(last_dates)
            if most_recent == today or most_recent == yesterday:
                # Basic streak: if practiced recently, show at least 1
                # In a real system, we'd count continuous days from DB
                practice_streak = 1 if most_recent == yesterday else 2
        
        # Overall improvement trend (simplified)
        trend = "stable"
        if aptitude_data["has_data"] and aptitude_data["accuracy"] > 70:
            trend = "improving"
        elif coding_data["has_data"] and coding_data["success_rate"] > 60:
            trend = "improving"
        elif interview_data["has_data"] and interview_data["average_score"] > 70:
            trend = "improving"
        
        return {
            "total_sessions": total_sessions,
            "total_time_minutes": total_time_minutes,
            "total_time_hours": round(total_time_minutes / 60, 1),
            "modules_used": modules_used,
            "modules_count": len(modules_used),
            "practice_streak": practice_streak,
            "improvement_trend": trend
        }
    
    @staticmethod
    def _get_module_performance(aptitude_data: Dict, coding_data: Dict, interview_data: Dict) -> List[Dict]:
        """Get performance data for each module"""
        modules = []
        
        # Aptitude
        modules.append({
            "module": "Aptitude",
            "sessions": aptitude_data["sessions_count"],
            "performance_level": "Good" if aptitude_data["accuracy"] >= 70 else "Moderate" if aptitude_data["accuracy"] >= 50 else "Low",
            "performance_score": aptitude_data["accuracy"],
            "last_practiced": aptitude_data["last_practiced"],
            "trend": "up" if aptitude_data["accuracy"] > 60 else "stable",
            "has_data": aptitude_data["has_data"]
        })
        
        # Coding
        modules.append({
            "module": "Coding",
            "sessions": coding_data["sessions_count"],
            "performance_level": "Good" if coding_data["success_rate"] >= 60 else "Moderate" if coding_data["success_rate"] >= 40 else "Low",
            "performance_score": coding_data["success_rate"],
            "progress_percentage": coding_data["progress_percentage"],
            "last_practiced": coding_data["last_practiced"],
            "trend": "up" if coding_data["success_rate"] > 50 else "stable",
            "has_data": coding_data["has_data"]
        })
        
        # Technical Interview
        modules.append({
            "module": "Technical Interview",
            "sessions": interview_data["technical_sessions"],
            "performance_level": "Good" if interview_data["technical_score"] >= 70 else "Moderate" if interview_data["technical_score"] >= 50 else "Low",
            "performance_score": interview_data["technical_score"],
            "last_practiced": interview_data["last_practiced"],
            "trend": "up" if interview_data["technical_score"] > 60 else "stable",
            "has_data": interview_data["technical_sessions"] > 0
        })
        
        # HR Interview
        modules.append({
            "module": "HR Interview",
            "sessions": interview_data["hr_sessions"],
            "performance_level": "Good" if interview_data["hr_score"] >= 70 else "Moderate" if interview_data["hr_score"] >= 50 else "Low",
            "performance_score": interview_data["hr_score"],
            "last_practiced": interview_data["last_practiced"],
            "trend": "stable",
            "has_data": interview_data["hr_sessions"] > 0
        })
        
        # Video Presence
        modules.append({
            "module": "Video Presence",
            "sessions": interview_data["video_presence_sessions"],
            "performance_level": "Good" if interview_data["video_presence_score"] >= 70 else "Moderate" if interview_data["video_presence_score"] >= 50 else "Low",
            "performance_score": interview_data["video_presence_score"],
            "last_practiced": interview_data["last_practiced"],
            "trend": "stable",
            "has_data": interview_data["video_presence_sessions"] > 0
        })
        
        return modules
    
    @staticmethod
    def _aggregate_skill_breakdown(aptitude_data: Dict, coding_data: Dict, interview_data: Dict) -> List[Dict]:
        """Aggregate data into skill categories"""
        skills = []
        
        # Problem Solving (Aptitude + Coding)
        problem_solving_score = 0
        if aptitude_data["has_data"] and coding_data["has_data"]:
            problem_solving_score = (aptitude_data["accuracy"] + coding_data["success_rate"]) / 2
        elif aptitude_data["has_data"]:
            problem_solving_score = aptitude_data["accuracy"]
        elif coding_data["has_data"]:
            problem_solving_score = coding_data["success_rate"]
        
        skills.append({
            "skill": "Problem Solving",
            "score": round(problem_solving_score, 1),
            "level": "Good" if problem_solving_score >= 70 else "Moderate" if problem_solving_score >= 50 else "Low"
        })
        
        # Technical Knowledge (Coding + Technical Interview)
        technical_score = 0
        if coding_data["has_data"] and interview_data["technical_sessions"] > 0:
            technical_score = (coding_data["success_rate"] + interview_data["average_score"]) / 2
        elif coding_data["has_data"]:
            technical_score = coding_data["success_rate"]
        elif interview_data["technical_sessions"] > 0:
            technical_score = interview_data["average_score"]
        
        skills.append({
            "skill": "Technical Knowledge",
            "score": round(technical_score, 1),
            "level": "Good" if technical_score >= 70 else "Moderate" if technical_score >= 50 else "Low"
        })
        
        # Communication (HR + GD)
        communication_score = interview_data["average_score"] if interview_data["hr_sessions"] > 0 else 0
        skills.append({
            "skill": "Communication",
            "score": round(communication_score, 1),
            "level": "Good" if communication_score >= 70 else "Moderate" if communication_score >= 50 else "Low"
        })
        
        # Video Presence (Aggregated)
        confidence_score = interview_data.get("average_score", 0) if interview_data["video_presence_sessions"] > 0 else 0
        skills.append({
            "skill": "Video Presence",
            "score": round(confidence_score, 1),
            "level": "Good" if confidence_score >= 70 else "Moderate" if confidence_score >= 50 else "Low"
        })
        
        # Consistency / Practice Habit
        consistency_score = 0
        total_sessions = aptitude_data["sessions_count"] + coding_data["sessions_count"] + interview_data["total_sessions"]
        if total_sessions >= 20:
            consistency_score = 80
        elif total_sessions >= 10:
            consistency_score = 60
        elif total_sessions >= 5:
            consistency_score = 40
        
        skills.append({
            "skill": "Practice Consistency",
            "score": round(consistency_score, 1),
            "level": "Good" if consistency_score >= 70 else "Moderate" if consistency_score >= 50 else "Low"
        })
        
        return skills
    
    @staticmethod
    def _identify_weak_areas(aptitude_data: Dict, coding_data: Dict, interview_data: Dict) -> List[Dict]:
        """Identify top weak areas across all modules with actionable suggestions"""
        weak_areas = []
        
        # Aptitude weak topics
        for topic in aptitude_data["weak_topics"]:
            weak_areas.append({
                "area": topic,
                "module": "Aptitude",
                "suggestion": f"Practice more {topic} questions",
                "action": "practice_aptitude"
            })
        
        # Coding weak areas
        if coding_data["has_data"] and coding_data["success_rate"] < 50:
            weak_areas.append({
                "area": "Coding Problem Solving",
                "module": "Coding",
                "suggestion": "Focus on solving easier problems first",
                "action": "practice_coding"
            })
        
        # Interview weak areas
        for area in interview_data["weak_areas"]:
            weak_areas.append({
                "area": area,
                "module": "Interview",
                "suggestion": f"Review {area} concepts",
                "action": "practice_interview"
            })
        
        # Return top 3
        return weak_areas[:3]
    
    @staticmethod
    def _get_recent_activity(db: Session, user_id: str, aptitude_data: Dict, coding_data: Dict, interview_data: Dict) -> List[Dict]:
        """Get recent activity timeline across all modules"""
        activities = []
        
        try:
            # Get recent aptitude attempts
            recent_aptitude = db.query(MockTestAttempt)\
                .filter(MockTestAttempt.user_id == user_id)\
                .filter(MockTestAttempt.status == "completed")\
                .order_by(MockTestAttempt.completed_at.desc())\
                .limit(5).all()
            
            for attempt in recent_aptitude:
                activities.append({
                    "module": "Aptitude",
                    "type": "Mock Test",
                    "date": attempt.completed_at.isoformat() if attempt.completed_at else None,
                    "result": f"{round(attempt.accuracy_percentage, 1)}% accuracy",
                    "score": attempt.accuracy_percentage
                })
            
            # Get recent coding submissions
            recent_coding = db.query(UserCodingProgress)\
                .filter(UserCodingProgress.user_id == user_id)\
                .order_by(UserCodingProgress.last_submission_date.desc())\
                .limit(5).all()
            
            for submission in recent_coding:
                if submission.last_submission_date:
                    activities.append({
                        "module": "Coding",
                        "type": "Problem Solved" if submission.is_solved else "Problem Attempted",
                        "date": submission.last_submission_date.isoformat(),
                        "result": "Solved" if submission.is_solved else f"{submission.attempts} attempts",
                        "score": 100 if submission.is_solved else 0
                    })
            
            # Get recent interview sessions
            from routes.interview import get_engine
            engine = get_engine()
            user_sessions = [
                session for session in engine.sessions.values()
                if session.get("user_id") == user_id
            ]
            
            # Sort by start time desc
            user_sessions.sort(key=lambda x: str(x.get("start_time", "")), reverse=True)
            
            for session in user_sessions[:5]:
                start_time = session.get("start_time")
                if start_time:
                    # Convert to ISO string if it's a datetime object
                    date_str = start_time.isoformat() if hasattr(start_time, "isoformat") else str(start_time)
                    
                    scores = session.get("scores", [])
                    avg_score = round(sum(scores) / len(scores), 1) if scores else 0
                    
                    category = session.get("interview_type", "Interview")
                    # Map category names for UI
                    display_category = {
                        "technical": "Technical Interview",
                        "hr": "HR Interview",
                        "video-practice": "Video Presence"
                    }.get(category, category.title())
                    
                    activities.append({
                        "module": display_category,
                        "type": "Practice Session",
                        "date": date_str,
                        "result": f"{avg_score}% score",
                        "score": avg_score
                    })
            
            # Sort all activities by date (most recent first)
            # Need to handle potential None dates
            activities.sort(key=lambda x: x["date"] if x.get("date") else "", reverse=True)
            
            # Return top 10 most recent
            return activities[:10]
            
        except Exception as e:
            print(f"[UnifiedAnalytics] Error getting recent activity: {e}")
            return activities # Return what we have so far
