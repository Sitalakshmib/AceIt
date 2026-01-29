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
        Text-to-speech synthesis using gTTS.
        Saves audio file to static/audio directory.
        Returns the URL path to the audio file.
        """
        try:
            from gtts import gTTS
            import uuid
            
            # Create static/audio directory if it doesn't exist
            audio_dir = "static/audio"
            os.makedirs(audio_dir, exist_ok=True)
            
            # Generate unique filename
            filename = f"response_{uuid.uuid4().hex[:8]}.mp3"
            filepath = os.path.join(audio_dir, filename)
            
            # Generate speech
            tts = gTTS(text=text, lang='en', slow=False)
            tts.save(filepath)
            
            # Return URL path (relative to static mount)
            return f"/static/audio/{filename}"
            
        except Exception as e:
            print(f"[ERROR] TTS synthesis failed: {e}")
            return ""  # Return empty string on failure

voice_service = VoiceService()
