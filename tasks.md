# AI Voice Note Summarizer – Project Plan

## 0. GitHub Setup
- [ ] Create a new GitHub repo: `voice-note-summarizer`.
- [ ] Initialize repo with `README.md` and `.gitignore (Python)`.
- [ ] Clone repo locally.
- [ ] Commit and push initial files (`README.md`, `tasks.md`).

## 1. Project Setup
- [ ] Create virtual environment.
- [ ] Add `requirements.txt` with:
  - fastapi
  - uvicorn
  - streamlit
  - openai
  - python-dotenv
  - sqlite-utils
  - requests
  - streamlit-audiorecorder
- [ ] Install dependencies.
- [ ] Add `.env` with OpenAI API key.
- [ ] Create `config.py` to load environment variables.

## 2. Backend (FastAPI)
- [ ] Create folder `backend/` with `main.py`.
- [ ] Setup FastAPI app with `/health` endpoint.
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
