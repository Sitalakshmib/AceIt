import os
import whisper

# Global Whisper Model (Lazy Loaded)
_WHISPER_MODEL = None

class VoiceService:
    def __init__(self):
        pass
        
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
        Text-to-speech synthesis disabled.
        Audio files are no longer saved to static/audio directory.
        Returns empty string.
        """
        # Audio saving disabled - no longer creating files in static/audio
        return ""

voice_service = VoiceService()
