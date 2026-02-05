from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
from services.stt_service import transcribe_audio_file

router = APIRouter()

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Receives an audio file (wav/mp3), saves it temporarily, 
    and returns textual transcription using OpenAI Whisper.
    """
    
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Transcribe using service
        text = transcribe_audio_file(temp_filename)
        
        return {"text": text}
        
    except Exception as e:
        print(f"[ERROR] Transcription Failed: {e}") 
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        
    finally:
        # Cleanup
        if os.path.exists(temp_filename):
           try: os.remove(temp_filename)
           except: pass
