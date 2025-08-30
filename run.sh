#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the project root
cd "$(dirname "$0")"

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting FastAPI backend (http://127.0.0.1:8000)..."
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 5 # Give the backend a few seconds to start up

echo "Starting Streamlit frontend (http://localhost:8501)..."
cd frontend
streamlit run app.py

# Ensure backend process is killed when the script exits
trap "kill $BACKEND_PID" EXIT
