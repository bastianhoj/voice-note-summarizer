import streamlit as st
import requests
from audiorecorder import audiorecorder
import io
import json
import sys
import os

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..")) # Corrected path
sys.path.insert(0, PROJECT_ROOT)

# Assuming your FastAPI backend is running on http://127.0.0.1:8000
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(layout="wide")
st.title("AI Voice Note Summarizer")

st.write("Frontend is running!")

audio = audiorecorder("Click to record", "Click to stop recording")

if len(audio) > 0:
    st.audio(audio.export().read(), format="audio/wav")

    # Save audio to temp file and send to backend /transcribe
    if st.button("Transcribe and Summarize"):
        with st.spinner("Transcribing audio..."):
            audio_file = io.BytesIO(audio.export().read())
            files = {"audio_file": ("audio.wav", audio_file, "audio/wav")}
            transcribe_response = requests.post(f"{BACKEND_URL}/transcribe", files=files)
            
            if transcribe_response.status_code == 200:
                transcription = transcribe_response.json()["transcription"]
                st.subheader("Raw Transcription:")
                st.write(transcription)

                with st.spinner("Summarizing transcription..."):
                    summary_response = requests.post(
                        f"{BACKEND_URL}/summarize",
                        json={"text": transcription}
                    )

                    if summary_response.status_code == 200:
                        summary_data = summary_response.json()
                        st.subheader("AI-Generated Summary:")
                        st.write(summary_data["summary"])

                        st.subheader("TODOs:")
                        for todo in summary_data["todos"]:
                            st.write(f"- {todo}")
                        
                        st.subheader("Tags:")
                        st.write(", ".join(summary_data["tags"]))

                        # Store data in session state for saving
                        st.session_state.current_note = {
                            "text": transcription,
                            "summary": summary_data["summary"],
                            "todos": summary_data["todos"],
                            "tags": summary_data["tags"]
                        }

                        if st.session_state.current_note and st.button("Save Note"):
                            with st.spinner("Saving note..."):
                                save_response = requests.post(f"{BACKEND_URL}/notes", json=st.session_state.current_note)
                                if save_response.status_code == 200:
                                    st.success("Note saved successfully!")
                                    st.session_state.current_note = None # Clear current note after saving
                                else:
                                    st.error(f"Error saving note: {save_response.text}")

                    else:
                        st.error(f"Error summarizing: {summary_response.text}")
            else:
                st.error(f"Error transcribing: {transcribe_response.text}")

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

# Display selected note details in the main area
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
