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

class NextResponse(BaseModel):
    text: str
    audio_url: str
    is_completed: bool

# --- Routes ---

@router.post("/start")
async def start_interview(req: StartRequest, engine: SimVoiceInterviewer = Depends(get_engine)):
    print(f"[INTERVIEW] /interview/start hit by User: {req.user_id}")
    try:
        result = engine.start_interview(req.user_id, req.resume_text, req.jd_text)
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
