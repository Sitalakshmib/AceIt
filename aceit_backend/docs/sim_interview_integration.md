# SimInterview Engine Integration

This document details the integration of the AI Interview Engine into AceIt.

## 1. Overview
The **SimInterview Engine** provides a human-like AI interviewer that adapts to candidate answers.
It uses **Google Gemini** for generating questions and **OpenAI Whisper** for Speech-to-Text.

## 2. Architecture

### Service Layer
- **`services/sim_interview_engine.py`**: 
  - Manages interview sessions (`start`, `process_answer`, `generate_next`).
  - Maintains conversation history and context (Resume, JD).
  - Uses `LLMClient` to communicate with Gemini.
- **`services/stt_service.py`**:
  - Handles audio transcription using `openai-whisper`.
  - Used by both the STT route and the Interview route.

### API Layer (`routes/interview.py`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/interview/start-ai` | POST | Starts a new session with Resume and JD. |
| `/interview/answer-ai` | POST | Submits an answer (Text or Audio). Returns automated transcription if audio. |
| `/interview/next-ai` | POST | Generates the next question based on history. |

## 3. How to Run

1. **Start the Backend**:
   ```bash
   cd aceit_backend
   python -m uvicorn main:app --reload --port 8000
   ```
2. **Environment Variables**:
   Ensure `GEMINI_API_KEY` is set in `.env`.

## 4. Testing

A verification script is available:
```bash
python scripts/test_sim_interview.py
```
This script:
1. Starts an interview.
2. Submits a text answer.
3. Retrieves the next question.
4. Submits a mock audio file.

## 5. Output Format
Standardized JSON response for questions:
```json
{
  "question": "Tell me about yourself.",
  "topic": "introduction",
  "difficulty": "easy",
  "feedback": "Good start.",
  "score": 0,
  "is_completed": false
}
```
