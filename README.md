# 🎙️ AI Voice Note Summarizer

A Python project to record voice notes, transcribe them, and automatically generate summaries, TODO lists, and tags using AssemblyAI.

---

## Features
- Record audio in the browser (Streamlit)
- Automatic speech-to-text transcription (AssemblyAI)
- AI-generated summaries and TODO items
- Keyword extraction for tags

---

## Tech Stack
- **Backend:** FastAPI + Uvicorn
- **Frontend:** Streamlit + streamlit-audiorecorder
- **Database:** SQLite
- **AI:** AssemblyAI (speech-to-text, summarization)
- **Infra:** Python + dotenv

---

## Installation

1. **Clone the repo**
    ```bash
    git clone https://github.com/<your-username>/voice-note-summarizer.git
    cd voice-note-summarizer
    ```

2. **Create a virtual environment**
    ```bash
    python -m venv venv
    source venv/bin/activate   # Mac/Linux
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**
    Create a `.env` file in the root directory:
    ```env
    ASSEMBLYAI_API_KEY=your_assemblyai_api_key
    DB_PATH=notes.db
    ```

---

## Running the Project

Run the provided script from the project root:

```bash
./run.sh
```

---

## Project Structure
```
voice-note-summarizer/
│── backend/
│   ├── main.py
│   ├── database.py
│   ├── assemblyai_service.py
│── frontend/
│   └── app.py
│── config.py
│── requirements.txt
│── README.md
│── .env.example
```
