from fastapi import APIRouter, Form
from datetime import datetime
from database import progress_data

router = APIRouter()

COMMUNICATION_QUESTIONS = [
    "Tell me about yourself",
    "What are your strengths and weaknesses?",
    "Why do you want to work for our company?",
    "Describe a challenging situation and how you handled it",
    "Where do you see yourself in 5 years?"
]

@router.get("/questions")
def get_communication_questions():
    return COMMUNICATION_QUESTIONS

@router.post("/evaluate-speech")
def evaluate_speech(
    question: str = Form(...),
    user_id: str = Form(...),
    response_text: str = Form(...)
):
    analysis_results = analyze_speech_content(response_text, question)
    
    progress_data.append({
        "user_id": user_id,
        "module": "communication",
        "score": analysis_results["overall_score"],
        "timestamp": datetime.utcnow(),
        "details": analysis_results
    })
    
    return analysis_results

def analyze_speech_content(text: str, original_question: str):
    word_count = len(text.split())
    fluency_score = min(word_count * 2, 100)
    relevance_score = calculate_relevance(text, original_question)
    confidence_score = calculate_confidence(text)
    
    overall_score = (fluency_score * 0.4 + relevance_score * 0.4 + confidence_score * 0.2)
    
    feedback = generate_feedback(fluency_score, relevance_score, confidence_score, text)
    
    return {
        "overall_score": round(overall_score, 2),
        "fluency_score": round(fluency_score, 2),
        "relevance_score": round(relevance_score, 2),
        "confidence_score": round(confidence_score, 2),
        "word_count": word_count,
        "feedback": feedback,
        "transcribed_text": text
    }

def calculate_relevance(response: str, question: str):
    question_keywords = set(question.lower().split())
    response_keywords = set(response.lower().split())
    common_words = question_keywords.intersection(response_keywords)
    if not question_keywords:
        return 50
    relevance = min(len(common_words) / len(question_keywords) * 100, 100)
    return relevance

def calculate_confidence(text: str):
    confident_words = ['confident', 'achieved', 'success', 'lead', 'managed', 'created', 'improved']
    weak_words = ['maybe', 'perhaps', 'not sure', 'I think', 'kind of']
    confident_count = sum(text.lower().count(word) for word in confident_words)
    weak_count = sum(text.lower().count(word) for word in weak_words)
    score = max(0, 50 + (confident_count * 10) - (weak_count * 15))
    return min(score, 100)

def generate_feedback(fluency, relevance, confidence, text):
    feedback = []
    if fluency < 40:
        feedback.append("Try to provide more detailed responses (aim for 50+ words).")
    elif fluency > 80:
        feedback.append("Excellent response length! Good elaboration.")
    if relevance < 60:
        feedback.append("Focus on directly addressing the question asked.")
    else:
        feedback.append("Great job staying relevant to the question!")
    if confidence < 50:
        feedback.append("Use more confident language and specific achievements.")
    else:
        feedback.append("Confident communication style - well done!")
    filler_words = ['um', 'uh', 'like', 'you know', 'actually', 'basically']
    filler_count = sum(text.lower().count(word) for word in filler_words)
    if filler_count > 2:
        feedback.append(f"Reduce filler words (found {filler_count}). Practice pausing instead.")
    return " | ".join(feedback) if feedback else "Excellent communication skills! Keep it up."