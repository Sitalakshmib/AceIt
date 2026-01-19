from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database_postgres import get_db
from models.aptitude_sql import AptitudeQuestion, UserAptitudeProgress
from models.analytics_sql import QuestionAttempt
from services.adaptive_engine import AdaptiveEngine, get_or_create_progress
from typing import Optional, List
import random
import datetime

router = APIRouter()

# --- HELPER FUNCTIONS ---

def calculate_next_difficulty(progress: UserAptitudeProgress) -> str:
    """
    Adaptive Algorithm:
    - If accuracy > 80% at current level -> Level Up
    - If accuracy < 50% at current level -> Level Down (if not easy)
    - Otherwise -> Stay
    """
    current_diff = progress.current_difficulty
    
    if current_diff == "easy":
        total = progress.easy_total
        correct = progress.easy_correct
    elif current_diff == "medium":
        total = progress.medium_total
        correct = progress.medium_correct
    else: # hard
        total = progress.hard_total
        correct = progress.hard_correct
        
    if total < 3: # Need minimum 3 attempts to judge
        return current_diff
        
    accuracy = correct / total
    
    if accuracy >= 0.8: # > 80% Success
        if current_diff == "easy": return "medium"
        if current_diff == "medium": return "hard"
        
    if accuracy < 0.5: # < 50% Success
        if current_diff == "hard": return "medium"
        if current_diff == "medium": return "easy"
        
    return current_diff

def format_questions(questions, include_explanations=False):
    """Format SQL objects to JSON response"""
    formatted = []
    for q in questions:
        item = {
            "id": q.id,
            "question": q.question,
            "options": q.options,
            "correct_answer": q.correct_answer, # Providing index for frontend checking if needed, or hide it
            "type": q.topic,
            "topic": q.topic,
            "category": q.category,
            "difficulty": q.difficulty
        }
        if include_explanations:
            item["explanation"] = q.answer_explanation
        formatted.append(item)
    return formatted

# --- ENDPOINTS ---

@router.get("/categories")
async def get_categories(db: Session = Depends(get_db)):
    """Get available aptitude categories and topics"""
    # Group topics by category
    results = db.query(AptitudeQuestion.category, AptitudeQuestion.topic).distinct().all()
    
    categories = {}
    for cat, topic in results:
        if cat not in categories:
            categories[cat] = []
        if topic not in categories[cat]:
            categories[cat].append(topic)
            
    return {"categories": categories}

@router.get("/questions")
async def get_aptitude_questions(
    user_id: Optional[str] = None, 
    topic: Optional[str] = None, 
    category: Optional[str] = None,
    count: int = 10, 
    include_explanations: bool = False,
    db: Session = Depends(get_db)
):
    """Get adaptive aptitude questions based on user proficiency"""
    
    # 1. Determine Difficulty
    target_difficulty = "easy" # Default
    
    if user_id and topic:
        # Check existing progress to find correct difficulty
        # We need the category to create progress if missing. Query one question to find category if not provided
        if not category:
            q_sample = db.query(AptitudeQuestion).filter(AptitudeQuestion.topic == topic).first()
            category = q_sample.category if q_sample else "General"
            
        progress = get_or_create_progress(db, user_id, topic, category)
        target_difficulty = progress.current_difficulty
        
    # 2. Query Questions
    query = db.query(AptitudeQuestion)
    
    if topic:
        query = query.filter(AptitudeQuestion.topic == topic)
    if category:
        query = query.filter(AptitudeQuestion.category == category)
        
    # Try to get questions of target difficulty
    preferred_query = query.filter(AptitudeQuestion.difficulty == target_difficulty)
    questions = preferred_query.limit(count * 2).all() # Get pool
    
    # If not enough, fallback to any difficulty
    if len(questions) < count:
        questions = query.limit(count * 2).all()
        
    # 3. Randomize Selection
    if not questions:
        return []
        
    selected_questions = random.sample(questions, min(len(questions), count))
    
    return format_questions(selected_questions, include_explanations)

@router.post("/submit")
async def submit_answers(payload: dict, db: Session = Depends(get_db)):
    """
    Submit user answers, calculate score, and update adaptive progress
    """
    try:
        user_id = payload.get("user_id")
        user_answers = payload.get("answers", {}) # {question_id: selected_index}
        
        if not user_answers:
            return {"message": "No answers provided", "correct": 0, "total": 0, "percentage": 0, "results": []}

        score = 0
        total = len(user_answers)
        results = []
        
        # Fetch all questions at once
        question_ids = list(user_answers.keys())
        questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()
        questions_map = {q.id: q for q in questions}
        
        # Process each answer
        for q_id, user_ans_idx in user_answers.items():
            question = questions_map.get(q_id)
            if not question: 
                continue
                
            is_correct = (question.correct_answer == user_ans_idx)
            if is_correct: 
                score += 1
                
            results.append({
                "question_id": q_id,
                "correct": is_correct,
                "topic": question.topic,
                "category": question.category,
                "difficulty": question.difficulty
            })
            
            # Adaptive Update (if user logged in)
            if user_id:
                progress = get_or_create_progress(db, user_id, question.topic, question.category)
                
                # Only update if progress was successfully created
                if progress:
                    # Update counters
                    progress.questions_attempted += 1
                    if is_correct:
                        progress.questions_correct += 1
                        progress.streak += 1
                    else:
                        progress.streak = 0
                        
                    # Update difficulty specific counters
                    if question.difficulty == "easy":
                        progress.easy_total += 1
                        if is_correct: progress.easy_correct += 1
                    elif question.difficulty == "medium":
                        progress.medium_total += 1
                        if is_correct: progress.medium_correct += 1
                    elif question.difficulty == "hard":
                        progress.hard_total += 1
                        if is_correct: progress.hard_correct += 1
                    
                    # Recalculate difficulty for next time
                    progress.current_difficulty = calculate_next_difficulty(progress)
                    progress.last_practiced = datetime.datetime.utcnow()
                
        if user_id:
            db.commit()
            
        percentage = (score / total) * 100 if total > 0 else 0
        return {
            "correct": score,
            "total": total,
            "percentage": round(percentage, 2),
            "results": results
        }
    except Exception as e:
        print(f"[ERROR] Aptitude submit failed: {e}")
        return {
            "correct": 0,
            "total": 0,
            "percentage": 0,
            "results": [],
            "error": str(e)
        }

@router.post("/detailed-results")
async def get_detailed_results(payload: dict, db: Session = Depends(get_db)):
    """Get detailed results with explanations for answered questions"""
    user_answers = payload.get("answers", {})
    
    if not user_answers:
        return []
    
    question_ids = list(user_answers.keys())
    questions = db.query(AptitudeQuestion).filter(AptitudeQuestion.id.in_(question_ids)).all()
    questions_map = {q.id: q for q in questions}
    
    results = []
    for q_id, user_ans_idx in user_answers.items():
        question = questions_map.get(q_id)
        if not question:
            continue
            
        is_correct = (question.correct_answer == user_ans_idx)
        results.append({
            "question_id": q_id,
            "question": question.question,
            "options": question.options,
            "user_answer": user_ans_idx,
            "correct_answer": question.correct_answer,
            "correct": is_correct,
            "explanation": question.answer_explanation,
            "topic": question.topic,
            "category": question.category,
            "difficulty": question.difficulty
        })
    
    return results

@router.get("/proficiency/{user_id}")
async def get_user_proficiency(user_id: str, db: Session = Depends(get_db)):
    """Get user's progress via SQL"""
    progress_records = db.query(UserAptitudeProgress).filter(UserAptitudeProgress.user_id == user_id).all()
    
    data = {}
    for p in progress_records:
        if p.category not in data:
            data[p.category] = {}
        data[p.category][p.topic] = {
            "level": p.current_difficulty,
            "accuracy": f"{(p.questions_correct / p.questions_attempted * 100):.1f}%" if p.questions_attempted > 0 else "0%",
            "total_solved": p.questions_correct
        }
        
    return {"user_id": user_id, "proficiency": data}


# ========== PRACTICE MODE ENDPOINTS (IndiaBIX Style) ==========

@router.get("/practice/next-question")
async def get_next_practice_question(
    user_id: str,
    category: str,
    topic: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Get next unattempted question for practice mode.
    IndiaBIX style: One question at a time, no repetition.
    """
    from services.practice_service import PracticeService
    
    try:
        question = PracticeService.get_next_question(db, user_id, category, topic)
        
        if not question:
            return {
                "has_more_questions": False,
                "message": "You've completed all available questions in this topic! Great job!"
            }
        
        return {
            "has_more_questions": True,
            **question
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get next question: {str(e)}")


@router.post("/practice/submit-answer")
async def submit_practice_answer(payload: dict, db: Session = Depends(get_db)):
    """
    Submit answer and get instant feedback with explanation.
    IndiaBIX style: Immediate correctness, explanation, and adaptive feedback.
    """
    from services.practice_service import PracticeService
    
    user_id = payload.get("user_id")
    question_id = payload.get("question_id")
    user_answer = payload.get("user_answer")
    time_spent = payload.get("time_spent", 0)
    
    if not all([user_id, question_id is not None, user_answer is not None]):
        raise HTTPException(
            status_code=400,
            detail="user_id, question_id, and user_answer are required"
        )
    
    try:
        feedback = PracticeService.submit_answer(
            db, user_id, question_id, user_answer, time_spent
        )
        return feedback
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit answer: {str(e)}")