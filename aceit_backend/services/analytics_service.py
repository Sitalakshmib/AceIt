"""
Analytics Service

Generates comprehensive user analytics, performance metrics, and personalized
recommendations based on practice and mock test performance.
"""

from sqlalchemy.orm import Session, joinedload
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
        print(f"[DEBUG] Step 1: Getting Aptitude Progress for {user_id}")
        # 1. Get Aptitude Progress
        progress_records = db.query(UserAptitudeProgress)\
            .filter(UserAptitudeProgress.user_id == user_id).all()
        print(f"[DEBUG] Got {len(progress_records)} progress records")
        
        # 2. Get Mock Test Attempts
        print("[DEBUG] Step 2: Getting Mock Test Attempts")
        mock_attempts = db.query(MockTestAttempt)\
            .filter(MockTestAttempt.user_id == user_id)\
            .filter(MockTestAttempt.status == "completed").all()
        print(f"[DEBUG] Got {len(mock_attempts)} mock attempts")

        # 3. Calculate Overall Stats
        print("[DEBUG] Step 3: Calculating Overall Stats")
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
        print("[DEBUG] Step 4: Aptitude Details")
        aptitude_data = {
            "tests_taken": len(mock_attempts),
            "average_score": round(sum(a.accuracy_percentage for a in mock_attempts) / len(mock_attempts), 1) if mock_attempts else 0,
            "best_score": round(max((a.accuracy_percentage for a in mock_attempts), default=0), 1),
            "total_questions_attempted": total_attempted,
            "accuracy": round(accuracy, 1)
        }

        # 5. Skill Distribution (Categories based + Coding as one)
        print("[DEBUG] Step 5: Skill Distribution")
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
            pass

        # 6. Recent Activity (Grouped by module with sub-items)
        print("[DEBUG] Step 6: Recent Activity")
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
        # Use simple query, no join needed if we just use stored category/topic for stats?
        # But this loop uses 'att.topic'. 
        recent_practice = db.query(QuestionAttempt)\
            .filter(QuestionAttempt.user_id == user_id)\
            .order_by(QuestionAttempt.attempted_at.desc())\
            .limit(10).all()
        
        # Group practice by topic for cleaner display
        topic_stats = {}
        for att in recent_practice:
            # OPTIMIZATION: Use stored topic directly
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
        
        # Convert to list format for frontend
        recent_activity = []
        for module_name, module_data in recent_activity_by_module.items():
            recent_activity.append({
                "module": module_name,
                "icon": module_data["icon"],
                "items": module_data["items"][:5]
            })

        print("[DEBUG] Step 6.5: Practice Metrics")
        # --- PRACTICE METRICS (QuestionAttempt) ---
        # OPTIMIZATION: Avoid join if we trust stored columns
        practice_attempts = db.query(QuestionAttempt)\
            .filter(QuestionAttempt.user_id == user_id).all()
        print(f"[DEBUG] Found {len(practice_attempts)} practice attempts")
        
        practice_stats = AnalyticsService.calculate_section_stats(practice_attempts, is_mock=False)
        
        print("[DEBUG] Step 6.8: Mock Metrics")
        # --- MOCK METRICS (MockTestResponse) ---
        # OPTIMIZATION: Eager load question to prevent N+1 in calculate_section_stats
        mock_responses = db.query(MockTestResponse)\
            .join(MockTestAttempt)\
            .options(joinedload(MockTestResponse.question))\
            .filter(MockTestAttempt.user_id == user_id)\
            .filter(MockTestAttempt.status == "completed").all()
        print(f"[DEBUG] Found {len(mock_responses)} mock responses")
            
        mock_stats = AnalyticsService.calculate_section_stats(mock_responses, is_mock=True)
        
        # Determine Strengths and Weaknesses
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

        # 7. Weekly Activity (Last 7 Days)
        print("[DEBUG] Step 7: Weekly Activity")
        weekly_stats = AnalyticsService.get_progress_history(db, user_id, days=7)
        weekly_activity = weekly_stats.get("daily_progress", [])

        # 8. Recommendations
        print("[DEBUG] Step 8: Recommendations")
        # Prepare data for recommendations
        weak_topics = [t["topic"] for t in improvements[:3]]
        
         # Ensure category_stats used in recommendations has accuracy
        recommendation_cat_stats = {}
        for cat, stats in category_scores.items():
            acc = (stats["correct"] / stats["total"] * 100) if stats["total"] > 0 else 0
            recommendation_cat_stats[cat] = {"accuracy": acc, "total": stats["total"]}

        recommendations = AnalyticsService.generate_recommendations(
            weak_topics=weak_topics,
            category_stats=recommendation_cat_stats,
            progress_records=progress_records
        )
        print("[DEBUG] Finished Recommendation Generation")

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
            # For QuestionAttempt, category/topic are on the object
            # For MockTestResponse, we need to access via 'question' relationship (should be eager loaded)
            
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
            
        # OPTIMIZATION: Eager load question relations for mock responses
        mock_responses = db.query(MockTestResponse)\
            .join(MockTestAttempt)\
            .options(joinedload(MockTestResponse.question))\
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
            
            # OPTIMIZATION: Use stored category directly, do NOT query AptitudeQuestion
            cat = attempt.category or "Unknown"
            
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
            
            # Get question category (eager loaded)
            cat = "Unknown"
            if response.question:
                cat = response.question.category or "Unknown"

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
