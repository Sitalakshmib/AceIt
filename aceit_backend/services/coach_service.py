import os
import io
import json
import requests
from typing import List, Dict, Optional
from openai import OpenAI
from sqlalchemy.orm import Session
from services.ai_analytics_service import AIAnalyticsService

class AICoachService:
    @staticmethod
    def get_chat_response(db: Session, user_id: str, message: str, history: List[Dict]) -> str:
        """
        Get a conversational response from the AI coach based on user's progress.
        Uses GROQ as primary, OpenAI as fallback.
        """
        # Get summarized context to make the coach "real-time" and personal
        summary = AIAnalyticsService.get_overall_summary(db, user_id)
        topic_info = AIAnalyticsService.get_mock_topic_performance(db, user_id)
        
        system_prompt = f"""
        You are an encouraging and highly skilled Aptitude Career Coach. 
        A student is asking you for guidance. Here is their current status:
        - Accuracy: {summary['exam_confidence']}%
        - Pace: {summary['pace_ratio']}x
        - Strengths: {', '.join(topic_info['strengths']) if topic_info['strengths'] else 'Unknown'}
        - Weaknesses: {', '.join(topic_info['weaknesses']) if topic_info['weaknesses'] else 'Unknown'}
        
        Instructions:
        1. Be supportive but realistic.
        2. Reference their specific stats if relevant to their question.
        3. Provide actionable tips for aptitude tests (Quantitative, Logical, Verbal).
        4. Keep responses concise (under 3 sentences unless they ask for a detailed explanation).
        """
        
        messages = [{"role": "system", "content": system_prompt}]
        for h in history:
            messages.append(h)
        messages.append({"role": "user", "content": message})
        
        # Try GROQ first
        try:
            groq_key = os.getenv("GROQ_API_KEY_SITA")
            if groq_key:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {groq_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.3-70b-versatile",
                        "messages": messages,
                        "temperature": 0.7
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f"[COACH] GROQ failed with status {response.status_code}, falling back to OpenAI")
        except Exception as e:
            print(f"[COACH] GROQ error: {e}, falling back to OpenAI")
        
        # Fallback to OpenAI
        try:
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_SITA"))
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[COACH] OpenAI fallback also failed: {e}")
            return "I'm having trouble connecting right now. Please try again in a moment."

    @staticmethod
    def transcript_audio(audio_file_content: bytes) -> str:
        """
        Convert speech to text using OpenAI Whisper.
        Note: GROQ doesn't support Whisper, so using OpenAI directly.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_SITA"))
        
        # Audio file must be buffered
        buffer = io.BytesIO(audio_file_content)
        buffer.name = "audio.webm" # Common for browser recordings
        
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=buffer
        )
        
        return transcript.text

    @staticmethod
    def text_to_speech(text: str) -> bytes:
        """
        Convert text to speech using OpenAI TTS.
        Note: GROQ doesn't support TTS, so using OpenAI directly.
        """
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY_SITA"))
        
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        
        return response.content
