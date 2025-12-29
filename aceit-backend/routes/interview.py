from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict
import random
from datetime import datetime
import os
import json
import requests

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
    Revised Rule-based Confidence Score (0-100).
    Focuses on Speech Quality (90%) and Video Stability (10%).
    """
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)
    
    # --- 1. BASELINE ---
    # Start at 70 (Average). Good behavior adds, bad subtracts.
    score = 70.0 
    
    # --- 2. LENGTH FACTOR ---
    # Penalize very short answers which can't be confident.
    if word_count < 10: score -= 30  # Very short
    elif word_count < 30: score -= 15 # Short
    elif word_count > 50: score += 10 # Good length (Bonus)
    
    # --- 3. FILLER DENSITY (per 100 words) ---
    fillers = ["um", "uh", "like", "you know", "actually", "basically", "literally"]
    filler_count = sum(text_lower.count(f) for f in fillers)
    
    density = 0
    if word_count > 0:
        density = (filler_count / word_count) * 100
        
    # Penalty: -5 points for every 2% of filler density
    filler_penalty = (density / 2) * 5
    score -= filler_penalty
    
    # --- 4. PACING (WPM) ---
    # Ideal range: 130-160 WPM.
    duration = speech_m.audio_duration_seconds if speech_m else 10.0
    wpm = (word_count / duration) * 60 if duration > 0 else 0
    
    if wpm > 0:
        dist_from_ideal = abs(wpm - 145) # 145 is sweet spot
        if dist_from_ideal > 25: # Outside 120-170 range
            # Penalty: 0.5 points per WPM deviation beyond expected buffer
            score -= (dist_from_ideal - 25) * 0.5

    # --- 5. VOCABULARY ANALYSIS ---
    # Power Words (Confidence)
    power_words = ["definitely", "successfully", "managed", "led", "solved", "optimized", "believe", "crucial", "achieved"]
    power_count = sum(1 for w in power_words if w in text_lower)
    score += min(15, power_count * 3) # Max +15 bonus
    
    # Hesitation/Weak Words
    weak_words = ["maybe", "guess", "probably", "i think", "sort of", "kind of"]
    weak_count = sum(1 for w in weak_words if w in text_lower)
    score -= min(15, weak_count * 3) # Max -15 penalty
    
    # --- 6. VIDEO MODIFIER (Mockable) ---
    # Only acts as a small modifier (+/- 10 max)
    video_mod = 0
    if video_m:
        if video_m.face_visible_pct < 0.8: video_mod -= 5
        if video_m.looking_away_pct > 0.3: video_mod -= 5
        if video_m.face_visible_pct > 0.95 and video_m.looking_away_pct < 0.1: video_mod += 5
    
    score += video_mod
    
    # Clamp final score
    final_score = int(max(0, min(100, score)))
    
    return {
        "score": final_score,
        "breakdown": {
            "base_score": 70,
            "length_penalty": -30 if word_count < 10 else (-15 if word_count < 30 else 0),
            "filler_penalty": int(-filler_penalty),
            "wpm_penalty": int(score - (70 - filler_penalty + min(15, power_count * 3) - min(15, weak_count * 3) + video_mod)) if wpm > 0 else 0, # Rough approx for debug
            "vocab_bonus": int(min(15, power_count * 3)),
            "weak_word_penalty": int(-min(15, weak_count * 3)),
            "video_mod": video_mod,
            "wpm_val": int(wpm),
            "fillers_count": filler_count
        }
    }

def analyze_answer_logic(question_text: str, user_text: str, keywords: List[str], confidence_data: Dict) -> Dict:
    """
    Combines Content Analysis + Confidence Score.
    """
    user_text = user_text.lower()
    words = user_text.split()
    word_count = len(words)
    
    # 1. Relevance Analysis
    matched = [k for k in keywords if k in user_text]
    relevance_score = min(100, (len(matched) / max(1, len(keywords))) * 100)
    if not keywords: relevance_score = 85 
    
    # 2. Depth Analysis
    # Expect ~50-80 words for a solid answer
    depth_score = min(100, (word_count / 60) * 100) 
    
    # 3. Clarity (Directly map confidence)
    clarity_score = confidence_data["score"]
        
    # Weighted Final Score
    # Relevance 40%, Depth 30%, Confidence 30%
    overall_score = int((relevance_score * 0.45) + (depth_score * 0.25) + (clarity_score * 0.30))
    
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
    """
    Selects the next question based on the candidate's performance (Overall Score).
    Rules:
    - >= 75: Increase Difficulty (Challenge)
    - 50 - 74: Maintain Difficulty (Reinforce)
    - < 50: Decrease Difficulty (Recovery)
    """
    score = analysis["overall_score"]
    current_diff = session["difficulty_level"]
    next_diff = current_diff
    transition_reason = ""
    
    # --- 1. Determine Next Difficulty ---
    if score >= 75:
        # High Performer -> Challenge them
        if current_diff == "easy":
            next_diff = "medium"
            transition_reason = "Great answer! Moving to intermediate questions."
        elif current_diff == "medium":
            next_diff = "hard"
            transition_reason = "Excellent technical depth. Let's try a complex scenario."
        else:
            transition_reason = "Consistent high performance on advanced topics."
            
    elif 50 <= score <= 74:
        # Average Performer -> Verify consistency
        transition_reason = "Good response. Let's stay on this level to verify consistency."
        # Optional: In a real system, we might ask a follow-up here. 
        # For now, we pick another question from the SAME bucket.
        
    else: # score < 50
        # Struggling -> Recovery mode
        if current_diff == "hard":
            next_diff = "medium"
            transition_reason = "Let's step back to intermediate concepts."
        elif current_diff == "medium":
            next_diff = "easy"
            transition_reason = "Let's review the basics to build confidence."
        else:
            transition_reason = "Focusing on core fundamentals."
            
    # --- 2. Fetch Question from Bank ---
    session["difficulty_level"] = next_diff
    
    # Safely get question pool
    type_pool = QUESTION_BANK.get(session["type"], {})
    topic_pool = type_pool.get(session["topic"], {})
    
    # Fallback to 'general' or 'python' if topic missing
    if not topic_pool:
        fallback_topic = "python" if session["type"] == "technical" else "general"
        topic_pool = type_pool.get(fallback_topic, {})
        
    pool = topic_pool.get(next_diff, [])
    
    # Filter used questions
    used_ids = {x["question"]["id"] for x in session["history"]}
    # Also exclude current question just in case it wasn't in history yet (though it should be)
    available = [q for q in pool if q["id"] not in used_ids and q["id"] != current_q["id"]]
    
    # --- 3. Handle Empty Pool (Fallback) ---
    if not available:
        # If run out of 'hard', maybe go back to 'medium'? 
        # For MVP, if we run out of specific level, try finding ANY available question
        all_levels = ["easy", "medium", "hard"]
        for lvl in all_levels:
            pool_lvl = topic_pool.get(lvl, [])
            available = [q for q in pool_lvl if q["id"] not in used_ids]
            if available:
                transition_reason += " (Switched level due to question availability)"
                break
    
    if not available:
        return None # End session if truly no questions left
        
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
    
    total_fillers = sum(h["analysis"]["confidence_breakdown"]["fillers_count"] for h in history)
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

# --- LLM Integration ---

def evaluate_with_llm(
    current_q: Dict, 
    user_text: str, 
    s_metrics: SpeechMetrics, 
    v_metrics: VideoMetrics
) -> Optional[Dict]:
    """
    Evaluates the interview answer using Google Gemini API.
    Returns None if API key is missing or error occurs (fallback to rules).
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    # Construct Prompt
    q_text = current_q.get("text", "Unknown Question")
    keywords = current_q.get("keywords", [])
    
    prompt = f"""
    You are an expert technical interviewer evaluating a candidate's response.
    
    Question: "{q_text}"
    Expected Keywords: {', '.join(keywords)}
    
    Candidate Response: "{user_text}"
    
    Speech Metrics:
    - Duration: {s_metrics.audio_duration_seconds}s
    - WPM: {s_metrics.wpm_calculated} (Ideal: 130-160)
    
    Video Context:
    - Face Visible: {int(v_metrics.face_visible_pct * 100)}%
    - Looking Away: {int(v_metrics.looking_away_pct * 100)}%
    
    Task:
    Analyze the answer for Relevance, Depth, Clarity, and Confidence.
    Provide a JSON response strictly in this format:
    {{
        "overall_score": <0-100>,
        "relevance": <0-100>,
        "depth": <0-100>,
        "clarity": <0-100>,
        "confidence": <0-100>,
        "feedback": "<Short, constructive feedback to the user (max 2 sentences)>",
        "missing_keywords": ["<keyword1>", "<keyword2>"],
        "confidence_breakdown": {{
            "fillers_count": 0,
            "wpm_val": {s_metrics.wpm_calculated or 0},
            "video_mod": 0
        }}
    }}
    """
    
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean markdown wrappers if present
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(raw_text)
        
        # Ensure fallback for fields potentially missed by LLM
        if "confidence_breakdown" not in analysis:
             analysis["confidence_breakdown"] = {"fillers_count": 0, "wpm_val": 0, "video_mod": 0}
             
        analysis["generated_feedback"] = analysis.get("feedback", "Good attempt.")
        return analysis

    except Exception as e:
        print(f"LLM Evaluation Failed: {e}")
        return None

def evaluate_answer_with_llm(
    question_text: str,
    user_answer_text: str,
    difficulty: str,
    interview_type: str
) -> Optional[Dict]:
    """
    Evaluates the interview answer using Gemini API with specific feedback structure.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return None

    prompt = f"""
    You are an expert technical interviewer evaluating a candidate's response.
    
    Context:
    - Interview Type: {interview_type}
    - Difficulty Level: {difficulty}
    - Question: "{question_text}"
    
    Candidate Answer: "{user_answer_text}"
    
    Analyze the answer strictly.
    Provide a JSON response strictly in this format:
    {{
        "confidence_score": <0-100 integer representing confidence and quality>,
        "strengths": ["<strength1>", "<strength2>"],
        "improvements": ["<improvement1>", "<improvement2>"],
        "feedback_summary": "<Concise feedback paragraph>",
        "suggested_followup_question": "<One relevant technical follow-up question>"
    }}
    """
    
    try:
        print(f"DEBUG: sending to llm: {question_text[:50]}...")
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        headers = {"Content-Type": "application/json"}
        
        response = requests.post(url, headers=headers, json=payload, timeout=5)
        response.raise_for_status()
        
        data = response.json()
        print(f"DEBUG: received from llm: {str(data)[:200]}...")
        
        raw_text = data["candidates"][0]["content"]["parts"][0]["text"]
        
        # Clean markdown
        raw_text = raw_text.replace("```json", "").replace("```", "").strip()
        analysis = json.loads(raw_text)
        
        return analysis

    except Exception as e:
        print(f"LLM Evaluation Failed (evaluate_answer_with_llm): {e}")
        return None


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
    # 1. Logic Phase
    # Try LLM first using the new function
    llm_result = evaluate_answer_with_llm(
        question_text=current_q["text"],
        user_answer_text=req.user_response_text,
        difficulty=session.get("difficulty_level", "easy"),
        interview_type=session.get("type", "hr")
    )
    
    if llm_result:
        # Map new LLM output to existing analysis structure
        score = llm_result.get("confidence_score", 0)
        feedback_summary = llm_result.get("feedback_summary", "")
        
        analysis = {
            "overall_score": score,
            "relevance": score,   # Approx
            "depth": score,       # Approx
            "clarity": score,     # Approx
            "confidence": score,  # Approx
            "confidence_breakdown": {"fillers_count": 0, "wpm_val": 0, "video_mod": 0},
            "generated_feedback": feedback_summary,
            "strengths": llm_result.get("strengths", []),
            "improvements": llm_result.get("improvements", []),
            "missing_keywords": [] # New LLM prompt doesn't ask for this explicitly
        }
    else:
        # Fallback to Rules if LLM fails
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
    feedback_text = analysis.get("generated_feedback", "")
    
    if not feedback_text:
        # Fallback to rule-based feedback generation if LLM didn't provide it (or if we used rule-based)
        if analysis["overall_score"] > 80: feedback_text = "Excellent answer! Confident and precise."
        else:
            # Check for confidence breakdown only if it exists (LLM might mock it)
            c_breakdown = analysis.get("confidence_breakdown", {})
            fillers = c_breakdown.get("fillers_count", 0)
            
            if fillers > 2:
                feedback_text += f"Try to reduce filler words (found {fillers}). "
            if analysis.get("missing_keywords"):
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