from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, Form
from pydantic import BaseModel
from typing import Optional
import shutil
import os
from services.sim_voice_interviewer import SimVoiceInterviewer

router = APIRouter()

# Singleton Engine
_engine = None
def get_engine():
    global _engine
    if _engine is None:
        _engine = SimVoiceInterviewer()
    return _engine

# --- Data Models ---
class StartRequest(BaseModel):
    user_id: str
    resume_text: Optional[str] = ""
    jd_text: Optional[str] = ""
    interview_type: Optional[str] = "technical"  # "technical", "hr", "project"
    topic: Optional[str] = "realtime"  # "realtime", "python", "java", "qa", "php", "dotnet"
    project_text: Optional[str] = ""  # Description for project-based interview

class NextResponse(BaseModel):
    text: str
    audio_url: str
    is_completed: bool

# --- Routes ---

@router.post("/start")
async def start_interview(req: StartRequest, engine: SimVoiceInterviewer = Depends(get_engine)):
    print(f"[INTERVIEW] /interview/start hit by User: {req.user_id}, Type: {req.interview_type}, Topic: {req.topic}")
    try:
        result = engine.start_interview(req.user_id, req.resume_text, req.jd_text, req.interview_type, req.topic, req.project_text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/answer")
async def process_answer(
    session_id: str = Form(...),
    text_answer: Optional[str] = Form(None),
    audio_file: Optional[UploadFile] = File(None),
    engine: SimVoiceInterviewer = Depends(get_engine)
):
    try:
        temp_file = None
        if audio_file:
            # Save upload momentarily
            temp_file = f"temp_{session_id}_{audio_file.filename}"
            with open(temp_file, "wb") as buffer:
                shutil.copyfileobj(audio_file.file, buffer)
        
        result = engine.process_answer(session_id, audio_file_path=temp_file, text_answer=text_answer)
        
        # Cleanup
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
            
        return result

    except Exception as e:
        if temp_file and os.path.exists(temp_file):
            try: os.remove(temp_file)
            except: pass
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/results/{session_id}")
async def get_results(session_id: str, engine: SimVoiceInterviewer = Depends(get_engine)):
    """
    Get comprehensive interview results and analytics
    """
    try:
        session = engine.sessions.get(session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        # Calculate analytics
        scores = session.get("scores", [])
        overall_score = round(sum(scores) / len(scores), 1) if scores else 0
        
        # Identify strengths (scores > 75) and weaknesses (scores < 60)
        strengths = []
        weaknesses = []
        
        # Get question-by-question review
        question_review = []
        history = session.get("history", [])
        q_bank = session.get("q_bank", [])
        
        # Parse conversation history to extract Q&A pairs
        for i in range(0, len(history) - 1, 2):
            if i + 1 < len(history):
                ai_msg = history[i]
                user_msg = history[i + 1]
                
                if ai_msg["role"] == "assistant" and user_msg["role"] == "user":
                    q_num = i // 2
                    score = scores[q_num] if q_num < len(scores) else None
                    
                    question_review.append({
                        "question_number": q_num + 1,
                        "question": ai_msg["content"],
                        "answer": user_msg["content"],
                        "score": score
                    })
                    
                    # Categorize as strength or weakness
                    if score:
                        if score >= 75:
                            strengths.append(f"Question {q_num + 1}: Strong answer (Score: {score})")
                        elif score < 60:
                            weaknesses.append(f"Question {q_num + 1}: Needs improvement (Score: {score})")
        
        # Generate recommendations
        recommendations = []
        if overall_score < 60:
            recommendations.append("Focus on understanding fundamental concepts before moving to advanced topics")
            recommendations.append("Practice explaining your answers with more detail and examples")
        elif overall_score < 75:
            recommendations.append("Good foundation! Work on providing more comprehensive explanations")
            recommendations.append("Try to include real-world examples in your answers")
        else:
            recommendations.append("Excellent performance! Continue practicing to maintain consistency")
            recommendations.append("Consider exploring more advanced topics in this area")
        
        # Add topic-specific recommendations
        if session.get("weak_areas"):
            weak_topics = list(set(session["weak_areas"]))[:3]
            recommendations.append(f"Review these topics: {', '.join(weak_topics)}")
        
        return {
            "session_id": session_id,
            "interview_type": session.get("interview_type", "technical"),
            "topic": session.get("topic", "realtime"),
            "overall_score": overall_score,
            "total_questions": len(q_bank),
            "questions_answered": session.get("answer_count", 0),
            "scores": scores,
            "strengths": strengths if strengths else ["Keep practicing to identify your strengths"],
            "weaknesses": weaknesses if weaknesses else ["Great job! No major weaknesses identified"],
            "recommendations": recommendations,
            "question_review": question_review,
            "performance_rating": (
                "Excellent" if overall_score >= 85 else
                "Good" if overall_score >= 70 else
                "Fair" if overall_score >= 55 else
                "Needs Improvement"
            )
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

