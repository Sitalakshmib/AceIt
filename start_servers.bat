@echo off
echo 🚀 Starting AceIt Development Environment...

REM Start Backend
echo Starting Backend on Port 8001...
start "AceIt Backend" cmd /k "cd aceit_backend && call venv\Scripts\activate && uvicorn main:app --reload --port 8001"

REM Start Frontend
echo Starting Frontend on Port 5173...
start "AceIt Frontend" cmd /k "cd aceit-frontend && npm run dev"

echo.
echo ✅ Servers are launching in separate windows!
echo 🔗 Backend: http://localhost:8001
echo 🔗 Frontend: http://localhost:5173
echo.
echo Keep this window open or close it, the servers are independent.
pause
