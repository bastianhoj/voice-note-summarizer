# AI Voice Note Summarizer – Project Plan

## 0. GitHub Setup
- [x] Create a new GitHub repo: `voice-note-summarizer`.
- [x] Initialize repo with `README.md` and `.gitignore (Python)`.
- [x] Clone repo locally.
- [x] Commit and push initial files (`README.md`, `tasks.md`).

## 1. Project Setup
- [x] Create virtual environment.
- [x] Add `requirements.txt` with:
  - fastapi
  - uvicorn
  - streamlit
  - assemblyai
  - python-dotenv
  - sqlite-utils
  - requests
  - streamlit-audiorecorder
- [x] Install dependencies.
- [x] Add `.env` with AssemblyAI API key. (Note: Created `sample.env` instead of `.env.example`)
- [x] Create `config.py` to load environment variables.

## 2. Backend (FastAPI)
- [x] Create folder `backend/` with `main.py`.
- [x] Setup FastAPI app with `/health` endpoint.
- [x] Add `/transcribe`:
  - Accept audio file upload.
  - Use AssemblyAI to transcribe.
  - Return transcription text.
- [x] Add `/summarize`:
  - Accept transcription text.
  - Use AssemblyAI service to generate:
    - Short summary
    - TODO list
    - Tags/keywords
  - Return JSON response.

## 3. Database (SQLite)
- [x] Create `database.py` helper.
- [x] Initialize `notes.db` with table:  
  `id, text, summary, todos, tags, created_at`.
- [x] Add endpoints:
  - `POST /notes` → save note
  - `GET /notes` → list all notes
  - `GET /notes/{id}` → get single note

## 4. Frontend (Streamlit)
- [x] Create folder `frontend/` with `app.py`.
- [x] Add Streamlit UI with title "AI Voice Note Summarizer".
- [x] Add `streamlit-audiorecorder` to record voice directly.
- [x] Save audio to temp file and send to backend `/transcribe`.
- [x] Send transcription to `/summarize`.
- [x] Display:
  - Raw transcription
  - AI-generated summary
  - TODOs
  - Tags
- [x] Add button "Save Note" → call backend `/notes`.
- [x] Add sidebar with "All Notes" → fetch from `/notes`.

## 5. GitHub Workflow
- [ ] Commit backend MVP (`