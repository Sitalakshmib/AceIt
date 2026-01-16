import json
import uuid
from typing import Dict, Optional
from datetime import datetime
from services.llm_client import LLMClient

class SimInterviewEngine:
    def __init__(self):
        self.llm = LLMClient()
        self.sessions = {}  # In-memory session store

    def start_interview(self, user_id: str, resume_text: str = None, jd_text: str = None, tech_stack: str = None) -> dict:
        """
        Initializes a new interview session.
        """
        session_id = str(uuid.uuid4())
        
        # Fallback context if resume/jd are missing (legacy frontend support)
        if not resume_text:
            resume_text = f"Candidate interested in {tech_stack or 'General'} roles."
        if not jd_text:
            jd_text = f"Job requires expertise in {tech_stack or 'General Technical Skills'}."

        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "resume_text": resume_text,
            "jd_text": jd_text,
            "tech_stack": tech_stack,
            "history": [], # List of {role: user/ai, content: text}
            "question_count": 0,
            "scores": [],
            "start_time": datetime.utcnow().isoformat(),
            "status": "active"
        }
        
        self.sessions[session_id] = session_data
        
        # Generate first question
        first_q_text = self._generate_initial_question(resume_text, jd_text, tech_stack)
        self._record_interaction(session_id, "ai", first_q_text)
        
        # Return format matching InterviewResponse.current_question mostly
        return {
            "session_id": session_id,
            "current_question": {
                "id": "q1",
                "text": first_q_text,
                "topic": tech_stack or "intro",
                "difficulty": "easy"
            },
            "feedback": "Welcome to the interview.",
            "score": 0,
            "is_completed": False
        }

    def process_answer(self, session_id: str, answer_text: str):
        """
        Records the user's answer.
        """
        if session_id not in self.sessions:
            raise ValueError("Session not found")
            
        self._record_interaction(session_id, "user", answer_text)

    def generate_next_question(self, session_id: str) -> dict:
        """
        Generates the next question based on history.
        """
        if session_id not in self.sessions:
            raise ValueError("Session not found")
            
        session = self.sessions[session_id]
        
        # Build prompt
        prompt = self._build_next_question_prompt(session)
        
        # Call LLM
        response_text = self.llm.generate_response(prompt)
        parsed_response = self._parse_json_response(response_text)
        
        # Update session
        session["question_count"] += 1
        if parsed_response.get("score"):
            session["scores"].append(parsed_response["score"])
            
        self._record_interaction(session_id, "ai", parsed_response["question"])
        
        return {
            "current_question": {
                "id": f"q{session['question_count']}",
                "text": parsed_response["question"],
                "topic": parsed_response.get("topic", "general"),
                "difficulty": parsed_response.get("difficulty", "medium")
            },
            "feedback": parsed_response.get("feedback", ""),
            "score": parsed_response.get("score", 0),
            "is_completed": session["question_count"] >= 10
        }

    def end_interview(self, session_id: str) -> dict:
        """
        Finalizes the interview and generates a report.
        """
        if session_id not in self.sessions:
            raise ValueError("Session not found")
        
        session = self.sessions[session_id]
        session["status"] = "completed"
        
        return {
            "session_id": session_id,
            "message": "Interview completed.",
            "total_questions": session["question_count"],
            "average_score": sum(session["scores"]) / len(session["scores"]) if session["scores"] else 0
        }

    # --- Helpers ---

    def _record_interaction(self, session_id, role, text):
        self.sessions[session_id]["history"].append({"role": role, "content": text})

    def _generate_initial_question(self, resume, jd, tech_stack=None):
        prompt = f"""
        You are an expert AI Interviewer.
        
        Context:
        Resume: {resume[:500]}
        Job Description: {jd[:500]}
        Tech Stack Focus: {tech_stack or "General"}
        
        Start the interview. 
        If a specific Tech Stack is mentioned, ask a conceptual question about it to start.
        Otherwise, ask the candidate to introduce themselves.
        Keep it professional.
        Return ONLY the question text.
        """
        response = self.llm.generate_response(prompt)
        if not response:
            return "Could you tell me about yourself?"
        return response.strip()

    def _build_next_question_prompt(self, session):
        # Construct history string
        history_str = ""
        # Get last 6 turns (3 Q&A pairs) to save context window
        recent_history = session["history"][-6:]
        for msg in recent_history:
            role = "Interviewer" if msg["role"] == "ai" else "Candidate"
            history_str += f"{role}: {msg['content']}\n"

        return f"""
        You are an expert AI Interviewer.
        
        History:
        {history_str}
        
        Task:
        1. Analyze the candidate's last answer.
        2. Provide brief feedback (internal thought, output in JSON).
        3. Score the answer (0-100).
        4. Ask the NEXT relevant interview question. Use the Resume and JD context implicitly.
           - If the answer was weak, ask a follow-up or simpler question.
           - If strong, increase difficulty.
           - Stay on topic but move to technical details if appropriate.
        5. Check if the interview should end (if user says "bye" or refuses to answer).
        
        Output JSON format:
        {{
            "question": "The actual question text",
            "topic": "The topic (e.g., python, behavior, system_design)",
            "difficulty": "easy|medium|hard",
            "feedback": "Constructive feedback on the last answer",
            "score": 85,
            "is_completed": false
        }}
        """

    def _parse_json_response(self, text: str) -> dict:
        fallback = {
            "question": "Could you elaborate on that further?",
            "topic": "general",
            "difficulty": "medium",
            "feedback": "Please continue.",
            "score": 50,
            "is_completed": False
        }
        
        if not text:
            return fallback

        try:
            # Clean markdown code blocks if present
            cleaned = text.replace("```json", "").replace("```", "").strip()
            data = json.loads(cleaned)
            return data
        except json.JSONDecodeError:
            print(f"JSON Parse Error. Raw text: {text}")
            return fallback

