from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, Integer, cast, DateTime
from models.mock_test_sql import MockTestAttempt, MockTestResponse, MockTest
from models.analytics_sql import QuestionAttempt
import datetime
from typing import List, Dict, Optional
import os
import json
from models.user_sql import User  # Fix for relationship resolution
from models.aptitude_sql import AptitudeQuestion # Fix for cascading relationship resolution

class AIAnalyticsService:
    @staticmethod
    def get_daily_mock_progress(db: Session, user_id: str, days: int = 7) -> List[Dict]:
        """
        Aggregate mock test accuracy on a daily basis for the last X days.
        Adjusts for UTC+5:30 (IST) to match user local date.
        """
        tz_offset = datetime.timedelta(hours=5, minutes=30)
        end_date = datetime.datetime.utcnow()
        start_date = end_date - datetime.timedelta(days=days + 1)
        
        # Query attempts in the range
        attempts = db.query(MockTestAttempt).filter(
            MockTestAttempt.user_id == user_id,
            MockTestAttempt.status == "completed",
            MockTestAttempt.completed_at >= start_date
        ).all()
        
        daily_stats = {}
        for a in attempts:
            if not a.completed_at: continue
            local_date = (a.completed_at + tz_offset).date().isoformat()
            if local_date not in daily_stats:
                daily_stats[local_date] = {"total_accuracy": 0, "count": 0}
            daily_stats[local_date]["total_accuracy"] += (a.accuracy_percentage or 0)
            daily_stats[local_date]["count"] += 1
            
        result = []
        # Sort by date for the chart
        for date_str in sorted(daily_stats.keys()):
            stats = daily_stats[date_str]
            result.append({
                "date": date_str,
                "accuracy": round(stats["total_accuracy"] / stats["count"], 1),
                "count": stats["count"]
            })
            
        return result[-days:] if days > 0 else result

    @staticmethod
    def get_mock_topic_performance(db: Session, user_id: str) -> Dict:
        """
        Extract strengths and weaknesses using optimized SQL aggregation.
        """
        from models.aptitude_sql import AptitudeQuestion
        
        # Use SQL aggregation instead of fetching all rows
        results = db.query(
            AptitudeQuestion.topic,
            func.count(MockTestResponse.id).label("total"),
            func.sum(cast(MockTestResponse.is_correct, Integer)).label("correct")
        ).join(
            MockTestResponse, AptitudeQuestion.id == MockTestResponse.question_id
        ).join(
            MockTestAttempt, MockTestResponse.attempt_id == MockTestAttempt.id
        ).filter(
            MockTestAttempt.user_id == user_id,
            MockTestAttempt.status == "completed"
        ).group_by(
            AptitudeQuestion.topic
        ).all()
        
        if not results:
            return {"strengths": [], "weaknesses": [], "topic_data": {}}
            
        topic_map = {}
        strengths = []
        weaknesses = []
        
        for r in results:
            topic = r.topic or "Miscellaneous"
            correct = int(r.correct or 0)
            total = int(r.total or 0)
            acc = (correct / total) * 100 if total > 0 else 0
            
            topic_map[topic] = {
                "correct": correct,
                "total": total,
                "accuracy": round(acc, 1)
            }
            
            if acc >= 75 and total >= 3:
                strengths.append(topic)
            elif acc < 50:
                weaknesses.append(topic)
                
        return {
            "strengths": strengths,
            "weaknesses": weaknesses,
            "topic_data": topic_map
        }

    @staticmethod
    def get_overall_summary(db: Session, user_id: str) -> Dict:
        """
        Calculate the high-level summary cards based on actual mock test data.
        """
        # UTC+5:30 Adjustment for Streak & Stats
        tz_offset = datetime.timedelta(hours=5, minutes=30)
        
        attempts_all = db.query(MockTestAttempt).filter(
            MockTestAttempt.user_id == user_id,
            MockTestAttempt.status == "completed"
        ).order_by(MockTestAttempt.completed_at.desc()).all()
        
        if not attempts_all:
            return {
                "exam_confidence": 0,
                "mastered_topics": 0,
                "pace_ratio": 1.0,
                "avg_time_per_q": 60,
                "total_mocks": 0,
                "questions_solved": 0,
                "current_streak": 0
            }

        # 1. Exam Confidence & Pace (7-Day Window)
        start_date = datetime.datetime.utcnow() - datetime.timedelta(days=7)
        attempts_recent = [a for a in attempts_all if a.completed_at and a.completed_at >= start_date]
        perf_attempts = attempts_recent if attempts_recent else attempts_all
        
        avg_accuracy = sum(a.accuracy_percentage or 0 for a in perf_attempts) / len(perf_attempts)
        
        perf_ids = [a.id for a in perf_attempts]
        total_seconds = sum(a.time_taken_seconds or 0 for a in perf_attempts)
        total_answered_recent = db.query(func.count(MockTestResponse.id)).filter(
            MockTestResponse.attempt_id.in_(perf_ids)
        ).scalar() or 0
        
        avg_time_per_q = total_seconds / total_answered_recent if total_answered_recent > 0 else 60
        pace_ratio = round(60 / avg_time_per_q, 1) if avg_time_per_q > 5 else 2.5
        pace_ratio = min(max(pace_ratio, 0.5), 3.0)

        # 2. Mastered Topics (All Time)
        topic_perf = AIAnalyticsService.get_mock_topic_performance(db, user_id)
        mastered_count = len(topic_perf.get("strengths", []))
        
        # 3. Overall Questions Solved
        all_ids = [a.id for a in attempts_all]
        total_answered_all = db.query(func.count(MockTestResponse.id)).filter(
            MockTestResponse.attempt_id.in_(all_ids)
        ).scalar() or 0

        # 4. Streak Logic (Local Time adjusted)
        activity_dates = set()
        for a in attempts_all:
            if a.completed_at: activity_dates.add((a.completed_at + tz_offset).date())
        
        practice_dates = db.query(QuestionAttempt.attempted_at).filter(
            QuestionAttempt.user_id == user_id
        ).all()
        for d in practice_dates:
            if d[0]: activity_dates.add((d[0] + tz_offset).date())
            
        today_local = (datetime.datetime.utcnow() + tz_offset).date()
        streak = 0
        if today_local in activity_dates:
            streak = 1
            check_date = today_local - datetime.timedelta(days=1)
        else:
            # Check if streak intact from yesterday
            check_date = today_local - datetime.timedelta(days=1)
            if check_date in activity_dates:
                streak = 1
                check_date = check_date - datetime.timedelta(days=1)
            else:
                streak = 0
                check_date = None
        
        while streak > 0 and check_date and check_date in activity_dates:
            streak += 1
            check_date -= datetime.timedelta(days=1)
            
        return {
            "exam_confidence": round(avg_accuracy, 1),
            "mastered_topics": mastered_count,
            "pace_ratio": pace_ratio,
            "avg_time_per_q": round(avg_time_per_q, 1),
            "total_mocks": len(attempts_all),
            "questions_solved": total_answered_all,
            "current_streak": streak
        }
        


    @staticmethod
    def generate_ai_insight(db: Session, user_id: str) -> Dict:
        """
        Query OpenAI to analyze daily trends and provide strategic advice.
        Includes a caching layer to reduce latency and costs.
        """
        from models.analytics_sql import UserAnalytics
        
        # 1. Check if we have a fresh cache
        # We only re-run AI if there's a new mock test since the last generation
        latest_test = db.query(MockTestAttempt.completed_at).filter(
            MockTestAttempt.user_id == user_id,
            MockTestAttempt.status == "completed"
        ).order_by(MockTestAttempt.completed_at.desc()).first()
        
        if not latest_test:
            return {
                "headline": "Ready to Start?",
                "analysis": "You haven't completed any mock tests yet. Starting a diagnostic mock test is the best way to activate your AI Tutor.",
                "action_plan": ["Take a Mock test.", " establece a baseline.", "Review results."]
            }

        user_anal = db.query(UserAnalytics).filter(UserAnalytics.user_id == user_id).first()
        
        # Cache is valid if: We have an insight AND it was generated AFTER the latest test
        if user_anal and user_anal.last_ai_insight and user_anal.last_ai_generated_at:
            if user_anal.last_ai_generated_at >= latest_test.completed_at:
                return user_anal.last_ai_insight

        # 2. Get performance data for context
        daily_data = AIAnalyticsService.get_daily_mock_progress(db, user_id, days=7)
        topic_data = AIAnalyticsService.get_mock_topic_performance(db, user_id)
        summary_data = AIAnalyticsService.get_overall_summary(db, user_id)
        
        # Get specific details of the last test for even more "real" feedback
        last_test_full = db.query(MockTestAttempt).filter(
            MockTestAttempt.user_id == user_id,
            MockTestAttempt.status == "completed"
        ).order_by(MockTestAttempt.completed_at.desc()).first()
        
        # Prepare context for AI
        context = {
            "daily_trends": daily_data,
            "strengths": topic_data["strengths"],
            "weaknesses": topic_data["weaknesses"],
            "pace_ratio": summary_data["pace_ratio"],
            "accuracy_percentage": summary_data["exam_confidence"],
            "total_mocks": summary_data["total_mocks"],
            "last_test": {
                "score": f"{last_test_full.score}/{last_test_full.total_questions}" if last_test_full else "N/A",
                "accuracy": f"{last_test_full.accuracy_percentage}%" if last_test_full else "N/A",
                "date": last_test_full.completed_at.strftime("%Y-%m-%d") if last_test_full else "N/A"
            },
            "best_topic": max(topic_data["topic_data"].items(), key=lambda x: x[1]["accuracy"])[0] if topic_data["topic_data"] else "N/A"
        }
        
        # 3. Call AI (Groq via SITA Key, OpenAI SITA Key Backup)
        from services.llm_client import LLMClient
        llm = LLMClient(groq_env_key="GROQ_API_KEY_SITA", openai_env_key="OPENAI_API_KEY_SITA")
        
        try:
            prompt = f"""
            You are an expert Aptitude Career Coach. Student data:
            - ACCURACY: {context['accuracy_percentage']}%
            - PACE: {context['pace_ratio']}x
            - LATEST MOCK TEST: Score {context['last_test']['score']} on {context['last_test']['date']} (Accuracy: {context['last_test']['accuracy']})
            - STRENGTHS: {', '.join(context['strengths']) if context['strengths'] else 'None yet'}
            - WEAKNESSES: {', '.join(context['weaknesses']) if context['weaknesses'] else 'None yet'}
            - BEST TOPIC: {context['best_topic']}
            - RECENT TRENDS: {json.dumps(context['daily_trends'])}

            INSTRUCTION: Your analysis MUST reference the 'LATEST MOCK TEST' data specifically to show you are tracking real-time progress.
            Return ONLY valid JSON (no markdown) with keys: "headline" (1 sentence), "analysis" (2 sentences mentioning specific topics), "action_plan" (list of 3 steps).
            """
            
            response_text = llm.generate_response(prompt)
            
            # Clean response
            clean_text = response_text.replace("```json", "").replace("```", "").strip()
            insight_data = json.loads(clean_text)
            
            # 4. Save to cache
            if not user_anal:
                user_anal = UserAnalytics(user_id=user_id)
                db.add(user_anal)
            
            user_anal.last_ai_insight = insight_data
            user_anal.last_ai_generated_at = datetime.datetime.utcnow()
            db.commit()
            
            return insight_data
            
        except Exception as e:
            db.rollback()
            print(f"[ERROR] OpenAI Insights failed: {e}")
            # Fallback (as before)
            return {
                "headline": f"Keep pushing in {context['best_topic']}!",
                "analysis": f"Your current accuracy is {summary_data['exam_confidence']}%.",
                "action_plan": ["Focus on weak topics.", "Improve speed.", "Take daily mocks."]
            }
