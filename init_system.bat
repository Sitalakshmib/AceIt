@echo off
echo ================================================================
echo     AceIt System Initialization Script
echo ================================================================
echo.

:: Check if virtual environment exists
echo [1/5] Checking Python virtual environment...
if exist "aceit_backend\venv\Scripts\activate.bat" (
    echo   ✅ Virtual environment found
) else (
    echo   ❌ Virtual environment not found!
    echo   Creating virtual environment...
    cd aceit_backend
    python -m venv venv
    call venv\Scripts\activate
    echo   Installing Python dependencies...
    pip install -r requirements.txt
    cd ..
)

:: Check if node_modules exists
echo.
echo [2/5] Checking Node.js dependencies...
if exist "aceit-frontend\node_modules" (
    echo   ✅ Node modules found
) else (
    echo   ❌ Node modules not found!
    echo   Installing Node.js dependencies...
    cd aceit-frontend
    npm install
    cd ..
)

:: Run system health check
echo.
echo [3/5] Running system health check...
cd aceit_backend
call venv\Scripts\activate
python check_system.py
if errorlevel 1 (
    echo.
    echo   ⚠️  System health check failed!
    echo   Please fix the issues above before starting servers.
    cd ..
    pause
    exit /b 1
)
cd ..

:: Display configuration
echo.
echo [4/5] System Configuration:
echo   📁 Project Root: %CD%
echo   🐍 Backend: aceit_backend (Port 8000)
echo   ⚛️  Frontend: aceit-frontend (Port 5173)
echo   🗄️  Database: Neon PostgreSQL (Cloud)
echo.

:: Confirm before starting
echo [5/5] Ready to start servers!
echo.
set /p CONFIRM="Start both servers now? (Y/N): "
if /i not "%CONFIRM%"=="Y" (
    echo   Cancelled by user.
    pause
    exit /b 0
)

:: Start Backend Server
echo.
echo 🚀 Starting Backend Server (Port 8000)...
start "AceIt Backend" cmd /k "cd /d %CD%\aceit_backend && call venv\Scripts\activate && uvicorn main:app --reload --port 8000"

:: Wait a moment for backend to start
timeout /t 3 /nobreak >nul

:: Start Frontend Server
echo 🚀 Starting Frontend Server (Port 5173)...
start "AceIt Frontend" cmd /k "cd /d %CD%\aceit-frontend && npm run dev"

echo.
echo ================================================================
echo     ✅ Servers are launching in separate windows!
echo ================================================================
echo.
echo   🔗 Backend API:  http://localhost:8000
echo   🔗 API Docs:     http://localhost:8000/docs
echo   🔗 Frontend:     http://localhost:5173
echo.
echo   Keep the server windows open to keep the system running.
echo   Close this window or press any key to continue...
echo.
pause
