#!/bin/bash

# Horizon App Runner Script
# This script starts both backend and frontend servers

echo "Starting Horizon Application..."
echo ""

# Check if PostgreSQL is running
export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"
if ! pg_isready -U horizon -d horizon > /dev/null 2>&1; then
    echo "Starting PostgreSQL..."
    brew services start postgresql@15
    sleep 3
fi

# Start Backend
echo "Starting Backend Server..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 2

# Start Frontend
echo "Starting Frontend Server..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "=========================================="
echo "Horizon Application Started!"
echo "=========================================="
echo "Backend API:  http://localhost:8000"
echo "API Docs:     http://localhost:8000/docs"
echo "Frontend:     http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop all servers"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""

# Wait for user interrupt
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT TERM
wait

