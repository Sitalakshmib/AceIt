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
            "weak_areas": [], # Track weak concepts
            "start_time": datetime.now(),  # Track start time for duration-based completion
            "scores": [],  # Track scores for each answer
            "qa_pairs": []  # Track question-answer pairs with scores
        }
        self.sessions[session_id] = session
        
        # 3. First Question (Intro or Direct Technical Start)
        topic = session.get("topic", "realtime")
        
        if interview_type == "project":
            # Project-based mode: Start with project discussion
            initial_text = f"Hello! I've reviewed your project description. It sounds interesting. Let's discuss the architecture and your implementation choices. {q_bank[0] if q_bank else 'Can you give me a high-level overview?'}"
            session["current_q_index"] = 1  # Logic fix: Q1 asked
        elif topic != "realtime" and interview_type == "technical":
            # Topic-specific mode: Start directly with basic concept question (no intro)
            # CRITICAL: First question must be fundamental, not from question bank
            topic_questions = {
                "python": "Hello! Let's practice Python concepts. To start, can you explain what Python data types are?",
                "java": "Hello! Let's practice Java concepts. To start, can you explain what Object-Oriented Programming is in Java?",
                "sql": "Hello! Let's practice SQL concepts. To start, can you explain what SQL is and what it's used for?",
                "dotnet": "Hello! Let's practice .NET Core concepts. To start, can you explain what .NET Core is?",
                "qa": "Hello! Let's practice QA/Testing concepts. To start, can you explain what software testing is?",
                "php": "Hello! Let's practice PHP concepts. To start, can you explain what PHP is used for?"
            }
            initial_text = topic_questions.get(topic, f"Hello! Let's practice {topic.upper()} concepts. {q_bank[0] if q_bank else 'What do you know about this topic?'}")
            session["current_q_index"] = 1  # First question asked
        else:
            # Realtime or HR mode: Use adaptive intro
            if interview_type == "technical" and topic == "realtime":
                # Real-Time Adaptive: Clean intro without mentioning question count
                initial_text = "Hello! I am your AI Interviewer for this Technical interview. This will be an adaptive conversation based on your background and experience. Let's begin. Please introduce yourself and tell me about your technical background."
            else:
                # HR mode
                interview_label = "HR/Behavioral"
                initial_text = f"Hello! I am your AI Interviewer for this {interview_label} interview. I have prepared {len(q_bank)} questions. Let's begin. Please introduce yourself."
        
        print(f"[SimVoice] Starting {interview_type} interview (Topic: {topic})")
        
        # Record AI turn
        self._add_history(session_id, "assistant", initial_text)
        
        # Generate TTS audio for initial greeting
        # PRIVACY POLICY: AI audio is generated on-demand via TTS and NOT stored.
        # Audio URLs are temporary and audio is played in-memory on the client.
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
        # PRIVACY POLICY: Audio is processed in-memory only and NOT persisted.
        # Temporary audio files are deleted immediately after transcription.
        user_text = text_answer or ""
        if audio_file_path:
            print(f"[SimVoice] Transcribing answer for {session_id}...")
            user_text = voice_service.transcribe(audio_file_path)
            # Note: Temporary file is deleted by the route handler after this method returns
            
        # Detect weak answer (simple heuristic for now)
        if len(user_text.split()) < 5 or "don't know" in user_text.lower() or "unsure" in user_text.lower():
            current_topic = session["q_bank"][session["current_q_index"]-1] if session["current_q_index"] > 0 else "General"
            session["weak_areas"].append(current_topic)
        
        print(f"[SimVoice] User Said: {user_text}")
        self._add_history(session_id, "user", user_text)
        
        # 2. Increment answer count
        session["answer_count"] += 1
        
        # 3. Check if interview should complete
        # CRITICAL: 20-minute timer applies to ALL technical interview topics
        topic = session.get("topic", "realtime")
        interview_type = session.get("interview_type", "technical")
        
        # Calculate elapsed time
        from datetime import datetime
        start_time = session.get("start_time")
        if not start_time:
            # Initialize start time if not set
            session["start_time"] = datetime.now()
            elapsed_minutes = 0
        else:
            elapsed_minutes = (datetime.now() - start_time).total_seconds() / 60
        
        print(f"[SimVoice] Session: {session_id} | Elapsed: {elapsed_minutes:.2f} min | Status: {session.get('status')} | Type: {interview_type} | Topic: {topic}")
        
        # Determine if we should complete
        is_completing = False
        is_completed = False
        
        # TIMER LOGIC: 10-minute limit for ALL technical interviews
        if interview_type == "technical":
            if elapsed_minutes >= 10:  # Changed from 20 to 10 minutes
                # If already in completing state, this is the final answer
                if session.get("status") == "completing":
                    is_completed = True
                else:
                    # Mark as completing - accept one more answer, then end gracefully
                    is_completing = True
                    session["status"] = "completing"
            # Also check question count for topic-based modes as a backup
            elif topic != "realtime":
                # For topic-based: also complete if all questions are answered
                if session["current_q_index"] >= len(session["q_bank"]):
                    is_completed = True
        elif interview_type == "hr":
            # HR interviews: question count based completion only
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
                
                # Store score in scores array for overall calculation
                session["scores"].append(feedback_data["score"])
                
                # Store question-answer pair with score for results generation
                # Get the previous question (the one the user just answered)
                if len(session["history"]) >= 2:
                    prev_question = session["history"][-2].get("content", "") if session["history"][-2]["role"] == "assistant" else ""
                    user_answer = session["history"][-1].get("content", "") if session["history"][-1]["role"] == "user" else ""
                    
                    session["qa_pairs"].append({
                        "question": prev_question,
                        "answer": user_answer,
                        "score": feedback_data["score"]
                    })
            else:
                # Backward compatibility - if string is returned
                next_q_text = ai_response
        
        # 5. Update History & Audio
        self._add_history(session_id, "assistant", next_q_text)
        # NOTE: current_q_index is now incremented conditionally in _generate_ai_response
        # based on answer quality (for topic-based modes) or always (for realtime mode)
        
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

    def _generate_question_bank(self, resume, jd, interview_type, topic="realtime", round_num=1, weak_areas=None, project_text="", user_id=None):
        """
        Asks LLM to generate list of questions based on JD/Resume, interview type, topic, and round.
        CRITICAL: Questions are generated dynamically, NOT hardcoded.
        Duration: ~20 minutes = 10-12 questions at ~2 minutes per question
        """
        # Calculate question count for ~10 minute session
        # Typical timing: 1 minute per question (30s question + 30s answer)
        target_question_count = 10  # Enough for ~10 minutes
        
        if interview_type == "project":
            # === PROJECT BASED INTERVIEW ===
            prompt = f"""
You are generating a PROJECT-BASED INTERVIEW QUESTION BANK.

Project Description: {project_text[:3000]}
Resume Context: {resume[:1000]}

CRITICAL RULES:
1. Generate EXACTLY {target_question_count} questions strictly about the USER'S PROJECT.
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
            if topic == "realtime":
                # === REALTIME ADAPTIVE (NO PREDEFINED QUESTIONS) ===
                # For realtime mode, we generate a minimal guidance list
                # The actual questions will be generated dynamically based on answers
                prompt = f"""
You are generating GUIDANCE TOPICS for a REAL-TIME ADAPTIVE technical interview.

Resume: {resume[:2000]}
Job Description: {jd[:2000]}

CRITICAL RULES:
1. This is NOT a question bank. These are TOPIC AREAS to explore.
2. Generate {target_question_count} topic areas based on the candidate's resume.
3. First topic MUST be: "Introduction and Background"
4. Remaining topics should be technical areas mentioned in their resume or JD.
5. These will guide the conversation, but actual questions will be generated dynamically.
6. Return ONLY a JSON list of topic strings.

Example: ["Introduction and Background", "Python Experience", "Database Design", "API Development", ...]
"""
            
            elif topic in ["python", "java", "sql", "dotnet", "qa", "php"]:
                # === TOPIC-SPECIFIC PRACTICE ===
                # Generate TOPIC AREAS (not specific questions) for coverage guidance
                topic_name = topic.upper() if topic != "dotnet" else ".NET Core"
                
                if round_num == 1:
                    prompt = f"""
You are creating a TOPIC COVERAGE GUIDE for {topic_name} practice interview.
Round: 1 (Basics & Foundations)

CRITICAL RULES:
1. Generate EXACTLY {target_question_count} TOPIC AREAS (not questions) about {topic_name}.
2. These are CONCEPTS to cover, not specific questions.
3. Start with FUNDAMENTAL concepts, progress to intermediate.
4. Focus: Theory, Core Concepts, Practical Understanding.
5. NO advanced topics in Round 1.
6. Return ONLY a JSON list of topic area strings.

Example for Python: ["Data Types & Variables", "Lists & Tuples", "Dictionaries", "Functions Basics", "String Operations", "Conditional Statements", "Loops", "List Comprehensions", "Exception Handling", "File Handling"]

Example for Java: ["Java Basics & JVM", "Data Types", "OOP Concepts", "Classes & Objects", "Inheritance", "Polymorphism", "Interfaces", "Exception Handling", "Collections Framework", "String Handling"]

Example for SQL: ["SQL Basics", "SELECT Statement", "WHERE Clause", "Data Types", "Primary Keys", "Foreign Keys", "INNER JOIN", "LEFT JOIN", "Aggregate Functions", "GROUP BY"]

Example for .NET: [".NET Core Basics", "CLR & Framework", "C# Fundamentals", "OOP in C#", "ASP.NET Core", "Dependency Injection", "Entity Framework", "MVC Pattern", "Web API", "Middleware"]

Generate for {topic_name}:
"""
                else:
                    # Round 2: Adaptive (Harder + Weak Areas)
                    weak_context = f"Candidate struggled with: {', '.join(weak_areas)}" if weak_areas else "Candidate performed well in Round 1."
                    prompt = f"""
You are creating Round 2 TOPIC COVERAGE GUIDE for {topic_name}.
Round: 2 (Intermediate & Weak Areas)

Context: {weak_context}

CRITICAL RULES:
1. Generate EXACTLY {target_question_count} TOPIC AREAS about {topic_name}.
2. FIRST 3-4 topics: Related to weak areas: {weak_areas if weak_areas else 'Core Foundations'}.
3. REMAINING topics: Intermediate level concepts.
4. Return ONLY a JSON list of topic area strings.
"""
            else:
                # Unsupported topic - fallback
                prompt = f"""
Generate {target_question_count} basic technical interview questions suitable for beginners.
Focus on fundamental programming concepts, data structures, and problem-solving.
Return ONLY a JSON list of strings.
"""

        else:  # HR/Behavioral
            prompt = f"""
You are an expert HR Interviewer creating a STRICTLY BEHAVIORAL interview question bank.

Resume: {resume[:2000]}
Job Description: {jd[:2000]}

🚨 CRITICAL RULES - FOLLOW ABSOLUTELY:

1. **NEVER INCLUDE TECHNICAL QUESTIONS**
   - Do NOT ask about algorithms, code, technical concepts, or technologies
   - Do NOT test technical knowledge
   - Even if resume mentions "Python", "AI", "Java", etc., DO NOT ask technical questions about them

2. **USE TECHNICAL BACKGROUND ONLY AS CONTEXT FOR BEHAVIORAL QUESTIONS**
   - If resume says "AI student":
     ✅ CORRECT: "Tell me about a time when you faced a challenging problem while learning AI. How did you approach it?"
     ❌ WRONG: "What is machine learning?" or "Explain neural networks"
   
   - If resume says "Python developer":
     ✅ CORRECT: "Describe a situation where you had to learn a new skill quickly. How did you manage it?"
     ❌ WRONG: "What are Python decorators?" or "Explain OOP in Python"

3. **BEHAVIORAL QUESTION CATEGORIES (ONLY THESE)**
   Generate {target_question_count} questions covering these areas:
   - Communication skills & clarity
   - Teamwork & collaboration
   - Conflict management & resolution
   - Leadership & taking initiative
   - Stress handling & pressure management
   - Time management & prioritization
   - Adaptability & learning from failure
   - Motivation, goals & career aspirations
   - Strengths & weaknesses (self-awareness)
   - Ethical situations & decision-making
   - Receiving & acting on feedback

4. **QUESTION FORMAT**
   - Use STAR method questions (Situation, Task, Action, Result)
   - Focus on experiences, challenges, decisions, and reflections
   - Use phrases: "Tell me about a time when...", "Describe a situation where...", "How do you handle..."

5. **RETURN FORMAT**
   - Return ONLY a JSON list of strings
   - Each string is a complete behavioral question
   - Example: ["Question 1", "Question 2", ...]

EXAMPLES OF CORRECT BEHAVIORAL QUESTIONS:
- "Tell me about a time when you faced a difficult challenge. How did you handle it?"
- "Describe a situation where you had to work with a difficult team member. What did you do?"
- "How do you manage stress when dealing with multiple deadlines?"
- "Tell me about a time when you failed at something. What did you learn?"
- "Describe a situation where you had to adapt to a significant change. How did you handle it?"
- "What motivates you in your studies/career?"
- "Tell me about a time when you showed leadership, even if you weren't in a leadership role."
- "Describe a conflict you had with a peer. How did you resolve it?"

🔒 FINAL CHECK: Before returning, verify that ZERO questions ask for technical explanations or test technical knowledge.
"""
        
        try:
            res = self.llm.generate_response(prompt)
            clean = res.replace("```json", "").replace("```", "").strip()
            questions = json.loads(clean)
            
            # Validate we got a list
            if not isinstance(questions, list):
                raise ValueError("LLM did not return a list")
            
            # Ensure we have at least some questions
            if len(questions) < 5:
                raise ValueError(f"Too few questions generated: {len(questions)}")
            
            return questions
            
        except Exception as e:
            print(f"[ERROR] Question generation failed: {e}")
            # Fallback questions based on type
            if interview_type == "technical":
                if topic == "realtime":
                    return [
                        "Introduction and Background",
                        "Programming Languages",
                        "Object-Oriented Programming",
                        "Data Structures",
                        "Database Concepts",
                        "Web Development",
                        "Problem Solving",
                        "Projects",
                        "Challenges Faced",
                        "Future Goals"
                    ]
                elif topic == "python":
                    return [
                        "What is Python?",
                        "What are Python data types?",
                        "Explain lists in Python",
                        "What is the difference between list and tuple?",
                        "What are dictionaries?",
                        "Explain functions in Python",
                        "What is a class in Python?",
                        "What is inheritance?",
                        "Explain exception handling",
                        "What are Python modules?"
                    ]
                elif topic == "java":
                    return [
                        "What is Java?",
                        "What is the JVM?",
                        "What are Java data types?",
                        "What is OOP in Java?",
                        "Explain classes and objects",
                        "What is inheritance in Java?",
                        "What are interfaces?",
                        "Explain exception handling",
                        "What are collections?",
                        "What is multithreading?"
                    ]
                elif topic == "sql":
                    return [
                        "What is SQL?",
                        "What is a database?",
                        "What is a primary key?",
                        "What is a foreign key?",
                        "Explain SELECT statement",
                        "What are SQL joins?",
                        "What is normalization?",
                        "Explain constraints",
                        "What are indexes?",
                        "What is a transaction?"
                    ]
                elif topic == "dotnet":
                    return [
                        "What is .NET Core?",
                        "Difference between .NET Framework and .NET Core?",
                        "What is the CLR?",
                        "What are namespaces?",
                        "Explain classes in C#",
                        "What is dependency injection?",
                        "What is ASP.NET Core?",
                        "Explain MVC pattern",
                        "What are middleware?",
                        "What is Entity Framework?"
                    ]
                else:
                    return [
                        "Tell me about yourself and your background.",
                        "What programming languages are you comfortable with?",
                        "What is Object-Oriented Programming?",
                        "Can you explain what a function is?",
                        "What projects have you worked on?",
                        "What is a database?",
                        "Explain your problem-solving approach",
                        "What challenges have you faced?",
                        "What are your strengths?",
                        "What are your career goals?"
                    ]
            elif interview_type == "project":
                return [
                    "Can you give me a high-level overview of your project's architecture?",
                    "What was the most challenging technical problem you faced in this project?",
                    "Why did you choose this specific technology stack?",
                    "How are you handling data security and user authentication?",
                    "If you had more time, what improvements would you make?",
                    "Describe a specific bug you encountered and how you debugged it.",
                    "How does your application handle scalability?",
                    "What testing strategies did you implement?",
                    "How did you handle error handling?",
                    "What did you learn from this project?"
                ]
            else:  # HR
                return [
                    "Tell me about yourself and what drives you.",
                    "Describe a time when you faced a significant challenge. How did you overcome it?",
                    "How do you handle conflict or disagreement in a team setting?",
                    "Tell me about your strengths and areas where you'd like to improve.",
                    "Describe a situation where you had to show leadership or take initiative.",
                    "What motivates you to do your best work?",
                    "How do you manage stress and pressure, especially during busy periods?",
                    "Tell me about a time when you failed or made a mistake. What did you learn?",
                    "Where do you see yourself in 5 years, and what are your career goals?",
                    "Describe a situation where you had to adapt to a major change. How did you handle it?"
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
You are a professional HR interviewer conducting a STRICTLY BEHAVIORAL practice interview.

🚨 CRITICAL RULES - FOLLOW ABSOLUTELY:

1. **NEVER ASK TECHNICAL QUESTIONS**
   - Do NOT ask about algorithms, code, technical concepts, or technologies
   - Do NOT test technical knowledge in any form
   - Do NOT ask "What is [technical term]?" or "Explain [technical concept]"
   - Even if the candidate mentions technical skills, DO NOT quiz them on it

2. **USE TECHNICAL BACKGROUND ONLY AS CONTEXT**
   - If candidate says "I'm an AI student" or "I work with Python":
     ✅ CORRECT: "What challenges did you face while learning AI, and how did you overcome them?"
     ✅ CORRECT: "Tell me about a time when you struggled with a complex subject. How did you handle it?"
     ❌ WRONG: "What is machine learning?" or "Explain neural networks"
     ❌ WRONG: "What algorithms did you study?" or "Explain overfitting"

3. **BEHAVIORAL QUESTION CATEGORIES (ONLY THESE)**
   - Communication skills & clarity
   - Teamwork & collaboration
   - Conflict management & resolution
   - Leadership & taking initiative
   - Stress handling & pressure management
   - Time management & prioritization
   - Adaptability & learning from failure
   - Motivation, goals & career aspirations
   - Strengths & weaknesses (self-awareness)
   - Ethical situations & decision-making
   - Receiving & acting on feedback

4. **QUESTION FORMAT**
   - Use STAR method questions (Situation, Task, Action, Result)
   - Ask about experiences, challenges, decisions, and reflections
   - Focus on "Tell me about a time when..." or "Describe a situation where..."
   - All questions must be experience-based or scenario-based

5. **ADAPTIVE CONVERSATION FLOW**
   - After each answer, analyze the BEHAVIORAL QUALITY:
     * Clarity of communication
     * Depth of reflection
     * Confidence in delivery
     * Structure of response (STAR format)
   - If answer is STRONG: Move to a different behavioral dimension
   - If answer is WEAK/VAGUE: Ask probing follow-up questions to help them reflect deeper
   - Guide them gently (this is practice mode, not evaluation)

6. **TONE & STYLE**
   - Sound human, empathetic, and encouraging
   - Be supportive and non-judgmental
   - Never "teach" technical content
   - Never quiz or test the student
   - This is a practice HR interview to build confidence

7. **SCORING CRITERIA (BEHAVIORAL ONLY)**
   - 90-100: Excellent - Clear, structured, reflective, confident delivery
   - 75-89: Good - Solid answer with some depth, could be more detailed
   - 60-74: Needs Work - Basic answer but lacks depth or structure
   - 0-59: Poor - Very vague, unclear, or too brief

Interview Goal:
Help the student practice HR behavioral interviews and improve communication, confidence, and self-reflection.

When providing periodic feedback (every 2-3 answers):
- Be encouraging and supportive
- Highlight what the candidate communicated well
- Gently suggest how to add more depth or structure
- Use phrases like "Great reflection", "Consider also sharing", "You might want to elaborate on"
- Avoid: "Wrong", "Incorrect", "Poor", "Fail"

🔒 FINAL RULE: If a question tests technical knowledge OR asks for technical explanations, DO NOT ask it. This overrides everything else.
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


    def _parse_json_response(self, response_text):
        """
        Parse JSON response from LLM, handling common formatting issues.
        """
        try:
            # Remove markdown code blocks if present
            clean = response_text.strip()
            if clean.startswith("```json"):
                clean = clean[7:]  # Remove ```json
            if clean.startswith("```"):
                clean = clean[3:]  # Remove ```
            if clean.endswith("```"):
                clean = clean[:-3]  # Remove trailing ```
            
            clean = clean.strip()
            
            # Parse JSON
            parsed = json.loads(clean)
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"[SimVoice] JSON Parse Error: {e}")
            print(f"[SimVoice] Raw response: {response_text[:500]}")
            raise ValueError(f"Failed to parse JSON response: {e}")
    
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
        elif topic in TOPIC_PROMPTS:
            # Use topic-specific prompt (includes realtime, python, java, sql, dotnet, etc.)
            system_prompt = TOPIC_PROMPTS[topic]
        else:
            # Fallback to general technical prompt
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
        
        # === HR BEHAVIORAL INTERVIEW: STRICTLY BEHAVIORAL LOGIC ===
        if interview_type == "hr":
            # HR interviews use question bank as guidance, but adapt based on behavioral quality
            idx = session["current_q_index"]
            q_bank = session["q_bank"]
            
            # Get current and remaining questions
            current_question_area = q_bank[min(idx, len(q_bank)-1)] if q_bank else "General behavioral questions"
            remaining_questions = q_bank[idx:idx+3] if idx < len(q_bank) else ["Closing questions"]
            
            prompt = f"""
{system_prompt}

### Conversation History
{history_str}

### Current Context
Interview Progress: Question {session.get('answer_count', 0) + 1} of approximately {len(q_bank)}
Current Question Area: "{current_question_area}"
Remaining Question Areas: {remaining_questions}
Candidate's Last Answer: "{last_user_answer}"

### Your Task - CRITICAL: Return JSON Format
You must analyze the candidate's last answer and return a JSON object with the following structure:

{{
    "score": <number 0-100>,
    "quality": "<excellent|good|needs_work|poor>",
    "feedback_text": "<brief constructive feedback, 1-2 sentences>",
    "next_question": "<the next behavioral question to ask>"
}}

### BEHAVIORAL SCORING GUIDELINES (NOT TECHNICAL):
- 90-100: Excellent - Clear, structured (STAR format), reflective, confident, detailed
- 75-89: Good - Solid answer with depth, good communication, could add more detail
- 60-74: Needs Work - Basic answer but lacks depth, structure, or reflection
- 0-59: Poor - Very vague, unclear, too brief, or lacks self-awareness

### Quality Mapping:
- excellent: 90-100
- good: 75-89
- needs_work: 60-74
- poor: 0-59

### Feedback Guidelines:
1. Be encouraging and supportive
2. Highlight what they communicated well
3. Gently suggest how to add more depth or structure
4. Keep it brief (1-2 sentences max)
5. Use supportive, non-judgmental language

### Periodic Feedback Mode
{"PROVIDE MORE DETAILED FEEDBACK NOW - Include overall behavioral progress comment" if should_give_periodic_feedback else "Keep feedback brief and focused on this answer"}

### CRITICAL INSTRUCTIONS FOR HR BEHAVIORAL INTERVIEW:
1. ANALYZE the candidate's last answer for BEHAVIORAL QUALITY:
   - Did they use STAR format (Situation, Task, Action, Result)?
   - Was their communication clear and structured?
   - Did they show self-reflection and learning?
   - Was the answer detailed enough?

2. GENERATE the next question based on BEHAVIORAL DEPTH:
   - If answer was STRONG (score >= 75): Move to a different behavioral dimension
   - If answer was WEAK/VAGUE (score < 75): Ask probing follow-up to help them reflect deeper
   
3. USE TECHNICAL BACKGROUND ONLY AS CONTEXT:
   - If they mentioned "AI", "Python", "Java", etc., use it for behavioral context
   - Example: "You mentioned working with AI. Tell me about a time when you faced a setback in that area. How did you handle it?"
   - DO NOT ask: "What is machine learning?" or "Explain neural networks"

4. BEHAVIORAL QUESTION CATEGORIES TO EXPLORE:
   - Communication & clarity
   - Teamwork & collaboration
   - Conflict management
   - Leadership & initiative
   - Stress & pressure handling
   - Time management
   - Adaptability & learning from failure
   - Motivation & goals
   - Self-awareness (strengths/weaknesses)
   - Ethics & decision-making
   - Feedback handling

5. QUESTION FORMAT:
   - Use "Tell me about a time when..." or "Describe a situation where..."
   - Focus on experiences, challenges, decisions, reflections
   - NEVER ask for technical explanations

6. ADAPTIVE FLOW:
   - Build naturally from their previous responses
   - If they mentioned a challenge, explore how they handled it
   - If they mentioned teamwork, ask about conflict or collaboration
   - Make it feel conversational, not a checklist

🚨 FINAL CHECK: Ensure your next_question is BEHAVIORAL and does NOT test technical knowledge.

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no extra text.
"""
        
        # CRITICAL FIX: For Real-Time Adaptive mode, do NOT use question bank
        # For topic-based modes, use question bank as guidance
        elif topic == "realtime":
            # Real-Time Adaptive: NO pre-planned topics, fully dynamic
            prompt = f"""
{system_prompt}

### Conversation History
{history_str}

### Current Context
Interview Progress: Question {session.get('answer_count', 0) + 1} of approximately 10
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

### CRITICAL INSTRUCTIONS FOR REAL-TIME ADAPTIVE MODE:
1. ANALYZE the candidate's last answer carefully
2. EXTRACT specific technologies, concepts, or experiences they mentioned
3. GENERATE the next question based ONLY on what they said:
   - If they mentioned a technology (e.g., "Python", "React"), ask them to explain their experience with it
   - If they described a project, ask about technical choices, challenges, or architecture
   - If they mentioned a concept, ask them to explain it deeper or give examples
   - If they struggled, ask a simpler related question
   - If they excelled, dive deeper into that specific area
4. DO NOT follow any pre-planned sequence
5. DO NOT ask generic questions unrelated to their answers
6. BUILD each question naturally from their previous response
7. Make it feel like a real conversation, not a checklist

### TRANSCRIPTION ERROR HANDLING (CRITICAL):
- Audio transcription may sometimes mishear technical terms
- Example: "autoencoder" might be transcribed as "hordeu encoder" or similar
- If you encounter an UNCLEAR or NON-EXISTENT technical term:
  * DO NOT ignore it
  * DO NOT assume you know what they meant
  * POLITELY ask for clarification
  * Example: "I heard you mention 'hordeu encoder' - could you clarify what you meant? Did you mean 'autoencoder' or something else?"
- This helps correct transcription errors and ensures accurate conversation

Example Flow:
- Student: "I work with Python and Django"
- You: "Great! Can you tell me about a specific Django project you've worked on?"
- Student: "I built a REST API for user authentication"
- You: "Interesting! How did you handle JWT token management in your API?"

CRITICAL: Return ONLY valid JSON. No markdown, no code blocks, no extra text.
"""
        else:
            # Topic-Based Practice: Use topic areas as COVERAGE GUIDE, not fixed sequence
            # CRITICAL: LLM decides actual questions based on student's answer quality
            idx = session["current_q_index"]
            topic_areas = session["q_bank"]  # These are topic areas, not questions
            
            # Determine which topic area we're currently exploring
            current_topic_area = topic_areas[min(idx, len(topic_areas)-1)] if topic_areas else "General Concepts"
            remaining_topics = topic_areas[idx:] if idx < len(topic_areas) else []
            
            prompt = f"""
{system_prompt}

### Conversation History
{history_str}

### Current Context
Current Topic Area: "{current_topic_area}"
Remaining Topic Areas to Cover: {remaining_topics[:3] if remaining_topics else ["Interview nearing completion"]}
Interview Progress: Question {session.get('answer_count', 0) + 1} of approximately 10
Candidate's Last Answer: "{last_user_answer}"

### Your Task - CRITICAL: Return JSON Format
You must analyze the candidate's last answer and return a JSON object with the following structure:

{{
    "score": <number 0-100>,
    "quality": "<excellent|good|needs_work|poor>",
    "feedback_text": "<brief constructive feedback, 1-2 sentences>",
    "answer_analysis": "<what student understood well / what they missed>",
    "next_action": "<move_forward|clarify_same_concept|teach_basics>",
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

### CRITICAL ADAPTIVE TEACHING LOGIC:

**ANALYZE the student's last answer quality:**

1. **If answer is WEAK or INCORRECT (score < 60):**
   - next_action: "teach_basics"
   - DO NOT move to a new topic
   - Stay on the SAME concept
   - Ask a SIMPLER sub-question to build understanding
   - Provide hints or break down the concept
   - Example: "Let me ask it differently - can you explain what [simpler aspect] means?"
   - GOAL: Help them understand the current concept before moving on

2. **If answer is PARTIAL (score 60-74):**
   - next_action: "clarify_same_concept"
   - Stay on the SAME concept
   - Ask a clarifying follow-up question
   - Help them complete their understanding
   - Example: "You mentioned [X], can you also explain [Y] which is related?"
   - GOAL: Deepen understanding of current concept

3. **If answer is GOOD or EXCELLENT (score >= 75):**
   - next_action: "move_forward"
   - Acknowledge their understanding
   - Move to a NEW concept from the remaining topic areas
   - Gradually increase depth
   - Example: "Great explanation! Now let's discuss [next topic area]..."
   - GOAL: Progress through the curriculum

### Topic Area Coverage:
- Use "Current Topic Area" and "Remaining Topic Areas" as GUIDES
- These are NOT specific questions - generate questions dynamically
- Ensure you cover different concepts, not just one
- If student struggles with a topic, spend more time on it
- If student excels, move through topics faster

### TRANSCRIPTION ERROR HANDLING:
- Audio transcription may mishear technical terms
- If you encounter unclear/non-existent terms, politely ask for clarification
- Example: "I heard you mention '[unclear term]' - could you clarify what you meant?"

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
                # For realtime mode, generate a generic follow-up
                # For topic-based modes, use the next_topic from question bank
                if topic == "realtime":
                    parsed["next_question"] = "Can you tell me more about your experience?"
                else:
                    idx = session["current_q_index"]
                    next_topic = session["q_bank"][idx] if idx < len(session["q_bank"]) else "Conclusion"
                    parsed["next_question"] = f"Let's move on to: {next_topic}"
            
            
            # Store score in session for analytics
            if "scores" not in session:
                session["scores"] = []
            session["scores"].append(parsed["score"])
            
            # Handle topic index increment based on mode
            if topic == "realtime":
                # Realtime mode: Always increment (no fixed topic areas)
                session["current_q_index"] += 1
            elif "next_action" in parsed:
                # Topic-based mode: Increment conditionally based on answer quality
                next_action = parsed["next_action"]
                if next_action == "move_forward":
                    # Good answer - move to next topic area
                    session["current_q_index"] += 1
                elif next_action in ["clarify_same_concept", "teach_basics"]:
                    # Weak/partial answer - stay on same topic area
                    # Don't increment current_q_index
                    pass
            else:
                # Fallback: increment if next_action not provided
                session["current_q_index"] += 1
            
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
            fallback_question = "Can you tell me more about your experience?"
            if topic != "realtime":
                idx = session.get("current_q_index", 0)
                q_bank = session.get("q_bank", [])
                next_topic = q_bank[idx] if idx < len(q_bank) else "Conclusion"
                fallback_question = f"Let's move on to: {next_topic}"
            
            return {
                "score": 50,
                "quality": "needs_work",
                "feedback_text": "Thank you for your answer.",
                "next_question": fallback_question
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
