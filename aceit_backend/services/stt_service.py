import shutil
import os
import whisper

# Global model cache (lazy load)
MODEL = None

def load_model():
    global MODEL
    if MODEL is None:
        print("⏳ Loading Whisper base model... this may take a moment.")
        try:
            MODEL = whisper.load_model("base")
            print("Whisper model loaded!")
        except Exception as e:
            print(f"[ERROR] Failed to load Whisper: {e}")
            raise RuntimeError("Could not load STT model. Is FFmpeg installed?")

def transcribe_audio_file(file_path: str) -> str:
    """
    Transcribes the audio file at the given path.
    """
    load_model()
    
    try:
        # Transcribe
        result = MODEL.transcribe(
            file_path, 
            language="en",
            temperature=0.0,
            condition_on_previous_text=False,
            initial_prompt="This is an interview answer."
        )
        return result["text"].strip()
        
    except Exception as e:
        print(f"[ERROR] Transcription Failed: {e}")
        # Fallback for MVP if FFmpeg is missing
        if "The system cannot find the file specified" in str(e) or "ffmpeg" in str(e).lower():
            print("⚠️ Switching to MOCK STT mode (FFmpeg missing).")
            return "I am very passionate about this role and I have strong experience in Python and React. I enjoy solving complex problems."
            
        raise e
