import sqlite3
import sys
import os
import json
from contextlib import contextmanager
from typing import List, Dict, Any

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # Corrected path
sys.path.insert(0, PROJECT_ROOT)

from config import DB_PATH

@contextmanager
def get_db_connection():
    """Create a new database connection for each request to avoid threading issues."""
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # This allows accessing columns by name
    try:
        yield conn
    finally:
        conn.close()

def get_db():
    """Get a database connection - this creates a new connection each time."""
    return get_db_connection()

def init_db():
    """Initialize the database and create tables if they don't exist."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id TEXT PRIMARY KEY,
                text TEXT NOT NULL,
                summary TEXT NOT NULL,
                todos TEXT NOT NULL,
                tags TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.commit()

def insert_note(note_data: Dict[str, Any]):
    """Insert a note into the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notes (id, text, summary, todos, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            note_data["id"],
            note_data["text"],
            note_data["summary"],
            note_data["todos"],
            note_data["tags"],
            note_data["created_at"]
        ))
        conn.commit()

def get_all_notes() -> List[Dict[str, Any]]:
    """Get all notes from the database."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
        rows = cursor.fetchall()
        notes = []
        for row in rows:
            note_data = dict(row)
            note_data["todos"] = json.loads(note_data["todos"])
            note_data["tags"] = json.loads(note_data["tags"])
            notes.append(note_data)
        return notes

def get_note_by_id(note_id: str) -> Dict[str, Any]:
    """Get a specific note by ID."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
        row = cursor.fetchone()
        if row:
            note_data = dict(row)
            note_data["todos"] = json.loads(note_data["todos"])
            note_data["tags"] = json.loads(note_data["tags"])
            return note_data
        return None
