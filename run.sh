#!/bin/bash

# Voice Note Summarizer - Run Script
# This script starts both the FastAPI backend and Streamlit frontend
# Uses AssemblyAI for speech-to-text transcription and text processing
#
# Exit immediately if a command exits with a non-zero status.
set -e

# Navigate to the project root
PROJECT_ROOT="$(dirname "$0")"
cd "$PROJECT_ROOT"

echo "Activating virtual environment..."
source venv/bin/activate

# Check for required environment variables
if [ -z "$ASSEMBLYAI_API_KEY" ]; then
    echo "⚠️  WARNING: ASSEMBLYAI_API_KEY environment variable is not set."
    echo "   Please create a .env file with your AssemblyAI API key."
    echo "   Example: ASSEMBLYAI_API_KEY=your_api_key_here"
fi

# Debugging information
echo "--- DEBUG INFO START ---"
echo "Which python: $(which python)"
echo "Python sys.path:"
python -c "import sys; [print(p) for p in sys.path]"
echo "PYTHONPATH: $PYTHONPATH"
echo "--- DEBUG INFO END ---"

echo "Verifying audiorecorder installation..."
/Users/bastianhojbjerre/Development/voice-note-summarizer/venv/bin/python3 -c "import audiorecorder; print('audiorecorder is installed.')" || echo "audiorecorder is NOT installed or cannot be imported."

echo "Verifying AssemblyAI installation..."
/Users/bastianhojbjerre/Development/voice-note-summarizer/venv/bin/python3 -c "import assemblyai; print('AssemblyAI is installed.')" || echo "AssemblyAI is NOT installed or cannot be imported."

echo "Installing/updating dependencies..."
/Users/bastianhojbjerre/Development/voice-note-summarizer/venv/bin/python3 -m pip install -r requirements.txt

echo "Starting FastAPI backend (http://127.0.0.1:8000)..."
(cd backend && PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH" uvicorn main:app --reload --host 127.0.0.1 --port 8000) &
BACKEND_PID=$!

echo "Waiting for backend to start..."
sleep 5 # Give the backend a few seconds to start up

echo "Starting Streamlit frontend (http://localhost:8501)..."
echo "🎙️  Voice Note Summarizer is starting up..."
echo "   Backend: http://127.0.0.1:8000"
echo "   Frontend: http://localhost:8501"
echo "   Using AssemblyAI for transcription and text processing"
echo ""
PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH" streamlit run frontend/app.py

# Ensure backend process is killed when the script exits
trap "kill $BACKEND_PID" EXIT
