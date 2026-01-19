"""
Analytics Service

Generates comprehensive user analytics, performance metrics, and personalized
recommendations based on practice and mock test performance.
"""

from sqlalchemy.orm import Session
from sqlalchemy import func
from models.aptitude_sql import UserAptitudeProgress, AptitudeQuestion
from models.analytics_sql import QuestionAttempt, UserAnalytics
from models.mock_test_sql import MockTestAttempt, MockTestResponse
from typing import Dict, List
import datetime


class AnalyticsService:
    """Generate user analytics and recommendations"""
    
    @staticmethod
    def generate_user_analytics(db: Session, user_id: str) -> Dict:
        """
        Generate comprehensive user analytics dashboard in the format expected by the frontend
        """
        # 1. Get Aptitude Progress
        progress_records = db.query(UserAptitudeProgress)\
            .filter(UserAptitudeProgress.user_id == user_id).all()
        
        # 2. Get Mock Test Attempts
        mock_attempts = db.query(MockTestAttempt)\
            .filter(MockTestAttempt.user_id == user_id)\
            .filter(MockTestAttempt.status == "completed").all()

        # 3. Calculate Overall Stats
        total_attempted = sum(p.questions_attempted or 0 for p in progress_records)
        total_correct = sum(p.questions_correct or 0 for p in progress_records)
        accuracy = (total_correct / total_attempted * 100) if total_attempted > 0 else 0
        total_time = sum(p.total_time_spent_seconds or 0 for p in progress_records) // 60
        
        # Streak (simplified for now)
        streak = max([p.streak or 0 for p in progress_records], default=0)

        # 4. Aptitude Details
        aptitude_data = {
            "tests_taken": len(mock_attempts),
            "average_score": round(sum(a.accuracy_percentage for a in mock_attempts) / len(mock_attempts), 1) if mock_attempts else 0,
            "best_score": round(max((a.accuracy_percentage for a in mock_attempts), default=0), 1),
            "total_questions_attempted": total_attempted,
            "accuracy": round(accuracy, 1)
        }

        # 5. Skill Distribution (Categories based)
        category_scores = {}
        for p in progress_records:
            if p.category not in category_scores:
                category_scores[p.category] = {"correct": 0, "total": 0}
            category_scores[p.category]["correct"] += p.questions_correct
            category_scores[p.category]["total"] += p.questions_attempted
        
        skill_distribution = []
        for cat, stats in category_scores.items():
            if stats["total"] > 0:
                skill_distribution.append({
                    "name": cat,
                    "score": round((stats["correct"] / stats["total"]) * 100, 1)
                })
        
        # 6. Recent Activity
        recent_activity = []
        
        # Add mock tests to activity
        for a in sorted(mock_attempts, key=lambda x: x.completed_at, reverse=True)[:3]:
            recent_activity.append({
                "type": "aptitude_test",
                "score": round(a.accuracy_percentage, 1),
                "date": a.completed_at.strftime("%Y-%m-%d") if a.completed_at else "Today",
                "duration": f"{a.time_taken_seconds // 60} min"
            })
            
        # Add practice attempts if not enough mock tests
        if len(recent_activity) < 5:
            recent_attempts = db.query(QuestionAttempt)\
                .filter(QuestionAttempt.user_id == user_id)\
                .order_by(QuestionAttempt.attempted_at.desc())\
                .limit(5 - len(recent_activity)).all()
            
            for att in recent_attempts:
                recent_activity.append({
                    "type": "practice_question",
                    "problem": att.topic or "Aptitude",
                    "success": att.is_correct,
                    "date": att.attempted_at.strftime("%Y-%m-%d"),
                    "score": 100 if att.is_correct else 0
                })

        # 7. Weekly Activity (Last 7 days)
        weekly_activity = []
        today = datetime.datetime.utcnow().date()
        for i in range(6, -1, -1):
            date = today - datetime.timedelta(days=i)
            # Count attempts for this day
            count = db.query(QuestionAttempt)\
                .filter(QuestionAttempt.user_id == user_id)\
                .filter(func.date(QuestionAttempt.attempted_at) == date).count()
            
            weekly_activity.append({
                "date": date.isoformat(),
                "aptitude": count,
                "coding": 0, # Placeholder
                "score": 0 # Placeholder for daily avg
            })

        # 8. Recommendations
        weak_topics = [p.topic for p in sorted(progress_records, key=lambda x: x.overall_accuracy)[:3] if p.overall_accuracy < 60]
        recommendations = [f"Practice more {topic} - accuracy is low." for topic in weak_topics]
        if not recommendations:
            recommendations = ["Great job! Keep practicing to maintain your streak.", "Try a Full-Length Mock Test to assess your readiness."]

        return {
            "user_id": user_id,
            "overall_score": round(accuracy, 1),
            "daily_streak": streak,
            "total_time_spent": total_time,
            "aptitude": aptitude_data,
            "coding": {
                "problems_attempted": 0,
                "average_success_rate": 0,
                "total_tests_passed": 0,
                "total_tests_attempted": 0
            },
            "recent_activity": recent_activity,
            "weekly_activity": weekly_activity,
            "skill_distribution": skill_distribution,
            "recommendations": recommendations[:5]
        }
    
    @staticmethod
    def generate_recommendations(
        weak_topics: List[str],
        category_stats: Dict,
        progress_records: List[UserAptitudeProgress]
    ) -> List[str]:
        """
        Generate personalized improvement recommendations
        
        Args:
            weak_topics: List of weak topic names
            category_stats: Category performance statistics
            progress_records: User progress records
            
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Topic-specific recommendations
        if weak_topics:
            recommendations.append(
                f"🎯 Focus on improving: {', '.join(weak_topics[:3])}"
            )
        
        # Category-specific recommendations
        for category, stats in category_stats.items():
            accuracy = stats["accuracy"]
            if accuracy < 50:
                recommendations.append(
                    f"📚 Practice more {category} questions to build fundamentals (current: {accuracy:.1f}%)"
                )
            elif accuracy < 70:
                recommendations.append(
                    f"📈 Work on medium and hard level {category} questions to improve (current: {accuracy:.1f}%)"
                )
            elif accuracy >= 85:
                recommendations.append(
                    f"⭐ Excellent performance in {category}! ({accuracy:.1f}%) - Try harder questions to challenge yourself"
                )
        
        # Difficulty progression recommendations
        for progress in progress_records:
            if progress.current_difficulty == "easy" and progress.questions_attempted >= 10:
                if progress.overall_accuracy >= 80:
                    recommendations.append(
                        f"🚀 You're ready for medium level {progress.topic} questions!"
                    )
            elif progress.current_difficulty == "medium" and progress.questions_attempted >= 15:
                if progress.overall_accuracy >= 75:
                    recommendations.append(
                        f"💪 Challenge yourself with hard {progress.topic} questions!"
                    )
        
        # Mock test recommendations
        if not recommendations:
            recommendations.append("✨ Keep practicing regularly to improve your skills!")
        
        return recommendations[:5]  # Limit to top 5 recommendations
    
    @staticmethod
    def get_progress_history(db: Session, user_id: str, days: int = 30) -> Dict:
        """
        Get user's progress over time
        
        Args:
            db: Database session
            user_id: User ID
            days: Number of days to look back
            
        Returns:
            Dictionary with daily progress statistics
        """
        cutoff_date = datetime.datetime.utcnow() - datetime.timedelta(days=days)
        
        attempts = db.query(QuestionAttempt)\
            .filter(QuestionAttempt.user_id == user_id)\
            .filter(QuestionAttempt.attempted_at >= cutoff_date)\
            .order_by(QuestionAttempt.attempted_at).all()
        
        # Group by date
        daily_stats = {}
        for attempt in attempts:
            date = attempt.attempted_at.date()
            if date not in daily_stats:
                daily_stats[date] = {
                    "attempted": 0,
                    "correct": 0,
                    "categories": {}
                }
            daily_stats[date]["attempted"] += 1
            if attempt.is_correct:
                daily_stats[date]["correct"] += 1
            
            # Get question category
            question = db.query(AptitudeQuestion).filter(
                AptitudeQuestion.id == attempt.question_id
            ).first()
            if question:
                cat = question.category
                if cat not in daily_stats[date]["categories"]:
                    daily_stats[date]["categories"][cat] = {"attempted": 0, "correct": 0}
                daily_stats[date]["categories"][cat]["attempted"] += 1
                if attempt.is_correct:
                    daily_stats[date]["categories"][cat]["correct"] += 1
        
        # Format for response
        daily_progress = []
        for date, stats in sorted(daily_stats.items()):
            accuracy = (stats["correct"] / stats["attempted"]) * 100 if stats["attempted"] > 0 else 0
            daily_progress.append({
                "date": str(date),
                "attempted": stats["attempted"],
                "correct": stats["correct"],
                "accuracy": round(accuracy, 2),
                "categories": stats["categories"]
            })
        
        return {
            "daily_progress": daily_progress,
            "total_days_active": len(daily_stats),
            "total_questions": sum(s["attempted"] for s in daily_stats.values())
        }
    
    @staticmethod
    def get_topic_analytics(db: Session, user_id: str, topic: str) -> Dict:
        """
        Get detailed analytics for a specific topic
        
        Args:
            db: Database session
            user_id: User ID
            topic: Topic name
            
        Returns:
            Dictionary with topic-specific analytics
        """
        progress = db.query(UserAptitudeProgress)\
            .filter(UserAptitudeProgress.user_id == user_id)\
            .filter(UserAptitudeProgress.topic == topic)\
            .first()
        
        if not progress:
            return {
                "topic": topic,
                "message": "No practice data available for this topic"
            }
        
        # Get recent attempts
        recent_attempts = db.query(QuestionAttempt)\
            .join(AptitudeQuestion, QuestionAttempt.question_id == AptitudeQuestion.id)\
            .filter(QuestionAttempt.user_id == user_id)\
            .filter(AptitudeQuestion.topic == topic)\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(20).all()
        
        # Difficulty breakdown
        difficulty_stats = {
            "easy": {
                "attempted": progress.easy_total,
                "correct": progress.easy_correct,
                "accuracy": (progress.easy_correct / progress.easy_total * 100) if progress.easy_total > 0 else 0
            },
            "medium": {
                "attempted": progress.medium_total,
                "correct": progress.medium_correct,
                "accuracy": (progress.medium_correct / progress.medium_total * 100) if progress.medium_total > 0 else 0
            },
            "hard": {
                "attempted": progress.hard_total,
                "correct": progress.hard_correct,
                "accuracy": (progress.hard_correct / progress.hard_total * 100) if progress.hard_total > 0 else 0
            }
        }
        
        return {
            "topic": topic,
            "category": progress.category,
            "current_difficulty": progress.current_difficulty,
            "overall_accuracy": round(progress.overall_accuracy, 2),
            "recent_accuracy": round(progress.recent_accuracy, 2),
            "total_attempted": progress.questions_attempted,
            "total_correct": progress.questions_correct,
            "current_streak": progress.streak,
            "difficulty_breakdown": difficulty_stats,
            "average_time_per_question": round(progress.average_time_per_question, 2),
            "last_practiced": progress.last_practiced.isoformat() if progress.last_practiced else None,
            "recent_attempts": [
                {
                    "is_correct": a.is_correct,
                    "difficulty": a.difficulty_at_attempt,
                    "time_spent": a.time_spent_seconds,
                    "attempted_at": a.attempted_at.isoformat()
                }
                for a in recent_attempts
            ]
        }
