from fastapi import APIRouter
from database import progress_data

router = APIRouter()

# Get user's overall progress and statistics
@router.get("/{user_id}")
def get_user_progress(user_id: str):
    """
    Get comprehensive progress data for a user
    """
    # Get all progress records for this user
    user_progress = [p for p in progress_data if p.get("user_id") == user_id]
    
    # Separate progress by module type
    aptitude_progress = [p for p in user_progress if p.get("module") == "aptitude"]
    coding_progress = [p for p in user_progress if p.get("module") == "coding"]
    
    # Calculate aptitude statistics
    aptitude_stats = {
        "tests_taken": len(aptitude_progress),
        "average_score": 0,
        "best_score": 0,
        "total_questions_attempted": 0
    }
    
    if aptitude_progress:
        total_score = sum(p.get("score", 0) for p in aptitude_progress)
        total_questions = sum(p.get("total_questions", 0) for p in aptitude_progress)
        if total_questions > 0:
            aptitude_stats["average_score"] = round((total_score / total_questions) * 100, 2)
        if aptitude_progress:
            aptitude_stats["best_score"] = max(p.get("percentage", 0) for p in aptitude_progress)
        aptitude_stats["total_questions_attempted"] = total_questions
    
    # Calculate coding statistics
    coding_stats = {
        "problems_attempted": len(coding_progress),
        "average_success_rate": 0,
        "total_tests_passed": 0,
        "total_tests_attempted": 0
    }
    
    if coding_progress:
        total_percentage = sum(p.get("percentage", 0) for p in coding_progress)
        total_passed = sum(p.get("passed_tests", 0) for p in coding_progress)
        total_tests = sum(p.get("total_tests", 0) for p in coding_progress)
        
        if coding_progress:
            coding_stats["average_success_rate"] = round(total_percentage / len(coding_progress), 2)
        coding_stats["total_tests_passed"] = total_passed
        coding_stats["total_tests_attempted"] = total_tests
    
    # Calculate overall progress score (weighted average)
    overall_score = 0
    if aptitude_stats["tests_taken"] > 0:
        overall_score += aptitude_stats["average_score"] * 0.4  # 40% weight for aptitude
    if coding_stats["problems_attempted"] > 0:
        overall_score += coding_stats["average_success_rate"] * 0.6  # 60% weight for coding
    
    # Get recent activity (last 5 activities)
    recent_activity = sorted(user_progress, key=lambda x: x.get("timestamp", ""), reverse=True)[:5]
    
    # Generate improvement tips
    improvement_tips = generate_improvement_tips(aptitude_stats, coding_stats)
    
    return {
        "user_id": user_id,
        "overall_score": round(overall_score, 2),
        "aptitude": aptitude_stats,
        "coding": coding_stats,
        "recent_activity": recent_activity,
        "summary": {
            "total_activities": len(user_progress),
            "improvement_tips": improvement_tips
        }
    }

# Generate personalized improvement tips based on user performance
def generate_improvement_tips(aptitude_stats, coding_stats):
    tips = []
    
    if aptitude_stats["tests_taken"] == 0:
        tips.append("Start practicing aptitude tests to improve your quantitative skills")
    elif aptitude_stats["average_score"] < 60:
        tips.append("Focus on practicing more aptitude questions to improve your score")
    
    if coding_stats["problems_attempted"] == 0:
        tips.append("Try solving coding problems to enhance your programming skills")
    elif coding_stats["average_success_rate"] < 50:
        tips.append("Practice more coding problems and focus on understanding test cases")
    
    if not tips:
        tips.append("Great job! Keep practicing to maintain your progress")
    
    return tips