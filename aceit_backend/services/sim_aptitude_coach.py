import json
import uuid
from datetime import datetime
from services.llm_client import LLMClient
from services.voice_service import voice_service
from services.ai_analytics_service import AIAnalyticsService

class SimAptitudeCoach:
    def __init__(self):
        self.llm = LLMClient(groq_env_key="GROQ_API_KEY_SITA", openai_env_key="OPENAI_API_KEY_SITA")
        self.sessions = {} # In-memory store (similar to SimVoiceInterviewer)
        
    def start_session(self, user_id: str, db):
        """
        Initializes an aptitude coaching session with fresh context.
        """
        session_id = str(uuid.uuid4())
        
        # Get latest performance context
        summary = AIAnalyticsService.get_overall_summary(db, user_id)
        topic_info = AIAnalyticsService.get_mock_topic_performance(db, user_id)
        
        # Initial greeting
        initial_text = f"Hello! I'm your AI Coach. I see your current exam confidence is at {summary['exam_confidence']}%. How can I help you sharpen your skills today?"
        
        session = {
            "id": session_id,
            "user_id": user_id,
            "history": [{"role": "assistant", "content": initial_text}],
            "stats_context": {
                "accuracy": summary['exam_confidence'],
                "pace": summary['pace_ratio'],
                "strengths": topic_info['strengths'],
                "weaknesses": topic_info['weaknesses']
            },
            "start_time": datetime.now()
        }
        
        self.sessions[session_id] = session
        
        # Generate TTS audio for greeting
        audio_url = voice_service.synthesize(initial_text)
        
        return {
            "session_id": session_id,
            "text": initial_text,
            "audio_url": audio_url
        }

    def process_message(self, session_id: str, db, audio_file_path: str = None, text_message: str = None):
        """
        Processes user query (Audio or Text) and returns coach's advice.
        """
        if session_id not in self.sessions:
            # Try to recover or create a new one if user_id is provided? 
            # For now, standard error handling
            raise ValueError("Invalid Session")
            
        session = self.sessions[session_id]
        user_id = session["user_id"]
        
        # 1. Get User Text
        user_text = text_message or ""
        if audio_file_path:
            user_text = voice_service.transcribe(audio_file_path)
            
        if not user_text:
            return {"error": "Empty message"}

        session["history"].append({"role": "user", "content": user_text})
        
        # 2. Get AI Response
        # LATENCY OPTIMIZATION: Use cached stats context from the session 
        # instead of re-querying the database on every message.
        stats = session.get("stats_context", {})
        accuracy = stats.get("accuracy", "Unknown")
        pace = stats.get("pace", "Unknown")
        strengths = stats.get("strengths", [])
        weaknesses = stats.get("weaknesses", [])
        
        system_prompt = f"""
        You are an encouraging and highly skilled Aptitude Career Coach. 
        A student is asking you for guidance. Here is their current REAL-TIME status:
        - Accuracy: {accuracy}%
        - Pace: {pace}x
        - Strengths: {', '.join(strengths) if strengths else 'None yet'}
        - Weaknesses: {', '.join(weaknesses) if weaknesses else 'None yet'}
        
        Instructions:
        1. Be supportive but realistic.
        2. Reference their specific stats if relevant to their question.
        3. Provide actionable tips for aptitude tests (Quantitative, Logical, Verbal).
        4. Keep responses CONCISE, PRECISE, and of MEDIUM LENGTH.
        5. DO NOT provide long paragraphs or unnecessary filler.
        6. Tone: Professional, encouraging, engineer-to-engineer.
        """
        
        # Construct history for LLM
        messages = [{"role": "system", "content": system_prompt}]
        # Limit history to prevent context overflow (last 10 turns)
        messages.extend(session["history"][-10:])
        
        try:
            ai_text = self.llm.generate_response_from_messages(messages)
            session["history"].append({"role": "assistant", "content": ai_text})
            
            # LATENCY OPTIMIZATION: Audio is no longer generated automatically for replies.
            # Frontend will request it on-demand when "Replay" is clicked.
            return {
                "text": ai_text,
                "audio_url": None, # Audio generated on-demand
                "is_completed": False
            }
        except Exception as e:
            print(f"[AptitudeCoach] LLM Failed: {e}")
            return {
                "text": "I'm having a bit of trouble connecting to my brain right now! (Model busy). Please try again in 30 seconds.",
                "error": str(e),
                "audio_url": None
            }
