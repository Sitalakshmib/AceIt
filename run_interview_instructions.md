# How to Run the Integrated Interview Module

The SimInterview Engine is now fully integrated into the backend. You can run it either via the **Web Frontend** or using **Backend Scripts**.

## Option 1: Run via Web Frontend (Recommended)
This uses the existing AceIt UI, which now transparently powers the interview with the new AI engine.

1. **Start the Backend Server**
   Ensure your backend is running on port 8000:
   ```powershell
   cd D:\AceIt\aceit_backend
   python -m uvicorn main:app --reload --port 8000
   ```
   *(Note: Ensure `GEMINI_API_KEY` is set in your `.env` file)*

2. **Start the Frontend**
   In a separate terminal:
   ```powershell
   cd D:\AceIt\aceit-frontend
   npm run dev
   ```

3. **Open Browser**
   - Go to: [http://localhost:5173/interview](http://localhost:5173/interview) (or the interview start page).
   - Click **"Start Interview"**.
   - **Text Mode**: Type answers and submit.
   - **Audio Mode**: Use the microphone button to record answers.
   
   *Result*: The AI will ask adaptive questions based on your responses using the new SimInterview logic.

---

## Option 2: Run via Backend Verification Script
To test the engine purely from the backend (useful for debugging):

1. **Ensure Backend is Running** (see Step 1 above).

2. **Run the Test Script**
   This script simulates a full interview flow (Start -> Answer -> Next Question).
   ```powershell
   cd D:\AceIt\aceit_backend
   python scripts/test_sim_interview.py
   ```
   *Or for the legacy frontend flow compatibility check:*
   ```powershell
   python scripts/test_legacy_net.py
   ```

## Troubleshooting
- **404 Not Found**: Restart the backend server ensures the new routes are loaded.
- **LLM Errors**: Check your `GEMINI_API_KEY` in `.env`.
- **Audio Issues**: Ensure `ffmpeg` is installed for Whisper, or the system will fallback to mock transcription (safe mode).
