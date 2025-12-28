from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import random
from datetime import datetime

router = APIRouter()

# --- Data Models ---
class InterviewStartRequest(BaseModel):
    user_id: str
    interview_type: str = "hr"
    tech_stack: Optional[str] = None

class VideoMetrics(BaseModel):
    face_visible_pct: float = 1.0  # 0.0 to 1.0
    looking_away_pct: float = 0.0  # 0.0 to 1.0

class SpeechMetrics(BaseModel):
    audio_duration_seconds: float = 10.0
    wpm_calculated: Optional[float] = None # Can be sent from frontend or calc here

class InterviewAnalysisRequest(BaseModel):
    session_id: str
    question_id: str
    user_response_text: str
    # New metrics
    video_metrics: Optional[VideoMetrics] = None
    speech_metrics: Optional[SpeechMetrics] = None

class InterviewResponse(BaseModel):
    session_id: str
    current_question: Dict
    feedback: Optional[str] = None
    score: Optional[int] = None
    scores: Optional[Dict] = None 
    report: Optional[Dict] = None # Final Report
    is_completed: bool = False

# --- Data Stores ---
active_sessions = {}

QUESTION_BANK = {
     "hr": {
        "general": {
            "easy": [
                {"id": "hr_e_1", "text": "Tell me about yourself.", "keywords": ["experience", "background"]},
                {"id": "hr_e_2", "text": "What are your greatest strengths?", "keywords": ["learner", "team"]},
            ],
            "medium": [
                {"id": "hr_m_1", "text": "Describe a challenge you overcame.", "keywords": ["situation", "result"]},
                {"id": "hr_m_2", "text": "Why do you want to work here?", "keywords": ["culture", "mission"]},
            ],
            "hard": [
                {"id": "hr_h_1", "text": "Where do you see yourself in 5 years?", "keywords": ["lead", "mentor"]},
            ]
        }
    },
    "technical": {
        "python": {
            "easy": [{"id": "py_e_1", "text": "What is the difference between list and tuple?", "keywords": ["mutable", "immutable"]}],
            "medium": [{"id": "py_m_1", "text": "Explain Python decorators.", "keywords": ["wrapper", "function"]}],
            "hard": [{"id": "py_h_1", "text": "How does memory management work in Python?", "keywords": ["garbage", "reference"]}]
        }
    }
}

# --- Core Logic ---

def calculate_confidence(text: str, speech_m: SpeechMetrics, video_m: VideoMetrics) -> Dict:
    """
    Rule-based Confidence Score (0-100)
    Factors: Filler words, WPM, Assertiveness, Face Visibility, Eye Contact.
    """
    text_lower = text.lower()
    word_count = len(text.split())
    
    # 1. SPEECH SCORE (60%)
    speech_score = 100
    
    # Filler penalty
    fillers = ["um", "uh", "like", "you know", "actually", "basically"]
    filler_count = sum(text_lower.count(f) for f in fillers)
    speech_score -= (filler_count * 2)
    
    # Pacing (WPM)
    duration = speech_m.audio_duration_seconds if speech_m else 10.0
    wpm = (word_count / duration) * 60 if duration > 0 else 120
    if wpm < 100: speech_score -= 10 # Too slow
    if wpm > 180: speech_score -= 5  # Too fast
    
    # Assertive Bonus
    assertive_words = ["definitely", "successfully", "managed", "led", "solved"]
    if any(w in text_lower for w in assertive_words):
        speech_score += 5
        
    speech_score = max(0, min(100, speech_score))
    
    # 2. VIDEO SCORE (40%) - Mockable
    video_score = 100
    if video_m:
         # Face visibility check
         if video_m.face_visible_pct < 0.9:
             penalty = (0.9 - video_m.face_visible_pct) * 100
             video_score -= penalty
         
         # Eye contact check (looking away)
         if video_m.looking_away_pct > 0.2:
             video_score -= 20
             
    video_score = max(0, min(100, int(video_score)))
    
    # Final Weighted Score
    final_confidence = int((speech_score * 0.6) + (video_score * 0.4))
    
    return {
        "score": final_confidence,
        "breakdown": {
            "speech_score": int(speech_score),
            "video_score": int(video_score),
            "wpm": int(wpm),
            "fillers_detected": filler_count
        }
    }

def analyze_answer_logic(question_text: str, user_text: str, keywords: List[str], confidence_data: Dict) -> Dict:
    """
    Combines Content Analysis + Confidence Score.
    """
    user_text = user_text.lower()
    
    # 1. Relevance Analysis
    matched = [k for k in keywords if k in user_text]
    relevance_score = min(100, (len(matched) / max(1, len(keywords))) * 100)
    if not keywords: relevance_score = 85 
    
    # 2. Depth Analysis
    word_count = len(user_text.split())
    depth_score = min(100, (word_count / 40) * 100) 
    
    # 3. Clarity Analysis (merged with confidence roughly)
    clarity_score = confidence_data["breakdown"]["speech_score"]
        
    overall_score = int((relevance_score * 0.4) + (depth_score * 0.3) + (clarity_score * 0.3))
    
    return {
        "overall_score": overall_score,
        "relevance": int(relevance_score),
        "depth": int(depth_score),
        "clarity": int(clarity_score),
        "confidence": confidence_data["score"],
        "confidence_breakdown": confidence_data["breakdown"],
        "missing_keywords": [k for k in keywords if k not in user_text]
    }

def generate_next_question_logic(current_q: Dict, analysis: Dict, session: Dict) -> Dict:
    # (Same as before)
    score = analysis["overall_score"]
    next_diff = session["difficulty_level"]
    
    if score > 75:
        if session["difficulty_level"] == "easy": next_diff = "medium"
        elif session["difficulty_level"] == "medium": next_diff = "hard"
        transition_reason = "Strong performance, increasing challenge."
    elif score < 50:
        if session["difficulty_level"] == "hard": next_diff = "medium"
        elif session["difficulty_level"] == "medium": next_diff = "easy"
        transition_reason = "Struggling, simplify to build confidence."
    else:
        transition_reason = "Steady performance, maintaining level."
        
    session["difficulty_level"] = next_diff
    pool = QUESTION_BANK.get(session["type"], {}).get(session["topic"], {}).get(next_diff, [])
    used = {x["question"]["id"] for x in session["history"]}
    available = [q for q in pool if q["id"] not in used]
    
    if not available: return None
    next_q = random.choice(available)
    next_q["ai_context"] = transition_reason
    return next_q

def generate_final_report(session: Dict) -> Dict:
    """
    Generates a performance report based on the entire session history.
    """
    history = session["history"]
    if not history:
        return {}
        
    total_q = len(history)
    avg_score = int(sum(h["analysis"]["overall_score"] for h in history) / total_q)
    
    # Aggregate Metrics
    avg_confidence = int(sum(h["analysis"]["confidence"] for h in history) / total_q)
    avg_depth = int(sum(h["analysis"]["depth"] for h in history) / total_q)
    avg_clarity = int(sum(h["analysis"]["clarity"] for h in history) / total_q)
    
    # Feedback Generation
    strengths = []
    improvements = []
    
    if avg_confidence > 80: strengths.append("Excellent executive presence and confidence.")
    elif avg_confidence < 60: improvements.append("Work on speaking more assertively and reducing hesitation.")
    
    if avg_depth > 70: strengths.append("Answers had good technical depth and detail.")
    else: improvements.append("Your answers were too brief. Use the STAR method to elaborate.")
    
    if avg_clarity > 80: strengths.append("Communication was clear and easy to follow.")
    
    total_fillers = sum(h["analysis"]["confidence_breakdown"]["fillers_detected"] for h in history)
    if total_fillers > 5:
        improvements.append(f"Detected {total_fillers} filler words. Pause instead of saying 'um' or 'like'.")

    # Final Result
    result = "Pass" if avg_score >= 60 else "Needs Improvement"
    recommendation = "Ready for HR Round!" if avg_score > 75 else "Review core concepts and practice mock interviews."
    
    return {
        "session_summary": {
            "total_questions": total_q,
            "overall_score": avg_score,
            "result": result
        },
        "metrics": {
            "confidence": avg_confidence,
            "communication": avg_clarity,
            "technical_depth": avg_depth,
            "hr_readiness": int((avg_confidence + avg_clarity)/2)
        },
        "detailed_feedback": {
            "strengths": strengths,
            "improvements": improvements
        },
        "recommendation": recommendation
    }

# --- Endpoints ---

@router.post("/start", response_model=InterviewResponse)
async def start_interview(req: InterviewStartRequest):
    session_id = f"{req.user_id}_{int(datetime.utcnow().timestamp())}"
    topic = req.tech_stack if req.interview_type == "technical" else "general"
    if req.interview_type == "technical" and topic not in QUESTION_BANK.get("technical", {}): topic = "python"
    
    try: first_q = random.choice(QUESTION_BANK[req.interview_type][topic]["easy"])
    except: raise HTTPException(500, "Configuration Error: Check Question Bank")

    active_sessions[session_id] = {
        "user_id": req.user_id,
        "type": req.interview_type,
        "topic": topic,
        "history": [],
        "current_q": first_q,
        "difficulty_level": "easy",
        "score_accumulated": 0
    }
    return {
        "session_id": session_id,
        "current_question": first_q,
        "feedback": "AI Interview Initialized. Good luck!",
        "score": 0,
        "is_completed": False
    }

@router.post("/analyze", response_model=InterviewResponse)
async def analyze_response(req: InterviewAnalysisRequest):
    session = active_sessions.get(req.session_id)
    if not session: raise HTTPException(404, "Session not found")
    current_q = session["current_q"]
    
    # Defaults
    s_metrics = req.speech_metrics or SpeechMetrics(audio_duration_seconds=10.0, wpm_calculated=0)
    v_metrics = req.video_metrics or VideoMetrics() # Use defaults (perfect visibility) if not sent
    
    # 1. Logic Phase
    confidence = calculate_confidence(req.user_response_text, s_metrics, v_metrics)
    analysis = analyze_answer_logic(current_q["text"], req.user_response_text, current_q.get("keywords", []), confidence)
    
    # History Update
    session["history"].append({
        "question": current_q,
        "answer": req.user_response_text,
        "analysis": analysis
    })
    session["score_accumulated"] += analysis["overall_score"]
    
    # 2. Generation Phase
    history_len = len(session["history"])
    if history_len >= 5:
        # Generate Final Report
        report = generate_final_report(session)
        avg = report["session_summary"]["overall_score"]
        
        return {
            "session_id": req.session_id,
            "current_question": {},
            "feedback": f"Session Complete! Score: {avg}/100.",
            "score": avg,
            "scores": analysis,
            "report": report, # Return the full report
            "is_completed": True
        }

    next_q = generate_next_question_logic(current_q, analysis, session)
    if not next_q:
         # Fallback report if run out of questions
         report = generate_final_report(session)
         return {
            "session_id": req.session_id,
            "current_question": {},
            "feedback": "No more questions.",
            "score": analysis["overall_score"],
            "scores": analysis,
            "report": report,
            "is_completed": True
        }
    
    session["current_q"] = next_q
    
    # Smart Feedback
    feedback_text = ""
    if analysis["overall_score"] > 80: feedback_text = "Excellent answer! Confident and precise."
    else: 
        if confidence["breakdown"]["fillers_detected"] > 2:
            feedback_text += f"Try to reduce filler words (found {confidence['breakdown']['fillers_detected']}). "
        if analysis["missing_keywords"]:
            feedback_text += f"Tip: Mention terms like {', '.join(analysis['missing_keywords'][:2])}."
        if not feedback_text: feedback_text = "Good, but try to elaborate more."

    return {
        "session_id": req.session_id,
        "current_question": next_q,
        "feedback": feedback_text,
        "score": analysis["overall_score"],
        "scores": analysis,
        "is_completed": False
    }