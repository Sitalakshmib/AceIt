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

#### **D. 🤖 AI Coach (The "Brain")**
A persistent, context-aware personality that guides users through their prep journey.
*   **Context Awareness**: The Coach "knows" you. It pulls real-time data from the `UserAptitudeProgress` and `AIAnalyticsService` to understand:
    *   **Current Confidence Level**: (e.g., "72% in Logical Reasoning").
    *   **Pace Ratio**: (e.g., "0.8x" - You are faster than average).
    *   **Weak Zones**: (e.g., "Struggling with Time & Work").
*   **Voice Interaction**:
    *   **Input**: Uses **OpenAI Whisper** for high-accuracy Speech-to-Text (STT).
    *   **Output**: Uses **OpenAI TTS (Text-to-Speech)** to talk back to you in a natural, human-like voice.
*   **Model Strategy**:
    *   **Primary**: **Groq (Llama-3)** for ultra-low latency conversational responses.
    *   **Fallback**: **GPT-4o** takes over if Groq is unavailable or for complex reasoning tasks.

#### **🔧 Under the Hood (Aptitude)**
*   **Data Models**: Uses `UserAptitudeProgress` to track multidimensional difficulty metrics:
    *   **Concept Depth**: Single vs Multi-concept problems.
    *   **Cognitive Load**: Complexity of the problem statement.
*   **Adaptive Logic**: The system maintains a localized history of the last 4 attempts per topic to calculate a moving average accuracy, triggering instantaneous difficulty adjustments.

---

### 2. 💻 Coding Arena
A robust coding environment supporting multiple languages and AI assistance.

*   **Multi-Language Support**: Python, Java, C++, C, and R.
*   **Monaco Editor**: Professional-grade code editor with syntax highlighting and auto-completion.
*   **Test Case Validation**:
    *   **Run**: Executes code against visible test cases for quick debugging.
    *   **Submit**: Validates against hidden edge cases to ensure solution robustness.
*   **Smart Filtering**: Filter problems by specific tags (e.g., Arrays, DP), difficulty, or "Bookmarked" status.

#### **A. 🤖 AI Tutor (Coding Companion)**
A dedicated coding assistant embedded in the IDE, powered by **Google Gemini Pro** and **Groq**. It follows strict pedagogical rules to *teach*, not just *solve*.
*   **Progressive Hint System**:
    *   **Level 1**: Strategy (e.g., "Try using a Two-Pointer approach").
    *   **Level 2**: Algorithm (e.g., "Initialize pointers at start and end...").
    *   **Level 3**: Pseudocode (logic structure without syntax).
*   **Smart Debugger**:
    *   Analyzes `Input` + `Expected Output` + `Actual Output` + `Error Message`.
    *   Generates a "What to Fix" checklist (e.g., "You have an off-by-one error in your loop condition").
*   **Code Reviewer**:
    *   Evaluates **Time/Space Complexity** (Big O).
    *   Suggests **Best Practices** (naming conventions, modularity).
    *   Identifies **Edge Cases** you missed (e.g., "What if the array is empty?").

#### **🔧 Under the Hood (Coding)**
*   **Hybrid Execution Engine**:
    *   **Local Execution**: Python code runs in a secure, isolated local subprocess for maximum speed.
    *   **Remote Execution**: Java, C++, and JavaScript use the **Piston API** for secure, sandboxed execution.
*   **Security**: Implements strict 10-second timeouts (`EXECUTION_TIMEOUT`) and resource limits to prevent infinite loops or malicious code.
*   **Test Runners**: Custom wrapper scripts for each language (e.g., `_wrap_java`, `_wrap_cpp`) invoke the user's function and compare outputs against JSON-defined test cases.

---

### 3. 🗣️ Group Discussion (AI-Moderated)
A dual-mode module designed to help you master both *content generation* and *articulation*.

#### **A. AI Topic Analysis (Content Builder)**
Struggling with what to say? The **Topic Analysis** tool helps you build a knowledge base before you speak.
*   **Custom Topic Engine**: Enter *any* topic (e.g., "Moonlighting in IT", "G20 Summit"), and the AI instantly generates a comprehensive cheat sheet.
*   **Balanced Perspectives**: Generates a structured list of **Arguments FOR** and **Arguments AGAINST** the motion.
*   **Smart Copy**: One-click copy for points to save them to your notes.
*   **Use Case**: Perfect for researching trending topics or preparing for specific company GD rounds.

#### **B. Practice Mode (Simulation)**
Simulates a real GD environment to test your articulation and thought process.
*   **AI Topic Generator**: If you don't have a topic, the system generates relevant, trending GD topics (50% from a curated high-frequency list, 50% freshly generated by AI).
*   **Simulation Flow**:
    1.  **Think**: You get a topic and time to structure your thoughts.
    2.  **Speak (Write)**: Type your response (mimicking the "speaking" phase) with an enforced minimum character limit to ensure depth.
    3.  **Analyze**: Instant AI evaluation.
*   **4-Dimensional AI Scoring**:
    *   **Clarity (0-10)**: Analyzes language precision and readability.
    *   **Coherence (0-10)**: Evaluates the logical flow and transition between arguments.
    *   **Relevance (0-10)**: Checks strictly for adherence to the core topic (detecting bluffing).
    *   **Overall Score**: A weighted average providing a final performance metric.
*   **Detailed Feedback**:
    *   **Strengths & Weaknesses**: AI identifies specific strong points (e.g., "Good use of examples") and areas for improvement (e.g., "Conclusion was abrupt").
    *   **Topic Study Points**: The AI generates 4-5 "Gold Standard" points—facts, statistics, or powerful arguments—that you *could* have used, helping you maximize your content depth for next time.

#### **🔧 Under the Hood (GD)**
*   **Prompt Engineering**: The feedback engine uses a multi-shot prompt technique to ensure the AI acts as a "Strict MBA Evaluator," prioritizing logic over flowery language.
*   **Hybrid Generation**: Topic generation uses a probabilistic router—sending 50% of requests to a static, high-quality database (for stability) and 50% to **Groq/Llama-3** (for novelty and current affairs).

---

### 4. 🤝 AI Mock Interviewer
A comprehensive simulation engine that prepares you for every stage of the interview process.

#### **Interview Modes:**
*   **Technical (Adaptive)**: Real-time, context-aware questions based on your Resume and Job Description.
*   **Topic-Specific Practice**: Focused drills on core technologies (Python, Java, SQL, .NET).
    *   **Round 1**: Covers fundamental concepts.
    *   **Round 2**: Adapts to your weak areas from Round 1 and increases difficulty.
*   **Project-Based**: Deep-dive discussions on your specific projects (Architecture, Tech Stack choices, Challenges faced).
*   **HR / Behavioral**: STAR method evaluation for soft skills, culture fit, and situational judgment.
*   **Video Presence (AI Mirror)**: Analyzes your body language and speech delivery in real-time.

#### **Key Features:**
*   **Voice Interaction**: Full-duplex voice conversation using **Whisper** (Speech-to-Text) and **OpenAI/ElevenLabs** (Text-to-Speech) for a natural flow.
*   **Visual Analysis**: Real-time feedback on your non-verbal cues (Eye Contact, Head Stability, Smile/Warmth).
*   **Comprehensive Report**:
    *   **Overall Score** & Performance Badge.
    *   **Speech Clarity**: Detects filler words ("um," "ah") and hesitation.
    *   **Model Answers**: Compares your response with an "Ideal Response" to highlight gaps.

#### **🔧 Under the Hood (Interview)**
*   **Dual Engine Architecture**:
    *   **Text Engine**: Standard chat-based interface with state management.
    *   **Voice Engine (`SimVoiceInterviewer`)**: Handles audio buffers, transcription, and TTS generation in-memory (privacy-focused).
*   **Hybrid Analysis (Video Presence)**:
    *   **Frontend (Edge AI)**: Uses **MediaPipe FaceLandmarker** running directly in the browser (~20 FPS) to analyze facial cues without sending video to the server.
    *   **Backend (Audio)**: Analyzes audio blobs for speech patterns, filler words, and confidence levels.
*   **Adaptive Question Bank**:
    *   **Dynamic Generation**: Questions are not hardcoded; they are generated on-the-fly using LLM prompts tailored to the user's resume and the specific interview context.
    *   **State Management**: Maintains a session state in `data/interview_sessions.json` to track progress across rounds and provide periodic feedback every 2-3 questions.

---

### 5. 📄 Resume Analyzer & Builder (ATS-Optimized)
A dual-purpose tool to **analyze** existing resumes against industry standards and **build** new ones from scratch.

#### **Key Features:**
*   **Deep PDF Parsing**: Extracts text from likely complex PDF layouts using a multi-stage approach (`pdfplumber` → `PyPDF2` fallback).
*   **Target Role Mapping**: Select from 8+ preset profiles (e.g., Full Stack Dev, Data Scientist, Product Manager) to tailor the analysis.
*   **Gap Analysis Engine**:
    *   **Skills Match**: Compares your skills against a curated database of required technologies for the selected role.
    *   **Critical Alerts**: Instantly flags missing contact info, broken links, or absent sections (Summary, Projects, etc.).
*   **AI Career Coach**: Uses Gemini to provide subjective feedback—identifying "Impact Gaps" (e.g., "You listed responsibilities but didn't quantify results").
*   **Resume Builder**: A wizard-style interface to create ATS-friendly, correctly formatted resumes by simply filling in your details.

#### **🔧 Under the Hood (Resume)**
*   **Hybrid Analysis System (60/40 Split)**:
    *   **Rule-Based Engine (60%)**: A deterministic scoring system using Regex to validate:
        *   **Contact Info (25 pts)**: Email, Phone, LinkedIn, GitHub/Portfolio.
        *   **Structure (30 pts)**: Presence of essential sections.
        *   **Formatting (20 pts)**: Checks for bullet point usage and Action Verb density.
        *   **Content Quality (25 pts)**: Detects quantifiable metrics (%, $, numbers) and career timeline clarity.
    *   **AI-Based Engine (40%)**: **Google Gemini** evaluates the *quality* of writing, tone, and impact, providing the "Overall Impression" and "Actionable Tips."
*   **Scoring Algorithm**:
    *   `Final Score = (ATS_Score * 0.6) + (Skills_Match_Score * 0.4)`
*   **PDF Generation**: Uses `jsPDF` (Frontend) and `python-docx` (Backend) to generate professional, parsable documents.

---

## 🛠️ Technical Stack

### **Frontend (Client-Side)**
*   **Framework**: [React 19](https://react.dev/) + [Vite](https://vitejs.dev/) (High-performance build tool).
*   **Styling**: [Tailwind CSS 4](https://tailwindcss.com/) (Utility-first design system).
*   **State Management**: React Hooks & Context API.
*   **Visualizations**: `Recharts`, `Chart.js`, `React-Chartjs-2` (Data-driven analytics).
*   **AI Integration**: `@mediapipe/tasks-vision` (Client-side Computer Vision).
*   **Code Editor**: Monaco Editor (VS Code core) for a professional coding experience.
*   **Icons**: Lucide React.

### **Backend (Server-Side)**
*   **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (High-performance, async Python web framework).
*   **Language**: Python 3.11+.
*   **Database**:
    *   **Production**: PostgreSQL (Recommended).
    *   **Development**: SQLite (`aceit_dev.db`).
*   **ORM**: SQLAlchemy (Database abstraction).
*   **Security**: OAuth2 with JWT (JSON Web Tokens) & `bcrypt` password hashing.

### **🤖 AI & Machine Learning Pipeline**
*   **Core Logic**: [Google Gemini Pro / Flash](https://deepmind.google/technologies/gemini/) (Primary Reasoning Engine).
*   **Fallback / Specialized Models**: Groq (Llama-3) for ultra-low latency requirements.
*   **Vision**: MediaPipe FaceLandmarker (Edge AI).
*   **Voice Processing**:
    *   **STT**: OpenAI Whisper (Speech-to-Text).
    *   **TTS**: gTTS / ElevenLabs (Text-to-Speech).
*   **Document Parsing**: `pdfplumber`, `PyPDF2`, `python-docx`.

---

## 📂 Project Structure

```bash
AceIt/
├── aceit-frontend/          # React + Vite Frontend
│   ├── src/
│   │   ├── components/      # Reusable UI Components
│   │   ├── contexts/        # Auth & Global State
│   │   ├── services/        # API Client & Endpoints
│   │   └── pages/           # Main Route Views (Aptitude, Interview, etc.)
│   └── package.json         # Frontend Dependencies
│
├── aceit_backend/           # FastAPI Backend
│   ├── services/            # Core Business Logic (AI, Scoring, Parsing)
│   ├── routes/              # API Endpoints (Auth, Resume, Interview)
│   ├── models/              # Database Schema (SQLAlchemy)
│   ├── main.py              # Application Entry Point
│   └── requirements.txt     # Python Dependencies
│
└── README.md                # Project Documentation
```

---

## 💡 Key System Highlights

### **1. Adaptive Difficulty Algorithm (Aptitude)**
The system uses a **Sliding Window** approach to adjust question difficulty in real-time.
```python
def adjust_difficulty(user_history):
    # Analyze last 4 attempts
    recent_accuracy = sum(user_history[-4:]) / 4
    
    if recent_accuracy >= 0.75:
        return "INCREASE_DIFFICULTY"  # Easy -> Medium -> Hard
    elif recent_accuracy < 0.50:
        return "DECREASE_DIFFICULTY"  # Hard -> Medium -> Easy
    return "MAINTAIN_LEVEL"
```

### **2. Interview Session State Management**
Maintains context across the interview to ensure logical follow-up questions.
```json
{
  "session_id": "uuid-v4",
  "mode": "technical_java",
  "current_topic": "multithreading",
  "difficulty": "medium",
  "history": [
    { "q": "Explain deadlock.", "performance": 0.85 },
    { "q": "How to prevent it?", "performance": 0.90 }
  ],
  "next_action": "increase_complexity"
}
```

---

## 🚀 Getting Started

### **Prerequisites**
*   **Node.js**: v18+
*   **Python**: v3.11+
*   **Tesseract OCR** (Optional, for Resume Parsing)

### **1. Clone the Repository**
```bash
git clone https://github.com/Sitalakshmib/AceIt.git
cd AceIt
```

### **2. Backend Setup**
Navigate to the backend directory and set up the Python environment.
```bash
cd aceit_backend

# Install dependencies
pip install -r requirements.txt

# Create .env file
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "GROQ_API_KEY=your_key_here" >> .env
echo "OPENAI_API_KEY=your_key_here" >> .env

# Run the server
uvicorn main:app --reload
```
*   *Server runs at: `http://localhost:8000`*
*   *Swagger Docs: `http://localhost:8000/docs`*

### **3. Frontend Setup**
Navigate to the frontend directory and install dependencies.
```bash
cd ../aceit-frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```
*   *App runs at: `http://localhost:5173`*

---
*Built with ❤️ for Student Success.*
