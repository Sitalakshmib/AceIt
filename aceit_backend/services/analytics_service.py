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
        
        # Calculate average time per question (in seconds)
        total_time_seconds = sum(p.total_time_spent_seconds or 0 for p in progress_records)
        avg_time_per_question = round(total_time_seconds / total_attempted, 1) if total_attempted > 0 else 0
        
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

        # 5. Skill Distribution (Categories based + Coding as one)
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
        
        # Add Coding as a single module (placeholder - update when coding module has data)
        # For now, use a placeholder or fetch from coding progress if available
        coding_score = 0  # This can be updated when coding module has progress tracking
        if coding_score > 0 or True:  # Always show Coding in distribution
            skill_distribution.append({
                "name": "Coding",
                "score": coding_score
            })
        
        # Import in-memory progress data
        try:
            from database import progress_data
        except ImportError:
            progress_data = []

        # 6. Recent Activity (Grouped by module with sub-items)
        # Structure: { "module_name": { "icon": "...", "items": [...] } }
        recent_activity_by_module = {
            "Aptitude": {"icon": "brain", "items": []},
            "Coding": {"icon": "code", "items": []},
            "Resume": {"icon": "file", "items": []},
            "Interview": {"icon": "mic", "items": []}
        }
        
        # Mock test completions -> Aptitude
        for a in mock_attempts[:5]:  # Limit to recent 5
            if a.completed_at:
                recent_activity_by_module["Aptitude"]["items"].append({
                    "type": "mock_test",
                    "title": "Mock Test",
                    "subtitle": f"{a.score}/{a.total_questions} correct",
                    "score": round(a.accuracy_percentage, 1),
                    "date": a.completed_at.strftime("%Y-%m-%d %H:%M"),
                    "success": a.accuracy_percentage >= 50
                })
        
        # Practice question attempts -> Aptitude
        recent_practice = db.query(QuestionAttempt)\
            .filter(QuestionAttempt.user_id == user_id)\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(10).all()
        
        # Group practice by topic for cleaner display
        topic_stats = {}
        for att in recent_practice:
            topic = (att.topic or "General").replace("_", " ")
            if topic not in topic_stats:
                topic_stats[topic] = {"correct": 0, "total": 0, "last_date": att.attempted_at}
            topic_stats[topic]["total"] += 1
            if att.is_correct:
                topic_stats[topic]["correct"] += 1
        
        for topic, stats in topic_stats.items():
            accuracy = round((stats["correct"] / stats["total"]) * 100) if stats["total"] > 0 else 0
            recent_activity_by_module["Aptitude"]["items"].append({
                "type": "practice",
                "title": topic,
                "subtitle": f"{stats['correct']}/{stats['total']} correct",
                "score": accuracy,
                "date": stats["last_date"].strftime("%Y-%m-%d"),
                "success": accuracy >= 50
            })
        
        # Coding progress from in-memory progress_data
        coding_records = [p for p in progress_data if p.get("module") == "coding" and p.get("user_id") == user_id]
        coding_records = sorted(coding_records, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]
        for record in coding_records:
            recent_activity_by_module["Coding"]["items"].append({
                "type": "submission",
                "title": record.get("problem_title", "Problem"),
                "subtitle": f"{record.get('passed_tests', 0)}/{record.get('total_tests', 0)} tests passed",
                "score": round(record.get("percentage", 0), 1),
                "date": record.get("timestamp", "")[:10] if record.get("timestamp") else "Unknown",
                "success": record.get("percentage", 0) >= 50
            })
        
        # Resume progress from in-memory progress_data
        resume_records = [p for p in progress_data if p.get("module") == "resume" and p.get("user_id") == user_id]
        resume_records = sorted(resume_records, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]
        for record in resume_records:
            recent_activity_by_module["Resume"]["items"].append({
                "type": "analysis",
                "title": record.get("job_role", "Resume").replace("_", " ").title(),
                "subtitle": f"ATS Score: {record.get('ats_score', 0)}%",
                "score": round(record.get("ats_score", 0), 1),
                "date": record.get("timestamp", "")[:10] if record.get("timestamp") else "Unknown",
                "success": record.get("ats_score", 0) >= 50
            })
        
        # Interview progress from in-memory progress_data
        interview_records = [p for p in progress_data if p.get("module") == "interview" and p.get("user_id") == user_id]
        interview_records = sorted(interview_records, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]
        for record in interview_records:
            recent_activity_by_module["Interview"]["items"].append({
                "type": "session",
                "title": record.get("interview_type", "Interview").title(),
                "subtitle": f"Session completed",
                "score": round(record.get("score", 0), 1),
                "date": record.get("timestamp", "")[:10] if record.get("timestamp") else "Unknown",
                "success": True
            })
        
        # Convert to list format for frontend (include all modules even if empty)
        recent_activity = []
        for module_name, module_data in recent_activity_by_module.items():
            recent_activity.append({
                "module": module_name,
                "icon": module_data["icon"],
                "items": module_data["items"][:5]  # Limit to 5 items per module
            })

        # --- PRACTICE METRICS (QuestionAttempt) ---
        practice_attempts = db.query(QuestionAttempt)\
            .join(AptitudeQuestion, QuestionAttempt.question_id == AptitudeQuestion.id)\
            .filter(QuestionAttempt.user_id == user_id).all()
        
        practice_stats = AnalyticsService.calculate_section_stats(practice_attempts, is_mock=False)
        
        # --- MOCK METRICS (MockTestResponse) ---
        mock_responses = db.query(MockTestResponse)\
            .join(MockTestAttempt)\
            .filter(MockTestAttempt.user_id == user_id)\
            .filter(MockTestAttempt.status == "completed").all()
            
        mock_stats = AnalyticsService.calculate_section_stats(mock_responses, is_mock=True)
        
        # Determine Strengths and Weaknesses (Combined or Practice preferred? Let's use combined relative accuracy)
        # Actually user wants to know "which all sections which all topic the user is good and need improvement"
        # We'll generate this based on the COMBINED performance to give a holistic view
        
        combined_topic_stats = {}
        # Merge practice stats
        for topic, stats in practice_stats.get("topic_breakdown", {}).items():
             combined_topic_stats[topic] = stats.copy()
             
        # Merge mock stats
        for topic, stats in mock_stats.get("topic_breakdown", {}).items():
            if topic not in combined_topic_stats:
                combined_topic_stats[topic] = stats.copy()
            else:
                combined_topic_stats[topic]["correct"] += stats["correct"]
                combined_topic_stats[topic]["total"] += stats["total"]
                # Recompute accuracy
                total = combined_topic_stats[topic]["total"]
                correct = combined_topic_stats[topic]["correct"]
                combined_topic_stats[topic]["accuracy"] = (correct / total * 100) if total > 0 else 0

        strengths = []
        improvements = []
        
        for topic, stats in combined_topic_stats.items():
            acc = stats["accuracy"]
            item = {
                "topic": topic,
                "accuracy": round(acc, 1),
                "total": stats["total"]
            }
            if acc >= 80:
                strengths.append(item)
            elif acc < 60:
                improvements.append(item)
                
        # Sort by accuracy
        strengths.sort(key=lambda x: x["accuracy"], reverse=True)
        improvements.sort(key=lambda x: x["accuracy"]) # Lowest first

        return {
            "user_id": user_id,
            "overall_score": round(accuracy, 1),
            "daily_streak": streak,
            "total_time_spent": total_time,
            "tests_completed": len(mock_attempts),
            "avg_time_per_question": avg_time_per_question,
            
            # New Separate Metrics
            "practice_metrics": practice_stats,
            "mock_metrics": mock_stats,
            
            # Insight Lists
            "strengths": strengths,
            "areas_for_improvement": improvements,
            
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
    def calculate_section_stats(records, is_mock=False):
        """
        Helper to calculate stats for a set of attempts/responses
        """
        total_attempts = len(records)
        correct_attempts = sum(1 for r in records if r.is_correct)
        accuracy = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        # Breakdown
        category_stats = {}
        topic_stats = {}
        
        for r in records:
            # For QuestionAttempt, category/topic are on the object (we joined in query)
            # For MockTestResponse, we need to access via 'question' relationship or similar
            # In the query above for practice_attempts, we joined AptitudeQuestion but result is QuestionAttempt object? 
            # SQLAlchemy result depends on query. returning .all() on QuestionAttempt returns attempt objects.
            # but we can access question relationship if defined.
            # Let's assume r.question is available or fields are present. 
            
            # Wait, QuestionAttempt model doesn't have relationship defined in the snippet I saw?
            # actually models/analytics_sql.py shows ForeignKey but no relationship property.
            # I must rely on the fields I saw: category, topic are columns in QuestionAttempt!
            
            cat = None
            top = None
            
            if is_mock:
                # r is MockTestResponse. It has 'question' relationship.
                if r.question:
                    cat = r.question.category
                    top = r.question.topic
            else:
                # r is QuestionAttempt. It has 'category' and 'topic' columns.
                cat = r.category
                top = r.topic
                
            if not cat: cat = "Unknown"
            if not top: top = "Unknown"
            
            # Category Update
            if cat not in category_stats:
                category_stats[cat] = {"correct": 0, "total": 0}
            category_stats[cat]["total"] += 1
            if r.is_correct:
                category_stats[cat]["correct"] += 1
                
            # Topic Update
            if top not in topic_stats:
                topic_stats[top] = {"correct": 0, "total": 0}
            topic_stats[top]["total"] += 1
            if r.is_correct:
                topic_stats[top]["correct"] += 1

        # Calculate Accuracies
        for c in category_stats:
            t = category_stats[c]["total"]
            category_stats[c]["accuracy"] = (category_stats[c]["correct"] / t * 100) if t > 0 else 0
            
        for t in topic_stats:
            tot = topic_stats[t]["total"]
            topic_stats[t]["accuracy"] = (topic_stats[t]["correct"] / tot * 100) if tot > 0 else 0
            
        return {
            "total_questions": total_attempts,
            "accuracy": round(accuracy, 1),
            "category_breakdown": category_stats,
            "topic_breakdown": topic_stats
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
            
        mock_responses = db.query(MockTestResponse)\
            .join(MockTestAttempt)\
            .filter(MockTestAttempt.user_id == user_id)\
            .filter(MockTestResponse.answered_at >= cutoff_date)\
            .order_by(MockTestResponse.answered_at).all()
        
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
        
        # Merge mock responses
        for response in mock_responses:
            if not response.answered_at:
                continue
            date = response.answered_at.date()
            if date not in daily_stats:
                daily_stats[date] = {
                    "attempted": 0,
                    "correct": 0,
                    "categories": {}
                }
            daily_stats[date]["attempted"] += 1
            if response.is_correct:
                daily_stats[date]["correct"] += 1
            
            # Get question category
            question = db.query(AptitudeQuestion).filter(
                AptitudeQuestion.id == response.question_id
            ).first()
            if question:
                cat = question.category
                if cat not in daily_stats[date]["categories"]:
                    daily_stats[date]["categories"][cat] = {"attempted": 0, "correct": 0}
                daily_stats[date]["categories"][cat]["attempted"] += 1
                if response.is_correct:
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
