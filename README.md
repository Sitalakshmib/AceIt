# AceIt - AI-Powered Placement Preparation Platform

**AceIt** is a comprehensive, AI-driven platform designed to prepare students for recruitment processes. It covers every stage of placement: **Aptitude, Coding, Group Discussion, Technical Interviews, and Resume Building**.

The system leverages advanced analytics, adaptive learning algorithms (Sliding Window & Round Robin), and Generative AI (Gemini) to provide personalized feedback and real-time coaching.

---

## 🚀 Key Modules & Features

### 1. 🧠 Aptitude Training Module
*Master quantitative, logical, and verbal reasoning with an adaptive learning engine.*

#### **Practice Mode (Adaptive Learning)**
- **Intelligent Question Selection**:
  - **Round Robin Algorithm**: Ensures diversity in question selection across different sub-topics, preventing repetitive patterns.
  - **Sliding Window Approach**: The "Adaptive Engine" uses a sliding window of your last **4 attempts** to dynamically adjust difficulty (Easy → Medium → Hard). If you consistently answer correct, the window shifts to harder problems.
- **IndiaBIX-Style Interface**: One question at a time with instant validation and detailed explanations.
- **Categorized Learning**: Topics are structured hierarchically (Category → Topic → Question).

#### **Mock Test System**
- **Three Test Types**:
  1.  **Full-Length Test**: 30 Questions | 30 Minutes | Mixed Topics.
  2.  **Section-Wise Test**: 30 Questions | 30 Minutes | Specific Category (e.g., Logical Reasoning).
  3.  **Topic-Wise Test**: 20 Questions | 20 Minutes | Specific Topic (e.g., Probability).
- **Test Characteristics**:
  - **Randomized Options**: Answer choices are shuffled at runtime to prevent muscle memory.
  - **Auto-Submission**: Tests automatically submit when the timer expires.
- **Detailed Analytics**:
  - **Performance Metrics**: Score, Accuracy %, Average Time per Question.
  - **Rating System**: Classifies performance as *Good* (≥75%), *Average* (50-75%), or *Poor* (<50%).
  - **Topic Performance**: Breakdown of accuracy per topic to identify specific weak areas.
- **Comprehensive Review**:
  - View "Your Answer" vs. "Correct Answer".
  - Detailed step-by-step explanations for every question.

#### **AI Aptitude Coach**
- **User Tier Classification**: Classifies users as *Developing, Competent, or Advanced* based on accuracy and speed.
- **Error Pattern Analysis**: Detects if your mistakes are due to:
  - *Conceptual Errors*
  - *Careless Mistakes*
  - *Overthinking*
  - *Time Pressure*
- **Strength & Weakness Identification**: Automatically highlights your top 3 strong topics and bottom 3 weak areas.

---

### 2. 💻 Coding Arena (CodeSprint)
*A robust competitive programming environment with real-time compilation.*

#### **Core Features**
- **Dual Execution Modes**:
  - **Run Code**: Executes against **3 visible sample test cases** for quick debugging.
  - **Submit Code**: Validates against **all test cases (including hidden/edge cases)** for final verification.
- **Problem Repository**:
  - Hybrid database: Fetches from local optimized DB or falls back to internal problem bank.
  - Categorized by Difficulty (Easy, Medium, Hard) and Tags (e.g., Arrays, DP, Sliding Window).
- **Bookmarks**: Save interesting or difficult problems for later review.

#### **Progress Analytics**
- **Heatmap & Streak**: Visualizes daily activity (similar to GitHub/LeetCode) and tracks current/max daily streaks.
- **Solved Counters**: Tracks total solved count broken down by difficulty (Easy/Medium/Hard).
- **Recent Activity Log**: Detailed history of all submission attempts and their outcomes.

---

### 3. 🗣️ Group Discussion (GD) Prep
*AI-simulated round-table discussion analysis.*

#### **Simulated Environment**
- **Smart Topic Generator**: Generates trending and relevant GD topics (Abstract, Current Affairs, Management).
- **Real-time Rules**: Enforces minimum content length (20+ chars) to encourage meaningful contributions.

#### **AI Feedback Engine**
- **Scoring Metrics (0-10)**:
  - **Clarity**: How clear and understandable your argument is.
  - **Coherence**: Flow and logical structure of your points.
  - **Relevance**: Adherence to the specific topic.
- **Qualitative Analysis**:
  - **Strengths**: What you did well (e.g., "Good use of examples").
  - **Weaknesses**: Areas to improve (e.g., "Avoid repetition").
- **Knowledge Enhancement**: The AI proactively provides **"Relevant Points to Study"**, giving you key facts and arguments you *could* have used for that specific topic.

---

### 4. 🎙️ AI Technical Interviewer
*Voice-enabled mock interviews with a virtual hiring manager.*

#### **Interview Modes**
- **Technical**: Deep dive into specific tech stacks (Python, Java, DBMS).
- **HR**: Behavioral questions (Strengths, Weaknesses, Situational).
- **Project-Based**: Questions tailored specifically to your project description.

#### **Analysis & Feedback**
- **Question-by-Question Review**:
  - Scores every answer (0-100).
  - Categorizes answers into *Strengths* (Score > 75) and *Needs Improvement* (Score < 60).
- **Model Answers**: For any answer scoring low, the AI generates an **Ideal Response**, teaching you exactly how a top candidate would answer that specific question.
- **Overall Performance**: Aggregated score and final verdict (Excellent, Good, Fair, Needs Improvement).

---

### 5. 📄 Smart Resume Analyzer & Builder
*ATS-Optimized resume creation and auditing.*

#### **AI Resume Analyzer**
- **ATS Scoring Engine (0-100)**:
  - **Contact Info Check**: Verifies Email, Phone, LinkedIn, GitHub.
  - **Section Audit**: Checks for presence of Summary, Experience, Projects, Skills.
  - **Formatting Score**: Analyzes bullet point usage and action verbs.
  - **Content Quality**: Detects quantifiable achievements (numbers, percentages).
- **Skills Gap Analysis**: Matches your resume keywords against specific Job Roles (e.g., *Full Stack Developer*) to find missing critical skills.
- **AI Career Coach**: Generates a strategic summary of "Top Strengths" and "Focus Areas" with actionable tips to increase interview callbacks.

#### **Resume Builder**
- **AI-Enhanced Content**: Input your raw details, and the AI rewrites your descriptions to be more professional and impactful.
- **One-Click Export**: Generates a perfectly formatted, ATS-friendly **DOCX** file.

---

## 🛠️ Tech Stack
- **Frontend**: React.js, Tailwind CSS, Lucide React (Icons), Recharts (Analytics).
- **Backend**: FastAPI (Python), SQLAlchemy (ORM).
- **Database**: PostgreSQL (NeonDB).
- **AI/ML**: Google Gemini Pro (GenAI), Scikit-Learn (Adaptive Algorithms).
- **Tools**: PyPDF2/PDFPlumber (Resume Parsing), SpeechRecognition (Interview).

---
*Built with ❤️ for AceIt.*
