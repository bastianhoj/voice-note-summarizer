#!/bin/bash

# Voice Note Summarizer - Run Script
# Starts FastAPI backend and Streamlit frontend
# Uses AssemblyAI for speech-to-text transcription and text processing
#
# Exit immediately if a command exits with a non-zero status
set -e

# Navigate to the project root
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

echo "Activating virtual environment..."
source venv/bin/activate

# Check for required environment variables
if [ -z "$ASSEMBLYAI_API_KEY" ]; then
    echo "⚠️  WARNING: ASSEMBLYAI_API_KEY environment variable is not set."
    echo "   Please create a .env file with your AssemblyAI API key."
    echo "   Example: ASSEMBLYAI_API_KEY=your_api_key_here"
fi

# Debug info
echo "--- DEBUG INFO START ---"
echo "Python: $(which python)"
python -c "import sys; [print(p) for p in sys.path]"
echo "PYTHONPATH: $PYTHONPATH"
echo "--- DEBUG INFO END ---"

# Verify dependencies
echo "Verifying installations..."
python -c "import audiorecorder; print('audiorecorder OK')" || echo "audiorecorder NOT installed"
python -c "import assemblyai; print('AssemblyAI OK')" || echo "AssemblyAI NOT installed"

# Install/update dependencies
echo "Installing/updating requirements..."
python -m pip install -r requirements.txt

# Ensure logs folder exists
mkdir -p "$PROJECT_ROOT/logs"
BACKEND_LOG="$PROJECT_ROOT/logs/backend.log"

# Start FastAPI backend
echo "Starting FastAPI backend (http://127.0.0.1:8000)..."
(cd backend && PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH" uvicorn main:app --reload --host 127.0.0.1 --port 8000 > "$BACKEND_LOG" 2>&1) &
BACKEND_PID=$!

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 5

# Optionally tail backend log
echo "Backend log tail (press Ctrl+C to stop):"
tail -f "$BACKEND_LOG" &

# Start Streamlit frontend
echo "Starting Streamlit frontend (http://localhost:8501)..."
echo "🎙️  Voice Note Summarizer is starting..."
echo "   Backend: http://127.0.0.1:8000"
echo "   Frontend: http://localhost:8501"
echo ""
PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH" streamlit run frontend/app.py

# Ensure backend process is killed when script exits
trap "kill $BACKEND_PID" EXIT
