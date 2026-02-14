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
    *   **Your Answer** vs **Correct Answer**.
    *   Detailed **Step-by-Step Explanations**.

#### **D. 🤖 AI Coach (The "Brain")**
A persistent, context-aware personality that guides users through their prep journey.
*   **Context Awareness**: The Coach "knows" you by pulling real-time data from `UserAptitudeProgress` and `AIAnalyticsService`:
    *   **Current Confidence Level**: (e.g., "72% in Logical Reasoning").
    *   **Pace Ratio**: (e.g., "0.8x" - You are faster than average).
    *   **Weak Zones**: (e.g., "Struggling with Time & Work").
*   **Voice Interaction**:
    *   **Input**: Uses **OpenAI Whisper** for high-accuracy Speech-to-Text (STT).
    *   **Output**: Uses **OpenAI TTS (Text-to-Speech)** to talk back in a natural voice.
*   **Model Strategy**:
    *   **Primary**: **Groq (Llama-3)** for ultra-low latency conversational responses.
    *   **Fallback**: **GPT-4o** for complex reasoning tasks.

#### **🔧 Under the Hood (Aptitude)**
*   **Data Models**: Tracks multidimensional difficulty metrics including:
    *   **Concept Depth**: Logic for single vs multi-concept problems.
    *   **Cognitive Load**: Complexity analysis of the problem statement.
*   **Adaptive Logic**: Maintains a localized history of the last 4 attempts per topic to trigger instantaneous difficulty adjustments via moving average accuracy.

---

### 2. 💻 Coding Arena

A robust coding environment supporting multiple languages and AI assistance.

#### **Main Features**
*   **Multi-Language Support**: Python, Java, C++, C, and R.
*   **Monaco Editor**: Professional-grade code editor with syntax highlighting and auto-completion.
*   **Test Case Validation**:
    *   **Run**: Executes code against visible test cases for quick debugging.
    *   **Submit**: Validates against hidden edge cases to ensure solution robustness.
*   **Smart Filtering**: Filter problems by specific tags (e.g., Arrays, DP), difficulty, or "Bookmarked" status.

#### **A. 🤖 AI Tutor (Coding Companion)**
A dedicated assistant embedded in the IDE, powered by **Google Gemini Pro** and **Groq**.
*   **Progressive Hint System**:
    *   **Level 1**: Strategy (e.g., "Try using a Two-Pointer approach").
    *   **Level 2**: Algorithm (e.g., "Initialize pointers at start and end...").
    *   **Level 3**: Pseudocode (logic structure without syntax).
*   **Smart Debugger**: Analyzes `Input` + `Expected` + `Actual` + `Error` to generate a "What to Fix" checklist.
*   **Code Reviewer**: Evaluates **Time/Space Complexity** (Big O) and suggests **Best Practices**.

#### **🔧 Under the Hood (Coding)**
*   **Hybrid Execution Engine**:
    *   **Local Execution**: Python code runs in a secure, isolated local subprocess.
    *   **Remote Execution**: Java, C++, and JavaScript use the **Piston API** for sandboxed execution.
*   **Security & Safety**:
    *   **Execution Timeout**: Strict 10-second limit to prevent infinite loops.
    *   **Resource Limits**: Sandboxed environments ensure system security.
*   **Test Runners**: Language-specific wrappers (e.g., `_wrap_java`) compare outputs against JSON-defined test cases.

---

### 3. 🗣️ Group Discussion (AI-Moderated)

A dual-mode module designed to master both content generation and articulation.

#### **A. AI Topic Analysis (Content Builder)**
*   **Custom Topic Engine**: Generates comprehensive cheat sheets for *any* user-entered topic.
*   **Balanced Perspectives**: Provides structured lists of **Arguments FOR** and **Arguments AGAINST**.
*   **Smart Utils**: One-click copy for points.

#### **B. Practice Mode (Simulation)**
*   **AI Topic Generator**: Fusion of curated lists and AI-generated trending topics (50/50 split).
*   **Simulation Flow**:
    1.  **Think Phase**: Time-limited brainstorming.
    2.  **Speak Phase**: Depth-enforced written response.
    3.  **Analyze Phase**: Real-time evaluation.
*   **4-Dimensional AI Scoring**:
    *   **Clarity**: Language precision.
    *   **Coherence**: Logical flow and transitions.
    *   **Relevance**: Subject-matter adherence.
    *   **Overall Score**: Weighted performance summary.
*   **Actionable Feedback**:
    *   **Strengths/Weaknesses**: Identifies specific hits and misses.
    *   **Gold Standard Points**: Facts/stats for next-time maximization.

#### **🔧 Under the Hood (GD)**
*   **Prompt Engineering**: Multi-shot prompting ensuring a "Strict MBA Evaluator" persona.
*   **Router Logic**: Probabilistic router for topic variety (Static Database vs Groq/Llama-3).

---

### 4. 🤝 AI Mock Interviewer

A comprehensive simulation engine that prepares you for every stage of the interview process.

#### **Interview Modes:**
*   **Technical (Adaptive)**: Resume/JD context-aware questions.
*   **Topic Practice**: Focused technology drills (Python, Java, etc.) with progressive rounds.
*   **Project-Based**: Architecture and tech stack deep-dives.
*   **HR / Behavioral**: STAR method evaluations for soft-skills.
*   **Video Presence (AI Mirror)**: Real-time body-language and speech analysis.

#### **Key Features:**
*   **Voice Interaction**: Full-duplex conversation using **Whisper (STT)** and **OpenAI/ElevenLabs (TTS)**.
*   **Visual Analysis**: Real-time tracking of eye contact, head stability, and smile/warmth.
*   **Comprehensive Reporting**:
    *   **Score & Badge**: Performance categorization.
    *   **Speech Clarity**: Detection of filler words ("um," "ah") and hesitation.
    *   **Model Comparison**: Your answer vs Ideal Response gaps.

#### **🔧 Under the Hood (Interview)**
*   **Dual Engine Architecture**:
    *   **Text Engine**: State-managed standard chat.
    *   **Voice Engine**: In-memory audio processing for privacy and speed.
*   **Hybrid Analysis (Video Presence)**:
    *   **Frontend (Edge AI)**: **MediaPipe FaceLandmarker** running at ~20 FPS in-browser.
    *   **Backend (Audio)**: Blobs analyzed for speech patterns and confidence levels.
*   **Adaptive Selection**: Questions generated on-the-fly via prompts tailored to user context and session state.

---

### 5. 📄 Resume Analyzer & Builder (ATS-Optimized)

A dual-purpose tool to analyze existing resumes and build new ones from scratch.

#### **Key Features:**
*   **Deep PDF Parsing**: Multi-stage approach (`pdfplumber` → `PyPDF2` fallback).
*   **Target Role Mapping**: Tailor analysis to 8+ professional profiles.
*   **Gap Analysis Engine**:
    *   **Skills Match**: Curated database comparison.
    *   **Critical Alerts**: Detection of missing info or broken links.
*   **AI Coach Insights**: Gemini-powered feedback on "Impact Gaps."
*   **Resume Builder**: Wizard-style interface for ATS-friendly document creation.

#### **🔧 Under the Hood (Resume)**
*   **Hybrid Analysis (60/40 Split)**:
    *   **Rule-Based (60%)**: Regex validation of contact info, structure, and formatting.
    *   **AI-Based (40%)**: **Google Gemini** evaluation of content quality, tone, and impact.
*   **Scoring Algorithm**: `Final Score = (ATS_Score * 0.6) + (Skills_Match_Score * 0.4)`.
*   **Document Generation**: `jsPDF` (Frontend) and `python-docx` (Backend).

---

## 🛠️ Technical Stack

### **Frontend (Client-Side)**
*   **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/)
*   **Styling**: [Tailwind CSS 4](https://tailwindcss.com/)
*   **Visuals**: `Recharts`, `Chart.js`
*   **Interactive**: Monaco Editor, Lucide Icons

### **Backend (Server-Side)**
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.11+)
*   **Database**: PostgreSQL / SQLite (`SQLAlchemy` ORM)
*   **Security**: OAuth2, JWT, `bcrypt`

### **🤖 AI & Machine Learning**
*   **Reasoning**: Google Gemini Pro / Flash, Groq (Llama-3)
*   **Vision**: MediaPipe FaceLandmarker (Edge AI)
*   **Audio**: OpenAI Whisper (STT), OpenAI TTS / ElevenLabs
*   **Parsing**: `pdfplumber`, `PyPDF2`, `python-docx`

---

## 📂 Project Structure

```bash
AceIt/
├── aceit-frontend/          # React + Vite Frontend
│   ├── src/
│   │   ├── components/      # UI Components
│   │   ├── contexts/        # Auth & State
│   │   ├── services/        # API Client
│   │   └── pages/           # Route Views
│
├── aceit_backend/           # FastAPI Backend
│   ├── services/            # Business Logic
│   ├── routes/              # API Endpoints
│   ├── models/              # Database Schema
│   └── main.py              # Entry Point
│
└── README.md                # Documentation
```

---

## 💡 Key System Highlights

### **1. Adaptive Difficulty Algorithm (Aptitude)**
```python
def adjust_difficulty(user_history):
    # Analyze last 4 attempts
    recent_accuracy = sum(user_history[-4:]) / 4
    
    if recent_accuracy >= 0.75:
        return "INCREASE_DIFFICULTY"
    elif recent_accuracy < 0.50:
        return "DECREASE_DIFFICULTY"
    return "MAINTAIN_LEVEL"
```

### **2. Interview Session State Management**
```json
{
  "session_id": "uuid-v4",
  "mode": "technical_java",
  "current_topic": "multithreading",
  "history": [
    { "q": "Explain deadlock.", "performance": 0.85 }
  ],
  "next_action": "increase_complexity"
}
```

---

## 🚀 Getting Started

### **1. Clone the Repository**
```bash
git clone https://github.com/Sitalakshmib/AceIt.git
cd AceIt
```

### **2. Backend Setup**
```bash
cd aceit_backend
pip install -r requirements.txt
# Configure .env with GEMINI_API_KEY, GROQ_API_KEY, OPENAI_API_KEY
uvicorn main:app --reload
```

### **3. Frontend Setup**
```bash
cd ../aceit-frontend
npm install
npm run dev
```

---
*Built with ❤️ for Student Success.*
