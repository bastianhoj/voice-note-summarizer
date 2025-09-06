# backend/main.py

from fastapi import FastAPI, UploadFile, File, Body, HTTPException, Depends
from pydantic import BaseModel
import json
import uuid
from datetime import datetime
import sys
import os
from typing import Any, List

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from database import init_db, insert_note, get_all_notes, get_note_by_id
from assemblyai_service import get_assemblyai_service

app = FastAPI()

# Initialize the database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

class SummaryRequest(BaseModel):
    text: str

class SummaryResponse(BaseModel):
    summary: str
    todos: List[str]
    tags: List[str]

class NoteIn(BaseModel):
    text: str
    summary: str
    todos: List[str]
    tags: List[str]

class NoteOut(NoteIn):
    id: str
    created_at: datetime

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    # Read the audio file content
    audio_bytes = await audio_file.read()
    
    # Use AssemblyAI for transcription
    assemblyai = get_assemblyai_service()
    transcript = assemblyai.transcribe_audio_bytes(audio_bytes)
    
    return {"transcription": transcript}

@app.post("/summarize", response_model=SummaryResponse)
async def summarize_text(request: SummaryRequest):
    # Use AssemblyAI service for summarization
    assemblyai = get_assemblyai_service()
    summary_data = assemblyai.summarize_text(request.text)
    return SummaryResponse(**summary_data)

@app.post("/notes", response_model=NoteOut)
async def create_note(note: NoteIn):
    note_id = str(uuid.uuid4())
    created_at = datetime.now().isoformat()
    
    note_data = {
        "id": note_id,
        "text": note.text,
        "summary": note.summary,
        "todos": json.dumps(note.todos),
        "tags": json.dumps(note.tags),
        "created_at": created_at
    }
    insert_note(note_data)
    
    return NoteOut(id=note_id, created_at=created_at, **note.dict())

@app.get("/notes", response_model=List[NoteOut])
async def get_all_notes_endpoint():
    notes_data = get_all_notes()
    notes = []
    for note_data in notes_data:
        notes.append(NoteOut(**note_data))
    return notes

@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: str):
    note_data = get_note_by_id(note_id)
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    
    return NoteOut(**note_data)
