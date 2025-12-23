from fastapi import APIRouter
from datetime import datetime
from database import progress_data

router = APIRouter()

HR_QUESTIONS = [
    "Tell me about yourself",
    "Why should we hire you?",
    "What are your salary expectations?",
    "Describe a time you faced a challenge",
    "Where do you see yourself in 5 years?",
    "Why do you want to work here?",
    "What are your strengths and weaknesses?"
]

TECHNICAL_QUESTIONS = {
    "python": [
        "What are Python decorators?",
        "Explain list comprehensions",
        "What is the difference between list and tuple?",
        "How does garbage collection work in Python?"
    ],
    "java": [
        "What is OOP?",
        "Explain inheritance in Java",
        "What are interfaces?",
        "What is method overloading?"
    ]
}

@router.get("/questions")
async def get_interview_questions(interview_type: str = "hr", topic: str = None):
    if interview_type.lower() == "hr":
        return HR_QUESTIONS
    elif interview_type.lower() == "technical" and topic:
        return TECHNICAL_QUESTIONS.get(topic.lower(), ["No questions available for this topic"])
    else:
        return {"error": "Invalid interview type or missing topic"}

@router.post("/submit-response")
async def submit_interview_response(response: dict):
    user_id = response.get("user_id")
    question = response.get("question")
    user_response = response.get("response")
    interview_type = response.get("interview_type", "hr")
    
    evaluation = evaluate_interview_response(question, user_response, interview_type)
    
    progress_data.append({
        "user_id": user_id,
        "module": f"interview_{interview_type}",
        "score": evaluation["overall_score"],
        "timestamp": datetime.utcnow(),
        "question": question,
        "user_response": user_response,
        "evaluation": evaluation
    })
    
    return evaluation

def evaluate_interview_response(question: str, response: str, interview_type: str):
    if interview_type == "hr":
        scores = evaluate_hr_response(question, response)
    else:
        scores = evaluate_technical_response(question, response)
    
    overall_score = (scores["relevance"] * 0.4 + scores["depth"] * 0.3 + scores["clarity"] * 0.3)
    feedback = generate_interview_feedback(scores, interview_type)
    
    return {
        "overall_score": round(overall_score, 2),
        "scores": scores,
        "feedback": feedback,
        "interview_type": interview_type
    }

def evaluate_hr_response(question: str, response: str):
    word_count = len(response.split())
    return {
        "relevance": min(word_count * 1.5, 100),
        "depth": min(len(response) / 5, 100),
        "clarity": 75,
        "confidence": min(word_count * 2, 100)
    }

def evaluate_technical_response(question: str, response: str):
    word_count = len(response.split())
    return {
        "relevance": min(word_count * 2, 100),
        "depth": min(len(response) / 3, 100),
        "clarity": 80,
        "accuracy": 70
    }

def generate_interview_feedback(scores: dict, interview_type: str):
    feedback = []
    if scores["relevance"] < 60:
        feedback.append("Focus on staying more relevant to the question.")
    else:
        feedback.append("Good relevance to the question.")
    if scores["depth"] < 50:
        feedback.append("Provide more detailed examples and explanations.")
    else:
        feedback.append("Good depth in your response.")
    if interview_type == "hr" and scores.get("confidence", 0) < 60:
        feedback.append("Work on expressing more confidence in your answers.")
    if interview_type == "technical" and scores.get("accuracy", 0) < 70:
        feedback.append("Review technical concepts for better accuracy.")
    return " | ".join(feedback)