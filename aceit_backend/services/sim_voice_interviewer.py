import json
import uuid
import asyncio
from datetime import datetime
from services.llm_client import LLMClient
from services.voice_service import voice_service
from services.topic_prompts import TOPIC_PROMPTS

class SimVoiceInterviewer:
    def __init__(self):
        self.llm = LLMClient()
        self.sessions = {} # In-memory store
        
    def start_interview(self, user_id: str, resume: str = "", jd: str = "", interview_type: str = "technical", topic: str = "realtime", project_text: str = ""):
        """
        Initializes session, generates Question Bank, and first question.
        """
        session_id = str(uuid.uuid4())
        
        # 1. Generate Question Bank (SimInterview Logic)
        print(f"[SimVoice] Generating {interview_type.upper()} Question Bank for {session_id}... Topic: {topic}")
        try:
            q_bank = self._generate_question_bank(resume, jd, interview_type, topic, round_num=1, project_text=project_text)
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
            "topic": topic,
            "project_text": project_text, # Store project description
            "q_bank": q_bank,
            "history": [], # raw conversation
            "current_q_index": 0,
            "answer_count": 0,  # Track answers for periodic feedback
            "status": "active",
            "round": 1,
            "weak_areas": [] # Track weak concepts
        }
        self.sessions[session_id] = session
        
        # 3. First Question (Intro or Direct Technical Start)
        topic = session.get("topic", "realtime")
        
        if interview_type == "project":
            # Project-based mode: Start with project discussion
            initial_text = f"Hello! I've reviewed your project description. It sounds interesting. Let's discuss the architecture and your implementation choices. {q_bank[0] if q_bank else 'Can you give me a high-level overview?'}"
            session["current_q_index"] = 1  # Logic fix: Q1 asked
        elif topic != "realtime" and interview_type == "technical":
            # Topic-specific mode: Start directly with first technical question (no intro)
            topic_name = topic.upper() if topic != "dotnet" else ".NET Core"
            initial_text = f"Hello! Let's practice {topic_name} concepts. {q_bank[0] if q_bank else 'What do you know about this topic?'}"
            session["current_q_index"] = 1  # Logic fix: Q1 asked
        else:
            # Realtime or HR mode: Use standard intro
            interview_label = "Technical" if interview_type == "technical" else "HR/Behavioral"
            initial_text = f"Hello! I am your AI Interviewer for this {interview_label} interview. I have prepared {len(q_bank)} questions. Let's begin. Please introduce yourself."
        
        print(f"[SimVoice] Starting {interview_type} interview (Topic: {topic})")
        
        # Record AI turn
        self._add_history(session_id, "assistant", initial_text)
        
        # Generate TTS audio for initial greeting
        audio_url = voice_service.synthesize(initial_text)
        
        return {
            "session_id": session_id,
            "text": initial_text,
            "audio_url": audio_url,
            "question_index": 0,
            "total_questions": len(q_bank)
        }

    def start_round_2(self, session_id):
        """
        Starts Round 2 for the given session.
        """
        session = self.sessions[session_id]
        topic = session['topic']
        
        # 1. Generate Round 2 Questions
        print(f"[SimVoice] Starting Round 2 for {session_id} ({topic})...")
        new_q_bank = self._generate_question_bank(
            session['resume'], session['jd'], session['interview_type'], 
            topic=topic, round_num=2, weak_areas=session['weak_areas']
        )
        
        # 2. Update Session
        session['q_bank'] = new_q_bank
        session['current_q_index'] = 0
        session['round'] = 2
        session['status'] = 'active'
        
        # 3. Transition Message
        next_q_text = f"Great! Let's start Round 2. We'll dive a bit deeper into {topic.upper()} concepts. {new_q_bank[0]}"
        
        # Update History
        self._add_history(session_id, "assistant", next_q_text)
        session["current_q_index"] += 1
        
        # Generate Audio
        audio_url = voice_service.synthesize(next_q_text)
        
        return {
            "text": next_q_text,
            "audio_url": audio_url,
            "is_completed": False
        }

    def process_answer(self, session_id: str, audio_file_path: str = None, text_answer: str = None):
        """
        Processes user answer (Audio or Text).
        Returns the NEXT question (Text only in text mode).
        """
        if session_id not in self.sessions:
            raise ValueError("Invalid Session")
            
        session = self.sessions[session_id]
        
        # --- ROUND 2 TRANSITION HANDLING ---
        if session.get("status") == "awaiting_round_2_confirmation":
            confirm = (text_answer or "").strip().lower()
            if "yes" in confirm or "sure" in confirm or "ok" in confirm or "ready" in confirm:
                return self.start_round_2(session_id)
            else:
                # User declined Round 2
                final_bye = "No problem! Great practice session today. Keep learning!"
                audio_url = voice_service.synthesize(final_bye)
                return {"text": final_bye, "audio_url": audio_url, "is_completed": True}

        # 1. Get User Text
        user_text = text_answer or ""
        if audio_file_path:
            print(f"[SimVoice] Transcribing answer for {session_id}...")
            user_text = voice_service.transcribe(audio_file_path)
            
        # Detect weak answer (simple heuristic for now)
        if len(user_text.split()) < 5 or "don't know" in user_text.lower() or "unsure" in user_text.lower():
            current_topic = session["q_bank"][session["current_q_index"]-1] if session["current_q_index"] > 0 else "General"
            session["weak_areas"].append(current_topic)
        
        print(f"[SimVoice] User Said: {user_text}")
        self._add_history(session_id, "user", user_text)
        
        # 2. Increment answer count
        session["answer_count"] += 1
        
        # 3. Check if CURRENT ROUND is complete
        is_completed = session["current_q_index"] >= len(session["q_bank"])
        
        # 4. Generate AI Response
        feedback_data = None
        if is_completed:
            if session['round'] == 1 and session['topic'] != "realtime":
                # Offer Round 2
                session['status'] = "awaiting_round_2_confirmation"
                summary_text = self._generate_final_summary(session)
                next_q_text = f"{summary_text}\n\nWould you like to attempt Round 2? I'll ask some questions on topics you found tricky and go a bit deeper."
            else:
                # Final End (Realtime mode or Round 2 end)
                next_q_text = self._generate_final_summary(session)
        else:
            # Get structured feedback response
            ai_response = self._generate_ai_response(session)
            
            # Handle both dict (new format) and string (fallback)
            if isinstance(ai_response, dict):
                next_q_text = ai_response.get("next_question", "Let's continue.")
                feedback_data = {
                    "score": ai_response.get("score", 50),
                    "quality": ai_response.get("quality", "needs_work"),
                    "feedback_text": ai_response.get("feedback_text", "Thank you for your answer.")
                }
            else:
                # Backward compatibility - if string is returned
                next_q_text = ai_response
        
        # 5. Update History & Audio
        self._add_history(session_id, "assistant", next_q_text)
        session["current_q_index"] += 1
        
        # Generate TTS audio for AI response
        audio_url = voice_service.synthesize(next_q_text)
        
        # Build response with feedback if available
        response = {
            "text": next_q_text,
            "audio_url": audio_url,
            "is_completed": is_completed and session['status'] != "awaiting_round_2_confirmation"
        }
        
        # Add feedback data if available
        if feedback_data:
            response["feedback"] = feedback_data
        
        return response

    def _generate_question_bank(self, resume, jd, interview_type, topic="realtime", round_num=1, weak_areas=None, project_text=""):
        """
        Asks LLM to generate list of questions based on JD/Resume, interview type, topic, and round.
        """
        if interview_type == "project":
            # === PROJECT BASED INTERVIEW ===
            count = 10
            prompt = f"""
You are generating a PROJECT-BASED INTERVIEW QUESTION BANK.

Project Description: {project_text[:3000]}
Resume Context: {resume[:1000]}

CRITICAL RULES:
1. Generate EXACTLY {count} questions strictly about the USER'S PROJECT.
2. Questions 1-2: High-Level Architecture & Project Overview.
3. Questions 3-6: TECHNICAL DEEP DIVE into the tech stack.
   - Example: "You mentioned using Redis. How exactly are you handling cache invalidation?"
   - Example: "Explain the React component lifecycle in the context of your dashboard."
4. Questions 7-8: System Design, Scalability, and Security.
5. Questions 9-10: Challenges faced, hardest bug, and future improvements.
6. Ensure questions are technically rigorous, not just surface level.
7. Return ONLY a JSON list of strings.
"""

        elif interview_type == "technical":
            if topic != "realtime":
                # === TOPIC-SPECIFIC PRACTICE (PYTHON, JAVA, ETC) ===
                count = 10  # 10 questions per round for practice
                
                if round_num == 1:
                    prompt = f"""
You are generating a PRACTICE QUESTION BANK for {topic.upper()}.
Round: 1 (Basics & Foundations)

Resume Context: {resume[:1000]}

CRITICAL RULES:
1. Generate EXACTLY {count} questions about {topic.upper()} ONLY.
2. Question 1 MUST be a fundamental concept (e.g. "What is a list in {topic}?").
3. DO NOT ask "Tell me about yourself" or general intro questions.
4. Difficulty: EASY → GRADUAL.
5. Focus: Theory, Syntax, Core Concepts.
6. NO coding exercises. NO advanced architecture yet.
7. Return ONLY a JSON list of strings.

Example for Python: ["What is a tuple?", "Difference between list and tuple?", ...]
"""
                else:
                    # Round 2: Adaptive (Harder + Weak Areas)
                    weak_context = f"Candidate struggled with: {', '.join(weak_areas)}" if weak_areas else "Candidate performed well in Round 1."
                    prompt = f"""
You are generating Round 2 PRACTICE QUESTIONS for {topic.upper()}.
Round: 2 (Intermediate & Weak Areas)

Context: {weak_context}

CRITICAL RULES:
1. Generate EXACTLY {count} questions about {topic.upper()} ONLY.
2. FIRST 3-4 questions: Retest concepts related to: {weak_areas if weak_areas else 'Core Foundations'}.
3. REMAINING questions: Increase difficulty to INTERMEDIATE level (e.g., Memory management, advanced features).
4. NO coding exercises.
5. Return ONLY a JSON list of strings.
"""
            else:
                # === REALTIME ADAPTIVE (EXISTING LOGIC) ===
                prompt = f"""
You are generating practice interview questions for students and freshers.

Resume: {resume[:2000]}
Job Description: {jd[:2000]}

CRITICAL RULES:
1. First 2 questions MUST be VERY EASY and confidence-building:
   - Examples: "Tell me about yourself", "What programming languages are you comfortable with?"
   
2. Questions 3-4 should be BASIC THEORY questions.
3. Question 5 can be slightly deeper but still THEORY-BASED.
4. FORBIDDEN: Coding challenges, Algo problems, Tricky questions.
5. Return ONLY a JSON list of 5 strings.
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
                    "Tell me about yourself and your background.",
                    "What programming languages are you comfortable with?",
                    "What is Object-Oriented Programming?",
                    "Can you explain what a function is?",
                    "What projects have you worked on?"
                ]
            elif interview_type == "project":
                return [
                    "Can you give me a high-level overview of your project's architecture?",
                    "What was the most challenging technical problem you faced in this project?",
                    "Why did you choose this specific technology stack? What were the alternatives?",
                    "How are you handling data security and user authentication?",
                    "If you had more time, what improvements would you make to the system?",
                    "Describe a specific bug you encountered and how you debugged it.",
                    "How does your application handle scalability?"
                ]
            else:
                return [
                    "Tell me about a time when you faced a difficult challenge at work.",
                    "How do you handle conflict in a team?",
                    "What are your strengths and weaknesses?",
                    "Where do you see yourself in 5 years?"
                ]

    MAX_HISTORY_TURNS = 6  # Limit context to last 6 turns to check drift

    # --- System Prompts ---
    PROJECT_SYSTEM_PROMPT = """
You are a Project-Based Technical Interviewer.

Your Role:
- You are interviewing a candidate specifically about a project they have built.
- Your goal is to understand their technical choices, challenges faced, and understanding of the system.
- Focus on: Architecture, Database design, API structure, Challenges, Scalability, and Security.

Rules:
1. Ask questions strictly based on the User's Project Description.
2. Start with high-level architecture questions.
3. Drill down into specific technologies mentioned (e.g., "Why did you choose MongoDB over SQL?").
4. Ask about challenges ("What was the hardest bug you fixed?").
5. Be encouraging but inquisitive.

Tone: Professional, curious, engineer-to-engineer.
"""

    HR_SYSTEM_PROMPT = """
You are an experienced HR interviewer conducting a mock interview for practice purposes.

Your role:
- Ask HR and behavioral questions suitable for students and fresh graduates.
- Focus on communication skills, attitude, teamwork, motivation, and self-awareness.
- Keep the difficulty moderate and supportive.
- Do NOT ask trick questions or stress-interview questions.
- Do NOT ask coding or technical questions.
- Encourage the candidate with natural follow-up questions.

Question style:
- Open-ended and reflective
- Based on real-life or academic experiences
- Resume-driven where applicable

Feedback style:
- Polite, encouraging, and constructive
- Focus on clarity, confidence, and structure
- Avoid harsh or judgmental language

Interview goal:
Help the student practice HR interviews and improve confidence.

When providing periodic feedback (every 2-3 answers):
- Be encouraging and supportive
- Highlight what the candidate did well
- Gently suggest areas to explore more
- Use phrases like "Great start", "Consider also", "You might want to explore"
- Avoid: "Wrong", "Incorrect", "Poor", "Fail"
"""

    TECHNICAL_SYSTEM_PROMPT = """
You are a friendly technical interviewer conducting a practice interview for students and freshers.

CRITICAL RULES - FOLLOW STRICTLY:

1. DIFFICULTY PROGRESSION (MANDATORY):
   - ALWAYS start with VERY EASY questions (e.g., "Tell me about yourself", "What programming languages do you know?")
   - First 2-3 questions MUST be confidence-building and simple
   - Increase difficulty ONLY if the student answers well
   - If student struggles, REDUCE difficulty immediately

2. QUESTION TYPES (ALLOWED):
   - Theory and concept explanations (e.g., "What is OOP?", "Explain inheritance")
   - Real-life examples and analogies
   - Simple scenario-based questions
   - Follow-up questions based on student's own answers

3. QUESTION TYPES (STRICTLY FORBIDDEN):
   - Live coding or function writing
   - Algorithm challenges or competitive programming
   - Time/space complexity analysis
   - Tricky or elimination-style questions
   - Mid-level or advanced questions in the first half

4. ADAPTIVE BEHAVIOR:
   - Listen to what the student mentions in their answer
   - Ask follow-up questions using THEIR concepts
   - Example: Student says "OOP has inheritance" → Ask "Can you explain inheritance with a real-life example?"
   - If answer is weak: Rephrase, provide hints, simplify
   - If answer is strong: Gently increase depth (still theory-based)

5. TONE AND APPROACH:
   - Friendly and encouraging
   - Practice-oriented, NOT evaluation
   - Suitable for beginners and freshers
   - Use phrases: "Great!", "Can you elaborate?", "That's a good start"
   - Avoid: "Wrong", "Incorrect", "That's not right"

Interview goal:
Help the student practice technical interviews in a supportive, gradual manner that builds confidence.

When providing periodic feedback (every 2-3 answers):
- Be encouraging and supportive
- Highlight what the candidate explained well
- Gently suggest concepts to explore deeper
- Use phrases like "Good explanation", "Consider also mentioning", "You might want to dive into"
- Avoid: "Wrong", "Incorrect", "Poor", "Fail"
"""

    def _generate_ai_response(self, session):
        """
        Decides what to say next using strict system prompts.
        Now returns structured feedback with scoring for real-time display.
        For project mode: generates questions dynamically based on answers.
        """
        interview_type = session.get("interview_type")
        
        # === SPECIAL PATH FOR PROJECT MODE: FULLY DYNAMIC ===
        if interview_type == "project":
            return self._generate_project_response(session)
        
        # === STANDARD PATH FOR OTHER MODES ===
        # Select System Prompt based on interview type and topic
        topic = session.get("topic", "realtime")
        
        if interview_type == "hr":
            system_prompt = self.HR_SYSTEM_PROMPT
        elif topic != "realtime" and topic in TOPIC_PROMPTS:
            # Use topic-specific prompt for focused practice
            system_prompt = TOPIC_PROMPTS[topic]
        else:
            # Use general technical prompt for realtime mode
            system_prompt = self.TECHNICAL_SYSTEM_PROMPT

        # Construct History
        history_msgs = session["history"][-self.MAX_HISTORY_TURNS:]
        history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history_msgs])
        
        # Get last user answer for scoring
        last_user_answer = ""
        if history_msgs and history_msgs[-1]["role"] == "user":
            last_user_answer = history_msgs[-1]["content"]
        
        # Check if we should provide periodic feedback (every 3 answers)
        should_give_periodic_feedback = session.get("answer_count", 0) % 3 == 0 and session.get("answer_count", 0) > 0
        
        # Next topic from bank (guidance only, LLM should flow naturally)
        idx = session["current_q_index"]
        next_topic = session["q_bank"][idx] if idx < len(session["q_bank"]) else "Conclusion"
        
        # NEW: Request structured feedback with scoring
        prompt = f"""
{system_prompt}

### Conversation History
{history_str}

### Current Context
Next Planned Question/Topic: "{next_topic}" (Use this if the previous topic is exhausted, otherwise follow up).
Candidate's Last Answer: "{last_user_answer}"

### Your Task - CRITICAL: Return JSON Format
You must analyze the candidate's last answer and return a JSON object with the following structure:

{{
    "score": <number 0-100>,
    "quality": "<excellent|good|needs_work|poor>",
    "feedback_text": "<brief constructive feedback, 1-2 sentences>",
    "next_question": "<the next question to ask>"
}}

### Scoring Guidelines:
- 90-100: Excellent - Comprehensive, accurate, well-explained with examples
- 75-89: Good - Solid understanding, mostly accurate, could be more detailed
- 60-74: Needs Work - Basic understanding but missing key points or clarity
- 0-59: Poor - Incorrect, very brief, or shows lack of understanding

### Quality Mapping:
- excellent: 90-100
- good: 75-89
- needs_work: 60-74
- poor: 0-59

### Feedback Guidelines:
1. Be encouraging and constructive
2. Highlight what they did well (if applicable)
3. Gently point out what could be improved
4. Keep it brief (1-2 sentences max)
5. Use supportive language

### Periodic Feedback Mode
{"PROVIDE MORE DETAILED FEEDBACK NOW - Include overall progress comment" if should_give_periodic_feedback else "Keep feedback brief and focused on this answer"}

### Instructions for Next Question:
1. ANALYZE the candidate's last response
2. IF the candidate answered the 'Next Planned Question' already:
   - SKIP asking it directly
   - Ask a DEEPER follow-up or move to next topic
3. IF the candidate mentioned a specific technology/concept:
   - Acknowledge it explicitly
   - Bridge it to the next question naturally
4. TRANSITION smoothly - feel like a conversation, not a checklist
5. SPEAK DIRECTLY to the candidate. Be natural.

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no extra text.
"""
        
        try:
            res = self.llm.generate_response(prompt)
            if not res:
                raise ValueError("Empty response from LLM")
            
            # Parse JSON response
            parsed = self._parse_json_response(res)
            
            # Validate and set defaults if needed
            if "score" not in parsed or not isinstance(parsed.get("score"), (int, float)):
                parsed["score"] = 50  # Default neutral score
            
            if "quality" not in parsed:
                score = parsed["score"]
                if score >= 90:
                    parsed["quality"] = "excellent"
                elif score >= 75:
                    parsed["quality"] = "good"
                elif score >= 60:
                    parsed["quality"] = "needs_work"
                else:
                    parsed["quality"] = "poor"
            
            if "feedback_text" not in parsed:
                parsed["feedback_text"] = "Thank you for your answer."
            
            if "next_question" not in parsed:
                parsed["next_question"] = f"Let's move on to: {next_topic}"
            
            # Store score in session for analytics
            if "scores" not in session:
                session["scores"] = []
            session["scores"].append(parsed["score"])
            
            # Store the full feedback in session for retrieval
            session["last_feedback"] = {
                "score": parsed["score"],
                "quality": parsed["quality"],
                "feedback_text": parsed["feedback_text"]
            }
            
            # Return the full parsed object
            return parsed
            
        except Exception as e:
            print(f"[SimVoice ERROR] Generate AI Response failed: {e}")
            # Fallback response
            return {
                "score": 50,
                "quality": "needs_work",
                "feedback_text": "Thank you for your answer.",
                "next_question": f"Let's move on to: {next_topic}"
            }
    
    def _generate_project_response(self, session):
        """
        Dynamic question generation for project-based interviews.
        Each question is generated based on the conversation so far.
        """
        project_text = session.get("project_text", "")
        
        # For project mode, use FULL history to prevent repetition
        history_msgs = session["history"]  # All history, not limited
        history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history_msgs])
        
        # Get the last user answer
        last_user_msg = history_msgs[-1]["content"] if history_msgs and history_msgs[-1]["role"] == "user" else ""
        
        # Extract all questions already asked to prevent repetition
        questions_asked = [msg["content"] for msg in history_msgs if msg["role"] == "assistant"]
        questions_asked_str = "\n".join([f"- {q.split('?')[0]}?" for q in questions_asked if "?" in q])
        
        # Determine question count for completion check
        idx = session["current_q_index"]
        total_questions = len(session["q_bank"])
        
        prompt = f"""
{self.PROJECT_SYSTEM_PROMPT}

### Project Context
Project Description: {project_text[:2000]}

### Interview Progress
Current Question Number: {idx + 1} of {total_questions}

### Questions Already Asked
{questions_asked_str if questions_asked_str else "None yet"}

### Conversation History
{history_str}

### Your Task
You are conducting a DYNAMIC project interview. Each question should be based on the student's previous answers.

CRITICAL INSTRUCTIONS:
1. ANALYZE the student's last answer: "{last_user_msg}"
   - What specific technologies did they mention?
   - What challenges or design decisions did they reveal?
   - What depth of understanding did they demonstrate?

2. DO NOT REPEAT any question you already asked (see "Questions Already Asked" above).

3. GENERATE THE NEXT QUESTION based on this analysis:
   - IF they mentioned a specific technology (e.g., "Redis", "React"), ask them to explain HOW they used it in this project.
   - IF they described a challenge, ask them to dive deeper into their solution.
   - IF their answer was high-level, ask for implementation details.
   - IF their answer was detailed, probe for edge cases or alternatives.

4. EXAMPLES of good adaptive questions:
   - Student: "I used Node.js for the backend"
     → You: "Interesting! How did you structure your Node.js application? Did you use any framework like Express?"
   
   - Student: "We faced scalability issues with the database"
     → You: "That's a common challenge. What specific bottleneck did you identify, and how did you address it?"

5. Keep questions focused on THEIR project, not generic theory.

6. Be conversational and natural. Acknowledge their answer before asking the next question.

7. If you've covered most aspects of the project, explore edge cases, testing strategies, or future improvements.

Generate your response now:
"""
        
        try:
            res = self.llm.generate_response(prompt)
            if not res:
                raise ValueError("Empty response from LLM")
            return res.strip()
        except Exception as e:
            print(f"[SimVoice ERROR] Generate Project Response failed: {e}")
            # Fallback to a generic follow-up
            return f"Thank you for that explanation. Can you tell me more about the technical challenges you faced in this project?"

    def _generate_final_summary(self, session):
        """
        Generates a friendly, encouraging summary when the interview ends.
        """
        # Select System Prompt based on topic
        topic = session.get("topic", "realtime")
        
        if session.get("interview_type") == "hr":
            system_prompt = self.HR_SYSTEM_PROMPT
        elif topic != "realtime" and topic in TOPIC_PROMPTS:
            system_prompt = TOPIC_PROMPTS[topic]
        else:
            system_prompt = self.TECHNICAL_SYSTEM_PROMPT

        # Construct History
        history_msgs = session["history"][-self.MAX_HISTORY_TURNS:]
        history_str = "\n".join([f"{m['role'].upper()}: {m['content']}" for m in history_msgs])
        
        prompt = f"""
{system_prompt}

### Conversation History
{history_str}

### Your Task: Generate Practice Summary
The interview practice session is now complete. Provide a warm, encouraging summary:

1. Thank them for practicing
2. Highlight 2-3 specific strengths you observed (communication, clarity, concepts explained well)
3. Gently suggest 1-2 areas they might want to explore more (use encouraging language)
4. End with motivation to keep practicing

Guidelines:
- Be warm and supportive
- Use phrases like "Great job", "Well done", "Consider exploring", "Keep practicing"
- Avoid scores, grades, or pass/fail language
- Keep it conversational and friendly
- Maximum 4-5 sentences
"""
        
        try:
            res = self.llm.generate_response(prompt)
            if not res:
                return "Thank you for practicing with me today! You did a great job engaging with the questions. Keep practicing and you'll continue to improve. Best of luck!"
            return res.strip()
        except Exception as e:
            print(f"[SimVoice ERROR] Generate Summary failed: {e}")
            return "Thank you for practicing with me today! You did a great job engaging with the questions. Keep practicing and you'll continue to improve. Best of luck!"

    def _add_history(self, session_id, role, content):
        self.sessions[session_id]["history"].append({"role": role, "content": content})
