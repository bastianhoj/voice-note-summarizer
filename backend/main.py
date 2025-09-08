from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import uuid
import json
from datetime import datetime
import sys
import os

# Project root path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from database import init_db, insert_note, get_all_notes, get_note_by_id
from assemblyai_service import get_assemblyai_service

app = FastAPI()

# Initialize DB
@app.on_event("startup")
async def startup_event():
    init_db()

class NoteOut(BaseModel):
    id: str
    text: str
    summary: str
    todos: List[str]
    tags: List[str]
    created_at: datetime

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/process_audio", response_model=NoteOut)
async def process_audio(audio_file: UploadFile = File(...)):
    try:
        audio_bytes = await audio_file.read()
        assemblyai = get_assemblyai_service()
        result = assemblyai.transcribe_and_summarize_audio(audio_bytes)

        note_id = str(uuid.uuid4())
        created_at = datetime.now().isoformat()
        note_data = {
            "id": note_id,
            "text": result["text"],
            "summary": result["summary"],
            "todos": json.dumps(result["todos"]),
            "tags": json.dumps(result["tags"]),
            "created_at": created_at,
        }

        insert_note(note_data)

        return NoteOut(
            id=note_id,
            text=result["text"],
            summary=result["summary"],
            todos=result["todos"],
            tags=result["tags"],
            created_at=created_at,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@app.get("/notes", response_model=List[NoteOut])
async def get_all_notes_endpoint():
    notes_data = get_all_notes()
    notes = [NoteOut(
        id=note["id"],
        text=note["text"],
        summary=note["summary"],
        todos=json.loads(note["todos"]),
        tags=json.loads(note["tags"]),
        created_at=note["created_at"]
    ) for note in notes_data]
    return notes

@app.get("/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: str):
    note_data = get_note_by_id(note_id)
    if not note_data:
        raise HTTPException(status_code=404, detail="Note not found")
    return NoteOut(
        id=note_data["id"],
        text=note_data["text"],
        summary=note_data["summary"],
        todos=json.loads(note_data["todos"]),
        tags=json.loads(note_data["tags"]),
        created_at=note_data["created_at"]
    )
