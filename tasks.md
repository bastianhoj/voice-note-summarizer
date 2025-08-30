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
  - openai
  - python-dotenv
  - sqlite-utils
  - requests
  - streamlit-audiorecorder
- [x] Install dependencies.
- [x] Add `.env` with OpenAI API key. (Note: Created `sample.env` instead of `.env.example`)
- [x] Create `config.py` to load environment variables.

## 2. Backend (FastAPI)
- [x] Create folder `backend/` with `main.py`.
- [x] Setup FastAPI app with `/health` endpoint.
- [ ] Add `/transcribe`:
  - Accept audio file upload.
  - Use OpenAI Whisper (`gpt-4o-transcribe`) to transcribe.
  - Return transcription text.
- [ ] Add `/summarize`:
  - Accept transcription text.
  - Use GPT (`gpt-4o-mini`) to generate:
    - Short summary
    - TODO list
    - Tags/keywords
  - Return JSON response.

## 3. Database (SQLite)
- [ ] Create `database.py` helper.
- [ ] Initialize `notes.db` with table:  
  `id, text, summary, todos, tags, created_at`.
- [ ] Add endpoints:
  - `POST /notes` → save note
  - `GET /notes` → list all notes
  - `GET /notes/{id}` → get single note

## 4. Frontend (Streamlit)
- [ ] Create folder `frontend/` with `app.py`.
- [ ] Add Streamlit UI with title "AI Voice Note Summarizer".
- [ ] Add `streamlit-audiorecorder` to record voice directly.
- [ ] Save audio to temp file and send to backend `/transcribe`.
- [ ] Send transcription to `/summarize`.
- [ ] Display:
  - Raw transcription
  - AI-generated summary
  - TODOs
  - Tags
- [ ] Add button "Save Note" → call backend `/notes`.
- [ ] Add sidebar with "All Notes" → fetch from `/notes`.

## 5. GitHub Workflow
- [ ] Commit backend MVP (`/transcribe` + `/summarize`) to GitHub.
- [ ] Commit database integration.
- [ ] Commit frontend Streamlit app.
- [ ] Push to `main` branch.
- [ ] (Optional) Setup GitHub Actions for tests + linting.

## 6. Extras (Optional Enhancements)
- [ ] Add endpoint `/stats` → number of notes, common tags.
- [ ] Add export button → download TODOs as `.txt`.
- [ ] Multi-language support in transcription + summary.
- [ ] Support both OpenAI and Azure Cognitive Services.
