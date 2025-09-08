# backend/assemblyai_service.py

import assemblyai as aai
import os
import sys
import tempfile
from typing import Dict, Any

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config import ASSEMBLYAI_API_KEY

class AssemblyAIService:
    def __init__(self):
        if not ASSEMBLYAI_API_KEY:
            raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")

        # Initialize the Transcriber
        aai.settings.api_key = ASSEMBLYAI_API_KEY
        self.transcriber = aai.Transcriber()

    def transcribe_and_summarize_audio(self, audio_bytes: bytes) -> Dict[str, Any]:
        try:
            # Save audio to temp file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name

            # Request summarization from AssemblyAI
            transcript = self.transcriber.transcribe(
                temp_file_path,
                config=aai.TranscriptionConfig(summarization=True, summary_model="informative", summary_type="bullets")
            )

            os.unlink(temp_file_path)

            if transcript.error:
                raise Exception(f"Transcription failed: {transcript.error}")

            summary = transcript.summary if transcript.summary else "No summary available"
            # Improved TODO extraction: sentences starting with action verbs
            import re
            action_verbs = [
                "review", "check", "analyze", "consider", "explore", "investigate", "assess", "monitor", "update", "plan", "research", "learn", "understand", "discuss", "note"
            ]
            todos = []
            for line in summary.split("\n"):
                line = line.strip()
                if line:
                    first_word = re.split(r'\W+', line.lower())[0]
                    if first_word in action_verbs:
                        todos.append(line)
            if not todos:
                todos = ["Review note"]
            # Dynamic tag extraction from transcript (no hardcoded keywords)
            import re
            stopwords = set(["the", "is", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with", "at", "by", "from", "as", "it", "this", "that", "these", "those", "are", "was", "were", "be", "been", "has", "have", "had", "but", "not", "do", "does", "did", "so", "if", "then", "than", "too", "very", "can", "will", "just", "about", "into", "out", "up", "down", "over", "under", "again", "more", "most", "some", "such", "no", "nor", "only", "own", "same", "s", "t", "d", "ll", "m", "o", "re", "ve", "y"])
            words = re.findall(r'\b\w{4,}\b', transcript.text.lower())
            keywords = [w for w in words if w not in stopwords]
            # Get most frequent keywords
            from collections import Counter
            freq = Counter(keywords)
            tags = [w for w, _ in freq.most_common(5)]
            tags = list(dict.fromkeys(tags))  # Remove duplicates, preserve order

            return {
                "text": transcript.text,
                "summary": summary,
                "todos": todos,
                "tags": tags
            }

        except Exception as e:
            raise Exception(f"Error transcribing/summarizing audio: {str(e)}")

# Singleton pattern for AssemblyAIService
_assemblyai_service_instance = None

def get_assemblyai_service():
    global _assemblyai_service_instance
    if _assemblyai_service_instance is None:
        _assemblyai_service_instance = AssemblyAIService()
    return _assemblyai_service_instance
