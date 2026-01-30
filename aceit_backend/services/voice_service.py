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
        Returns base64 encoded audio string (data URI).
        NO FILES SAVED TO DISK.
        """
        try:
            from gtts import gTTS
            import io
            import base64
            
            # Generate speech to memory buffer
            tts = gTTS(text=text, lang='en', slow=False)
            mp3_fp = io.BytesIO()
            tts.write_to_fp(mp3_fp)
            
            # Encode to base64
            mp3_fp.seek(0)
            b64_data = base64.b64encode(mp3_fp.read()).decode("utf-8")
            
            # Return Data URI
            return f"data:audio/mp3;base64,{b64_data}"
            
        except Exception as e:
            print(f"[ERROR] TTS synthesis failed: {e}")
            return ""  # Return empty string on failure

voice_service = VoiceService()
