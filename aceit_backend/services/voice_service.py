import os
import whisper

# Global Whisper Model (Lazy Loaded)
_WHISPER_MODEL = None

class VoiceService:
    def __init__(self):
        pass
        
    def transcribe(self, file_path: str) -> str:
        """
        Transcribes audio file using Groq Whisper API (Fast & Fail-safe).
        """
        if not os.path.exists(file_path):
             return "Error: Audio file not found."

        try:
            from groq import Groq
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                return "Error: GROQ_API_KEY missing for voice input."
                
            client = Groq(api_key=api_key)
            
            with open(file_path, "rb") as file:
                transcription = client.audio.transcriptions.create(
                    file=(os.path.basename(file_path), file.read()),
                    model="whisper-large-v3-turbo",
                    response_format="json",
                    language="en",
                    temperature=0.0
                )
            
            text = transcription.text.strip()
            return text
            
        except Exception as e:
            print(f"[ERROR] Groq STT error: {e}")
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
