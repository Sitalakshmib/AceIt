import os
import shutil
import whisper
from gtts import gTTS
import uuid

# Global Whisper Model (Lazy Loaded)
_WHISPER_MODEL = None

class VoiceService:
    def __init__(self, static_dir="static/audio"):
        self.static_dir = static_dir
        os.makedirs(self.static_dir, exist_ok=True)
        
    def _load_whisper(self):
        global _WHISPER_MODEL
        if _WHISPER_MODEL is None:
            print("Loading Whisper model...")
            try:
                _WHISPER_MODEL = whisper.load_model("base")
                print("Whisper loaded.")
            except Exception as e:
                print(f"[ERROR] Whisper load failed: {e}")
                raise RuntimeError("STT Model failed to load.")

    def transcribe(self, file_path: str) -> str:
        """
        Transcribes audio file using Whisper.
        """
        # Fallback check (if file doesn't exist)
        if not os.path.exists(file_path):
             return "Error: Audio file not found."

        try:
            self._load_whisper()
            result = _WHISPER_MODEL.transcribe(
                file_path,
                language="en",
                fp16=False # safe for CPU
            )
            return result["text"].strip()
        except Exception as e:
            print(f"[ERROR] Transcription error: {e}")
            return "I could not hear that clearly."

    def synthesize(self, text: str) -> str:
        """
        Converts text to speech using gTTS.
        Returns the relative path to the audio file (for frontend access).
        """
        try:
            filename = f"speech_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(self.static_dir, filename)
            
            # Generate speech
            tts = gTTS(text=text, lang='en')
            tts.save(filepath)
            
            return f"/static/audio/{filename}" # Web-accessible path
        except Exception as e:
            print(f"[ERROR] TTS Error: {e}")
            return ""

voice_service = VoiceService()
