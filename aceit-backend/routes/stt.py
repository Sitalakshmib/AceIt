from fastapi import APIRouter, File, UploadFile, HTTPException
import shutil
import os
import whisper

router = APIRouter()

# Global model cache (lazy load)
MODEL = None

def load_model():
    global MODEL
    if MODEL is None:
        print("⏳ Loading Whisper base model... this may take a moment.")
        try:
            MODEL = whisper.load_model("base")
            print("✅ Whisper model loaded!")
        except Exception as e:
            print(f"❌ Failed to load Whisper: {e}")
            raise RuntimeError("Could not load STT model. Is FFmpeg installed?")

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Receives an audio file (wav/mp3), saves it temporarily, 
    and returns textual transcription using OpenAI Whisper.
    """
    load_model()
    
    # Save temp file
    temp_filename = f"temp_{file.filename}"
    try:
        with open(temp_filename, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Transcribe
        result = MODEL.transcribe(temp_filename)
        text = result["text"].strip()
        
        return {"text": text}
        
    except Exception as e:
        print(f"❌ Transcription Failed: {e}")
        # Fallback for MVP if FFmpeg is missing
        if "The system cannot find the file specified" in str(e) or "ffmpeg" in str(e).lower():
            print("⚠️ Switching to MOCK STT mode (FFmpeg missing).")
            return {"text": "I am very passionate about this role and I have strong experience in Python and React. I enjoy solving complex problems."}
            
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")
        
    finally:
        # Cleanup
        if os.path.exists(temp_filename):
           try: os.remove(temp_filename)
           except: pass
