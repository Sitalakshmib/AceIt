# 🚀 AceIt - Ultimate Placement Preparation Platform

**AceIt** is a comprehensive, AI-powered placement preparation platform designed to help students master every aspect of the recruitment process. From aptitude tests to coding challenges, group discussions, and mock interviews, AceIt provides a holistic, adaptive, and data-driven learning experience.

---

## 🌟 Core Modules & Features

### 1. 🧠 Aptitude Mastery (Adaptive & Intelligent)
The Aptitude module is built on a sophisticated **Adaptive Learning Engine** that personalizes the experience based on user performance.

#### **A. Practice Mode**
Designed for pure learning without the pressure of a timer.
*   **Adaptive Difficulty**: Uses a **Sliding Window Algorithm** (tracking the last 4 attempts) to dynamically adjust difficulty:
    *   **Level Up**: Accuracy ≥ 75% moves you to the next difficulty (Easy → Medium → Hard).
    *   **Level Down**: Accuracy < 50% drops the difficulty to ensure foundational understanding.
*   **Instant Feedback**: Detailed explanations are shown immediately after submitting an answer.
*   **Smart Question Serving**: Ensures no question repetition for a specific user and topic.
*   **Topic Selection**: Granular filtering by Category (e.g., Quantitative Aptitude) and Sub-topic (e.g., Time & Work).

#### **B. Mock Tests (Examination Simulation)**
Simulates real-world exam conditions with three distinct configurations:
1.  **Full-Length Test**: 30 Questions | 30 Minutes | Mixed Syllabus.
2.  **Section-Wise Test**: 30 Questions | 30 Minutes | Specific Category (e.g., Logical Reasoning).
3.  **Topic-Wise Test**: 20 Questions | 20 Minutes | Targeted Topic Practice.

**Test Features:**
*   **Live Timer & Progress**: Real-time tracking of time remaining and questions attempted.
*   **Question Palette**: Quick navigation to specific questions.
*   **Auto-Submit**: Automatically submits the test when the timer hits zero.

#### **C. Deep Analytics**
Post-test analysis provides actionable insights:
*   **Performance Metrics**: Score, Accuracy (%), and Average Time per Question.
*   **Performance Rating**: Categorizes performance as **Excellent, Good, Average, or Poor**.
*   **Topic Breakdown**: Detailed accuracy percentages for every topic attempted in the test.
*   **Comprehensive Review**: Question-by-question review with:
    *   Your Answer vs Correct Answer.
    *   Detailed Step-by-Step Explanations.

---

### 2. 💻 Coding Arena
A robust coding environment supporting multiple languages and AI assistance.

*   **Multi-Language Support**: Python, Java, C++, C, and R.
*   **Monaco Editor**: Professional-grade code editor with syntax highlighting and auto-completion.
*   **Test Case Validation**:
    *   **Run**: Executes code against visible test cases for quick debugging.
    *   **Submit**: Validates against hidden edge cases to ensure solution robustness.
*   **AI Tutor**: An integrated AI assistant (floating bot) that provides hints, logic explanation, and debugging help without giving away the direct solution.
*   **Smart Filtering**: Filter problems by specific tags (e.g., Arrays, DP), difficulty, or "Bookmarked" status.

---

### 3. 🗣️ Group Discussion (AI-Moderated)
A unique module to practice structuring thoughts and articulating arguments.

*   **AI Topic Generator**: Generates relevant, trending GD topics on demand.
*   **Structured Practice**:
    *   Timer-based session to simulate pressure.
    *   Minimum word count enforcement (20+ chars) to encourage substantial responses.
*   **4-Dimensional AI Scoring**:
    *   **Clarity**: How easy is it to understand your points?
    *   **Coherence**: Logical flow and structuring of arguments.
    *   **Relevance**: Adherence to the core topic.
    *   **Overall Score**: Weighted average of the above metrics.
*   **Detailed Feedback**:
    *   **Strengths & Weaknesses**: AI identifies specific strong points and areas for improvement.
    *   **Topic Study Points**: Provides key facts and arguments you *could* have mentioned.

---

### 4. 🤝 AI Mock Interviewer
Simulates a real interview environment with audio-visual interaction.

#### **Interview Modes:**
*   **Technical**: Focuses on core concepts (Python, Java, SQL, etc.) or "Real-time Adaptive" (context-aware testing).
*   **HR / Behavioral**: Tests soft skills, culture fit, and situational judgment.
*   **Video Presence**: Uses camera feedback to analyze body language and confidence.

#### **Key Features:**
*   **Voice Interaction**:
    *   **AI Speaks**: Text-to-Speech (TTS) engine reads out questions.
    *   **You Speak**: Speech-to-Text (STT) transcribe your answers in real-time.
*   **Live Camera Feed**: Mirrors your video to help you practice maintaining eye contact and professional posture.
*   **Comprehensive Report**:
    *   **Overall Score** & Performance Badge.
    *   **Model Answers**: Compares your response with an "Ideal Response" to highlight gaps.
    *   **Focus Areas**: Specific recommendations (e.g., "Improve detailed explanations for SQL joins").

---

### 5. 📄 Resume Analyzer (ATS-Optimized)
Ensures your resume gets past Applicant Tracking Systems (ATS).

*   **PDF Parsing**: Extracts text from uploaded PDF resumes.
*   **Target Role Mapping**: You specific the target role (e.g., "Frontend Developer"), and the AI analyzes relevance.
*   **Scoring Engine**:
    *   **Overall Score**: General quality rating.
    *   **ATS Score**: Formatting, keyword density, and structure compatibility.
    *   **Skills Match**: Compares your skills against standard requirements for the target role.
*   **Gap Analysis**:
    *   **Found Skills** vs **Missing/Recommended Skills**.
    *   **Critical Alerts**: Missing contact info, bad formatting, or empty sections.
*   **AI Career Coach**: Provides "Actionable Next Steps" to improve the resume immediately.

---

## 🛠️ Technical Stack

*   **Frontend**: React.js, Tailwind CSS, Lucide Icons, Monaco Editor.
*   **Backend**: FastAPI (Python), SQLAlchemy.
*   **Database**: PostgreSQL / SQLite (Dev).
*   **AI/ML**: Integration with LLMs (Groq/OpenAI) for real-time evaluation and content generation.

---

## 🚀 Getting Started

1.  **Backend**:
    ```bash
    cd aceit_backend
    uvicorn main:app --reload
    ```
2.  **Frontend**:
    ```bash
    cd aceit-frontend
    npm run dev
    ```

---
*Built with ❤️ for Student Success.*
