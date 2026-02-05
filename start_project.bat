@echo off
echo ===================================================
echo     AceIt AI Interview Platform - Startup Script
echo ===================================================
echo.

:: 1. Start Backend
echo Starting Backend Server (Port 8000)...
start "AceIt Backend" cmd /k "cd /d D:\AceIt\aceit_backend && venv\Scripts\activate && python -m uvicorn main:app --reload --port 8000"

:: 2. Start Frontend
echo Starting Frontend (Vite)...
start "AceIt Frontend" cmd /k "cd /d D:\AceIt\aceit-frontend && npm run dev"

echo.
echo ===================================================
echo     Servers are launching in separate windows!
echo     Backend: http://localhost:8000/docs
echo     Frontend: http://localhost:5173
echo ===================================================
echo.
pause
