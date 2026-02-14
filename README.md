# AceIt - AI-Powered Placement Preparation Platform

**AceIt** is a comprehensive, AI-driven platform designed to help students and job seekers prepare for recruitment processes. It integrates multiple modules covering every aspect of placement preparation, from aptitude tests and coding challenges to AI-simulated interviews and soft skills training.

## 🚀 Key Features

AceIt provides a holistic preparation experience through the following specialized modules:

### 1. 🧩 Aptitude Module
Master quantitative, logical, and verbal reasoning skills.
*   **Practice Mode**: Topic-wise practice questions with detailed explanations.
*   **Mock Tests**: Full-length timed tests to simulate real exam conditions.
*   **Smart Analytics**: Track performance, identify weak areas, and monitor progress over time.
*   **AI Coach**: Personalized guidance and study recommendations based on performance.

### 2. 💻 Coding Module
A robust Integrated Development Environment (IDE) for programming practice.
*   **Rich Problem Library**: Curated collection of problems ranging from Easy to Hard.
*   **Online Compiler**: Execute code in real-time (Python supported) with custom test cases.
*   **AI Tutor**:
    *   **Hints**: Get progressive hints without revealing the full solution.
    *   **Debug Assistant**: AI analyzes your code to explain why it failed test cases.
    *   **Code Review**: Get feedback on code quality, efficiency, and best practices.
*   **Bookmarks & Progress**: Save important problems and track solved capability.

### 3. 🎙️ AI Interviewer
Simulate realistic HR and Technical interviews.
*   **Voice-Enabled**: Speak naturally to the AI interviewer (Speech-to-Text & Text-to-Speech).
*   **Real-time Analysis**: Immediate feedback on answer relevance, confidence, and fluency.
*   **Dynamic Questioning**: The AI adapts follow-up questions based on your responses.

### 4. 📹 Video Presence & Communication
Enhance your non-verbal communication and soft skills.
*   **Video Analysis**: Uses computer vision (MediaPipe) to track eye contact, head stability, and facial expressions.
*   **Speech Analysis**: Detects hesitation, filler words (um, uh), and speech pace.
*   **Communication Drills**: Practice answering common behavioral questions with instant scoring on fluency and confidence.

### 5. 🗣️ Group Discussion (GD) Practice
Prepare for group discussions with AI agents.
*   **Simulated Round Table**: Participate in a GD with multiple AI characters.
*   **Topic Analysis**: Get insights and key points for various trending topics.
*   **Performance Scoring**: Evaluate your entry points, content relevance, and leadership skills.

### 6. 📄 Resume Analyzer
Optimize your CV for Applicant Tracking Systems (ATS).
*   **ATS Scoring**: Check how well your resume parsers against standard algorithms.
*   **Keyword Analysis**: Identify missing keywords relevant to your target job roles.
*   **Formatting Checks**: Ensure your resume meets professional formatting standards.

---

## 🛠️ Technology Stack

### Frontend
*   **Framework**: React (Vite)
*   **Styling**: TailwindCSS, Lucide React (Icons)
*   **Charts**: Chart.js, Recharts
*   **Editor**: Monaco Editor (VS Code like experience)

### Backend
*   **Framework**: FastAPI (Python)
*   **Database**: PostgreSQL (NeonDB) / SQLite (Local Dev)
*   **ORM**: SQLAlchemy
*   **AI/ML**:
    *   **LLMs**: Gemini 1.5 Flash / OpenAI GPT-4o (for generic reasoning & coaching)
    *   **Groq**: Llama 3 (for high-speed responses)
    *   **Computer Vision**: Google MediaPipe (for posture & gesture analysis)
    *   **Audio**: OpenAI Whisper (Scanning & Transcription)

---

## ⚙️ Installation & Setup

### Prerequisites
*   Node.js (v18+)
*   Python (v3.9+)
*   PostgreSQL (Optional, SQLite enabled by default)

### 1. Clone the Repository
```bash
git clone https://github.com/Sitalakshmib/AceIt.git
cd AceIt
```

### 2. Backend Setup
```bash
cd aceit_backend
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup Environment Variables
# Create a .env file in aceit_backend/ with:
# GEMINI_API_KEY=your_key_here
# DATABASE_URL=your_postgres_url (optional)

# Run the Server
python main.py
```
*Backend runs on: `http://localhost:8000`*

### 3. Frontend Setup
```bash
cd aceit-frontend
# Install dependencies
npm install

# Run the Development Server
npm run dev
```
*Frontend runs on: `http://localhost:5173`*

---

## 📂 Directory Structure

```
AceIt/
├── aceit_backend/          # FastAPI Backend
│   ├── routes/             # API Endpoints (Auth, Coding, Interview, etc.)
│   ├── services/           # Business Logic & AI Integrations
│   ├── models/             # Database Models (SQLAlchemy)
│   ├── data/               # Static Data & Seed Files
│   └── main.py             # Entry Point
│
└── aceit-frontend/         # React Frontend
    ├── src/
    │   ├── components/     # Reusable UI Components
    │   ├── pages/          # Main Application Pages
    │   ├── context/        # React Context (Auth, State)
    │   └── assets/         # Images & Styles
    └── package.json
```

---

## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements.

## 📄 License
This project is licensed under the MIT License.
