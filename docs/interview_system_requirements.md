# AceIt AI Interview System - Requirements & Audit

## 🛠 System Overview
The AceIt Interview module provides a real-time, voice-based interview experience.
It consists of:
- **Frontend**: React + Vite (Port 5173/5174)
- **Backend**: FastAPI + Python (Port 8000)
- **AI Engine**: Google Gemini (LLM) + Whisper (STT) + gTTS (TTS)

## 🔑 API Keys & Environment Variables

Create a `.env` file in `D:\AceIt\aceit_backend\` with:

```ini
# CORE SERVICES
GEMINI_API_KEY=AIz... (Required for Interview & Prompting)
JWT_SECRET=dev-secret (Required for Auth)

# DATABASE (Used for legacy User Data, optional for Interview flow if using demo user)
# DATABASE_URL=postgresql://user:pass@localhost:5432/aceit

# SYSTEM SETTINGS
# ENV=development
```

## 📦 Dependencies

### Backend (`aceit_backend/requirements.txt`)
- `fastapi` & `uvicorn` (Server)
- `google-generativeai` (LLM)
- `openai-whisper` (Speech-to-Text)
- `gTTS` (Text-to-Speech)
- `python-multipart` (File Uploads)

### Frontend (`aceit-frontend/package.json`)
- `react`, `react-dom`, `vite`
- `axios` (API Client)

## 📡 Ports & Services

| Service | Port | Description |
|---------|------|-------------|
| **Backend** | `8000` | Main API (`/interview/start`, `/static/audio`) |
| **Frontend** | `5173` or `5174` | React UI |
| **Postgres** | `5432` | (Optional) User DB |

## 🛡 CORS Configuration
The backend is configured to allow requests from:
- `http://localhost:5173`
- `http://127.0.0.1:5173`
- `http://localhost:5174` (Fix for "Failed to Fetch")
- `http://127.0.0.1:5174`

## ✅ Validation Checklist

1. **Start Backend**: `python -m uvicorn main:app --reload --port 8000`
2. **Start Frontend**: `npm run dev`
3. **Check Connection**:
   - Backend Health: [http://localhost:8000/health](http://localhost:8000/health) -> `{"status": "healthy"}`
   - Interview Start: [http://localhost:8000/interview/start](http://localhost:8000/interview/start)
4. **Enter Room**:
   - Go to Frontend URL.
   - Click "Enter Interview Room".
   - **Expect**: AI speaks greeting + Valid JSON response in Network Tab.

## 🚨 Troubleshooting
- **"Failed to Fetch"**: Usually means backend is NOT running on port 8000, or CORS blocked port 5174.
- **"404 Not Found"**: Route missing. Restart backend.
- **Audio not playing**: Check `static` folder permissions or Browser Autoplay.
