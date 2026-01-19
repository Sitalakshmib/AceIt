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
        
    def start_interview(self, user_id: str, resume: str = "", jd: str = "", interview_type: str = "technical"):
        """
        Initializes session, generates Question Bank, and first question.
        """
        session_id = str(uuid.uuid4())
        
        # 1. Generate Question Bank (SimInterview Logic)
        print(f"[SimVoice] Generating {interview_type.upper()} Question Bank for {session_id}...")
        try:
            q_bank = self._generate_question_bank(resume, jd, interview_type)
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
            "interview_type": interview_type,
            "q_bank": q_bank,
            "history": [], # raw conversation
            "current_q_index": 0,
            "status": "active"
        }
        self.sessions[session_id] = session
        
        # 3. First Question (Intro)
        interview_label = "Technical" if interview_type == "technical" else "HR/Behavioral"
        initial_text = f"Hello! I am your AI Interviewer for this {interview_label} interview. I have prepared {len(q_bank)} questions. Let's begin. Please introduce yourself."
        
        print(f"[SimVoice] Starting {interview_type} interview")
        
        # Record AI turn
        self._add_history(session_id, "assistant", initial_text)
        
        return {
            "session_id": session_id,
            "text": initial_text,
            "audio_url": "",  # No audio in text-only mode
            "question_index": 0,
            "total_questions": len(q_bank)
        }

    def process_answer(self, session_id: str, audio_file_path: str = None, text_answer: str = None):
        """
        Processes user answer (Audio or Text).
        Returns the NEXT question (Text only in text mode).
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
        next_q_text = self._generate_ai_response(session)
        
        # 3. Update History
        self._add_history(session_id, "assistant", next_q_text)
        session["current_q_index"] += 1
        
        return {
            "text": next_q_text,
            "audio_url": "",  # No audio in text-only mode
            "is_completed": session["current_q_index"] >= len(session["q_bank"])
        }

    def _generate_question_bank(self, resume, jd, interview_type):
        """
        Asks LLM to generate list of questions based on JD/Resume and interview type.
        """
        if interview_type == "technical":
            prompt = f"""
You are an expert Technical Interviewer.
Create a list of 5 technical interview questions based on the following context.

Resume: {resume[:2000]}
Job Description: {jd[:2000]}

Rules:
1. Focus on: Coding skills, algorithms, data structures, system design, technical problem-solving
2. If the candidate mentions specific technologies (e.g., Python, React), ask deep questions about those
3. Include at least one coding/algorithm question
4. Include at least one system design or architecture question
5. Make questions progressively harder
6. Return ONLY a JSON list of strings. Example: ["Question 1", "Question 2"]

Be specific and technical. If they mention Python, ask about Python internals, decorators, async/await, etc.
"""
        else:  # HR/Behavioral
            prompt = f"""
You are an expert HR Interviewer.
Create a list of 5 behavioral/HR interview questions based on the following context.

Resume: {resume[:2000]}
Job Description: {jd[:2000]}

Rules:
1. Focus on: Soft skills, teamwork, conflict resolution, leadership, work ethic, culture fit
2. Use STAR method questions (Situation, Task, Action, Result)
3. Ask about their experience, challenges faced, and how they handled them
4. Include questions about their career goals and motivations
5. Return ONLY a JSON list of strings. Example: ["Question 1", "Question 2"]

Examples:
- "Tell me about a time when you faced a difficult challenge at work. How did you handle it?"
- "Describe a situation where you had to work with a difficult team member."
- "What motivates you in your career?"
"""
        
        try:
            res = self.llm.generate_response(prompt)
            clean = res.replace("```json", "").replace("```", "").strip()
            return json.loads(clean)
        except Exception as e:
            print(f"[ERROR] Question generation failed: {e}")
            # Fallback questions based on type
            if interview_type == "technical":
                return [
                    "Tell me about a challenging technical problem you solved recently.",
                    "Explain how you would design a scalable system for [specific use case].",
                    "What are your strongest programming languages and why?",
                    "Describe your experience with databases and data modeling."
                ]
            else:
                return [
                    "Tell me about a time when you faced a difficult challenge at work.",
                    "How do you handle conflict in a team?",
                    "What are your strengths and weaknesses?",
                    "Where do you see yourself in 5 years?"
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

