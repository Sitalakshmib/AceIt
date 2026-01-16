import json
import uuid
import asyncio
from datetime import datetime
from services.llm_client import LLMClient
from services.voice_service import voice_service

class SimVoiceInterviewer:
    def __init__(self):
        self.llm = LLMClient()
        self.sessions = {} # In-memory store
        
    def start_interview(self, user_id: str, resume: str = "", jd: str = ""):
        """
        Initializes session, generates Question Bank, and first question.
        """
        session_id = str(uuid.uuid4())
        
        # 1. Generate Question Bank (SimInterview Logic)
        print(f"[SimVoice] Generating Question Bank for {session_id}...")
        try:
            q_bank = self._generate_question_bank(resume, jd)
            print(f"[SimVoice] Question Bank Generated: {len(q_bank)} questions")
        except Exception as e:
            print(f"[ERROR] [SimVoice] Question Bank Failed: {e}")
            q_bank = ["Tell me about yourself."] # Fallback

        # 2. Create Session
        session = {
            "id": session_id,
            "user_id": user_id,
            "resume": resume,
            "jd": jd,
            "q_bank": q_bank,
            "history": [], # raw conversation
            "current_q_index": 0,
            "status": "active"
        }
        self.sessions[session_id] = session
        
        # 3. First Question (Intro)
        initial_text = f"Hello! I am your AI Interviewer. I have prepared {len(q_bank)} questions. Let's begin. Please introduce yourself."
        
        print(f"[SimVoice] Synthesizing Intro: {initial_text[:30]}...")
        audio_url = voice_service.synthesize(initial_text)
        print(f"[SimVoice] Audio Ready: {audio_url}")
        
        # Record AI turn
        self._add_history(session_id, "assistant", initial_text)
        
        return {
            "session_id": session_id,
            "text": initial_text,
            "audio_url": audio_url,
            "question_index": 0,
            "total_questions": len(q_bank)
        }

    def process_answer(self, session_id: str, audio_file_path: str = None, text_answer: str = None):
        """
        Processes user answer (Audio or Text).
        Returns the NEXT question (Text + Audio).
        """
        if session_id not in self.sessions:
            raise ValueError("Invalid Session")
            
        session = self.sessions[session_id]
        
        # 1. Get User Text
        user_text = text_answer or ""
        if audio_file_path:
            print(f"[SimVoice] Transcribing answer for {session_id}...")
            user_text = voice_service.transcribe(audio_file_path)
        
        print(f"[SimVoice] User Said: {user_text}")
        self._add_history(session_id, "user", user_text)
        
        # 2. Generate AI Response (Next Question or Follow-up)
        # We use the Question Bank + History
        
        next_q_text = self._generate_ai_response(session)
        
        # 3. Synthesize Voice
        print(f"[SimVoice] AI Replying: {next_q_text}")
        audio_url = voice_service.synthesize(next_q_text)
        
        # 4. Update History
        self._add_history(session_id, "assistant", next_q_text)
        session["current_q_index"] += 1
        
        return {
            "text": next_q_text,
            "audio_url": audio_url,
            "is_completed": session["current_q_index"] >= len(session["q_bank"])
        }

    def _generate_question_bank(self, resume, jd):
        """
        Asks LLM to generate list of questions based on JD/Resume.
        """
        prompt = f"""
        You are an expert Technical Recruiter.
        Create a list of 5 interview questions based on the following context.
        
        Resume: {resume[:2000]}
        Job Description: {jd[:2000]}
        
        Rules:
        1. Mix of Behavioral, Technical, and Experience-based.
        2. Return ONLY a JSON list of strings. Example: ["Question 1", "Question 2"]
        """
        try:
            res = self.llm.generate_response(prompt)
            clean = res.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except:
            return [
                "Tell me about a challenging project you worked on.",
                "What are your strengths and weaknesses?",
                "Describe your experience with Python.",
                "How do you handle conflict in a team?"
            ]

    def _generate_ai_response(self, session):
        """
        Decides what to say next.
        """
        # Simple Logic: Check if we have more questions in bank.
        # But also acknowledge the previous answer.
        
        history_str = "\n".join([f"{m['role']}: {m['content']}" for m in session["history"][-4:]])
        
        # Next topic from bank
        idx = session["current_q_index"]
        next_topic = session["q_bank"][idx] if idx < len(session["q_bank"]) else "Conclusion"
        
        prompt = f"""
        You are an AI Interviewer.
        
        Conversation History:
        {history_str}
        
        Your Goal:
        1. Acknowledge the candidate's last answer briefly (be natural).
        2. Transition to the next question: "{next_topic}".
        3. If the interview is over (no more questions), thank them.
        
        Keep it conversational and professional. Speak as if you are talking (no markdown, no bullets).
        """
        
        res = self.llm.generate_response(prompt)
        if res is None:
            # Fallback if LLM fails
            return f"Thank you for your answer. Let's move on to: {next_topic}"
        return res.strip()

    def _add_history(self, session_id, role, content):
        self.sessions[session_id]["history"].append({"role": role, "content": content})

