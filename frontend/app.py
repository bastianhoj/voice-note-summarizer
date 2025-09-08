import streamlit as st
import requests
from audiorecorder import audiorecorder
import io
import sys
import os

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

# FastAPI backend URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("AI Voice Note Summarizer")

st.write("Frontend is running!")

# Record audio
audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    # Send audio to backend
    if st.button("Process Audio"):
        with st.spinner("Processing audio (transcription + summarization)..."):
            audio_file = io.BytesIO(audio.export().read())
            files = {"audio_file": ("audio.wav", audio_file, "audio/wav")}
            response = requests.post(f"{BACKEND_URL}/process_audio", files=files)

            if response.status_code == 200:
                note = response.json()
                st.session_state.current_note = note

                st.subheader("Raw Transcription:")
                st.write(note["text"])

                st.subheader("AI-Generated Summary:")
                st.write(note["summary"])

                st.subheader("TODOs:")
                for todo in note["todos"]:
                    st.write(f"- {todo}")

                st.subheader("Tags:")
                st.write(", ".join(note["tags"]))

                st.success("Note processed and saved to DB!")
            else:
                st.error(f"Error processing audio: {response.text}")

# Sidebar to display all notes
st.sidebar.title("All Notes")

if st.sidebar.button("New Note"):
    st.session_state.current_note = None
    st.rerun()

try:
    response = requests.get(f"{BACKEND_URL}/notes")
    if response.status_code == 200:
        all_notes = response.json()
        for note in all_notes:
            if st.sidebar.button(f"{note['created_at'].split('T')[0]} - {note['summary'][:30]}..."):
                st.session_state.current_note = note
                st.rerun()
    else:
        st.sidebar.error(f"Error fetching notes: {response.text}")
except requests.exceptions.ConnectionError:
    st.sidebar.error("Could not connect to backend. Please ensure it is running.")

# Display selected note
if st.session_state.get("current_note"):
    note = st.session_state.current_note
    st.subheader("Selected Note")
    if 'created_at' in note:
        st.write(f"**Created At:** {note['created_at']}")
    st.subheader("Raw Transcription:")
    st.write(note["text"])
    st.subheader("AI-Generated Summary:")
    st.write(note["summary"])
    st.subheader("TODOs:")
    for todo in note["todos"]:
        st.write(f"- {todo}")
    st.subheader("Tags:")
    st.write(", ".join(note["tags"]))
