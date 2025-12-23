from fastapi import APIRouter
from database import questions_collection, progress_collection, update_user_proficiency, get_next_difficulty, get_user_topic_proficiency
from datetime import datetime
from typing import Optional
import random

router = APIRouter()

# Get aptitude questions for the test (adaptive)
@router.get("/questions")
async def get_aptitude_questions(user_id: Optional[str] = None, topic: Optional[str] = None, count: int = 10, include_explanations: bool = False):
    """Get adaptive aptitude questions based on user proficiency"""
    from database import get_aptitude_questions
    
    all_questions = get_aptitude_questions()
    
    # Filter by topic if provided
    if topic:
        all_questions = [q for q in all_questions if q.get('topic') == topic]
    
    # If no user_id provided, return random questions
    if not user_id:
        selected_questions = random.sample(all_questions, min(count, len(all_questions)))
        return format_questions(selected_questions, include_explanations)
    
    # If user_id provided, implement adaptive selection
    selected_questions = []
    
    # Get topics from available questions
    topics = list(set(q.get('topic') for q in all_questions))
    if topic:
        topics = [topic]
    
    # If no topics available, return random questions
    if not topics:
        selected_questions = random.sample(all_questions, min(count, len(all_questions)))
        return format_questions(selected_questions, include_explanations)
    
    # Select questions adaptively
    questions_per_topic = max(1, count // len(topics))
    
    for t in topics:
        # Get next difficulty level for this topic
        difficulty = get_next_difficulty(user_id, t)
        
        # Filter questions by topic and difficulty
        topic_questions = [q for q in all_questions 
                          if q.get('topic') == t and q.get('difficulty') == difficulty]
        
        # If no questions of this difficulty, get any difficulty
        if not topic_questions:
            topic_questions = [q for q in all_questions if q.get('topic') == t]
        
        # Select questions for this topic
        if topic_questions:
            selected_for_topic = random.sample(
                topic_questions, 
                min(questions_per_topic, len(topic_questions))
            )
            selected_questions.extend(selected_for_topic)
    
    # If we still need more questions, fill with random questions
    if len(selected_questions) < count:
        remaining_count = count - len(selected_questions)
        remaining_questions = [q for q in all_questions if q not in selected_questions]
        if remaining_questions:
            additional_questions = random.sample(
                remaining_questions,
                min(remaining_count, len(remaining_questions))
            )
            selected_questions.extend(additional_questions)
    
    # Limit to requested count
    selected_questions = selected_questions[:count]
    
    return format_questions(selected_questions, include_explanations)

def format_questions(questions, include_explanations=False):
    """Format questions to match frontend expectations"""
    formatted_questions = []
    for question in questions:
        formatted_question = {
            "id": question.get("id"),
            "question": question.get("question"),
            "options": question.get("options", []),
            "correct": question.get("correct_answer"),
            "type": question.get("topic", "general"),
            "difficulty": question.get("difficulty", "easy"),
            "topic": question.get("topic", "general")
        }
        
        # Only include explanation if requested
        if include_explanations:
            formatted_question["explanation"] = question.get("explanation", "")
        
        formatted_questions.append(formatted_question)
    
    return formatted_questions

# Submit answers and calculate score
@router.post("/submit")
async def submit_answers(payload: dict):
    """
    Submit user answers and calculate score
    Expected input: {"user_id": "user123", "answers": {"question_id": selected_option_index}}
    """
    from database import questions_data
    
    user_id = payload.get("user_id")
    user_answers = payload.get("answers", {})
    topic = payload.get("topic", "general")
    
    score = 0
    total_questions = len(user_answers)
    
    # Check each answer and update user proficiency
    for question_id, user_answer in user_answers.items():
        # Find the question in the list
        question = next((q for q in questions_data if q.get("id") == question_id), None)
        
        # If question exists and user answer is correct
        is_correct = False
        if question and question.get("correct_answer") == user_answer:
            score += 1
            is_correct = True
        
        # Update user proficiency if user_id is provided
        if user_id and question:
            difficulty = question.get("difficulty", "easy")
            question_topic = question.get("topic", topic)
            update_user_proficiency(user_id, question_topic, difficulty, is_correct)
    
    # Calculate percentage
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    # Save progress to database
    progress_record = {
        "module": "aptitude",
        "correct": score,
        "total": total_questions,
        "percentage": percentage,
        "timestamp": datetime.utcnow()
    }
    
    if user_id:
        progress_record["user_id"] = user_id
        if topic:
            progress_record["topic"] = topic
    
    progress_collection.append(progress_record)
    
    return {
        "correct": score,
        "total": total_questions, 
        "percentage": round(percentage, 2),
        "message": "Answers submitted successfully"
    }

# Get user's topic proficiency
@router.get("/proficiency/{user_id}")
async def get_user_proficiency_endpoint(user_id: str, topic: Optional[str] = None):
    """Get user's proficiency data for all topics or a specific topic"""
    if topic:
        proficiency = get_user_topic_proficiency(user_id, topic)
        return {
            "user_id": user_id,
            "topic": topic,
            "proficiency": proficiency
        }
    else:
        # Return proficiency for all topics
        from database import user_proficiency_data
        user_proficiency = user_proficiency_data.get(user_id, {})
        return {
            "user_id": user_id,
            "proficiency": user_proficiency
        }

# Get available topics
@router.get("/topics")
async def get_topics():
    """Get list of available aptitude topics"""
    from database import get_aptitude_questions
    
    questions = get_aptitude_questions()
    topics = list(set(q.get('topic') for q in questions))
    
    return {
        "topics": topics
    }

# Get detailed results with explanations
@router.post("/detailed-results")
async def get_detailed_results(payload: dict):
    """Get detailed results with explanations for each question"""
    from database import questions_data, get_aptitude_questions
    
    user_answers = payload.get("answers", {})
    question_ids = list(user_answers.keys())
    
    # Get all aptitude questions
    all_questions = get_aptitude_questions()
    
    # Find the questions that were answered
    detailed_results = []
    for question_id in question_ids:
        # Find the question in the database
        question = next((q for q in all_questions if q.get("id") == question_id), None)
        user_answer = user_answers.get(question_id)
        
        if question:
            is_correct = question.get("correct_answer") == user_answer
            
            result = {
                "id": question.get("id"),
                "question": question.get("question"),
                "options": question.get("options", []),
                "correct_answer": question.get("correct_answer"),
                "user_answer": user_answer,
                "is_correct": is_correct,
                "explanation": question.get("explanation", ""),
                "topic": question.get("topic", "general"),
                "difficulty": question.get("difficulty", "easy")
            }
            detailed_results.append(result)
    
    return detailed_results