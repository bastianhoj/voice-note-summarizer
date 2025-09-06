# 🎙️ AI Voice Note Summarizer

A simple AI project where you can record voice notes, transcribe them into text, and automatically generate summaries, TODO lists, and tags.  
Built with **FastAPI**, **Streamlit**, **AssemblyAI**, and **SQLite**.  

---

## 🚀 Features
- 🎤 Record audio directly in the browser (Streamlit).
- ✍️ Automatic speech-to-text transcription.
- 📝 AI-generated summaries, TODO items, and keywords.
- 💾 Store notes in an SQLite database.
- 📚 Browse all saved notes in the UI.
- ⚡ Built with Python and easy to extend (e.g., Azure, alternative AI models).

---

## 📦 Tech Stack
- **Backend:** FastAPI + Uvicorn  
- **Frontend:** Streamlit (+ `streamlit-audiorecorder`)  
- **Database:** SQLite  
- **AI Models:** AssemblyAI (speech-to-text and text processing)  
- **Infra:** Python + dotenv  

---

## 🛠️ Installation

1. **Clone the repo**
```bash
git clone https://github.com/<your-username>/voice-note-summarizer.git
cd voice-note-summarizer
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
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
API_HOST=127.0.0.1
API_PORT=8000
```

---

## ▶️ Running the Project

### Backend (FastAPI)
```bash
cd backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
- API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Frontend (Streamlit)
```bash
cd frontend
streamlit run app.py
```
- UI: [http://localhost:8501](http://localhost:8501)

---

## 📂 Project Structure (planned)
```
voice-note-summarizer/
│── backend/
│   ├── main.py          # FastAPI app
│   ├── database.py      # SQLite integration
│   └── ...
│── frontend/
│   └── app.py           # Streamlit UI
│── config.py            # Loads .env variables
│── requirements.txt
│── tasks.md             # Step-by-step dev plan
│── README.md
│── .env.example
```

---

## ✅ Roadmap
See [tasks.md](./tasks.md) for detailed step-by-step development tasks.  
This file is structured so that **Cursor** (or other AI coding assistants) can follow along and implement features incrementally.  

---

## 🤝 Contributing
PRs, issues, and feature requests are welcome!  

---

## 📜 License
MIT
