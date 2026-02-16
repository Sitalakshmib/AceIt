#!/bin/bash

# Define colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Starting AceIt System...${NC}"

# Function to kill background processes on exit
cleanup() {
    echo -e "\n${RED}Stopping servers...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

# Trap SIGINT (Ctrl+C)
trap cleanup SIGINT

# 1. Start Backend
echo -e "${GREEN}Starting Backend...${NC}"
cd aceit_backend

# Check if venv exists and activate
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo -e "${RED}Virtual environment not found in aceit_backend/.venv${NC}"
    echo "Attempting to create one..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Always check requirements
echo "Checking requirements..."
pip install -r requirements.txt

# Run backend in background
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo -e "Backend running with PID: $BACKEND_PID"

# Return to root
cd ..

# 2. Start Frontend
echo -e "${GREEN}Starting Frontend...${NC}"
cd aceit-frontend

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

# Run frontend
npm run dev &
FRONTEND_PID=$!
echo -e "Frontend running with PID: $FRONTEND_PID"

# Wait for both processes
wait