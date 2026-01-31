#!/bin/bash

# Start backend in background
echo "🚀 Starting Backend on port 8000..."
cd aceit_backend
.venv/bin/python main.py &
BACKEND_PID=$!

# Start frontend in background  
echo "🌐 Starting Frontend on port 5173..."
cd ../aceit-frontend
npm run dev &
FRONTEND_PID=$!

echo "✅ Both servers started!"
echo "🔗 Backend: http://localhost:8000"
echo "🔗 Frontend: http://localhost:5173"
echo "📝 Backend Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; echo '🛑 Servers stopped'" SIGINT
wait