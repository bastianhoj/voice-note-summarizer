import assemblyai as aai
import os
import sys
from typing import Dict, List, Any

# Get the absolute path of the project root dynamically
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from config import ASSEMBLYAI_API_KEY

class AssemblyAIService:
    def __init__(self):
        """Initialize AssemblyAI service with API key."""
        if not ASSEMBLYAI_API_KEY:
            raise ValueError("ASSEMBLYAI_API_KEY not found in environment variables")
        
        aai.settings.api_key = ASSEMBLYAI_API_KEY
        self.transcriber = aai.Transcriber()
    
    def transcribe_audio_bytes(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio bytes to text using AssemblyAI.
        
        Args:
            audio_bytes: Audio file content as bytes
            
        Returns:
            Transcribed text
        """
        try:
            # Create a temporary file to store the audio bytes
            import tempfile
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_file.write(audio_bytes)
                temp_file_path = temp_file.name
            
            # Transcribe the audio file
            transcript = self.transcriber.transcribe(temp_file_path)
            
            # Clean up the temporary file
            os.unlink(temp_file_path)
            
            if transcript.status == aai.TranscriptStatus.error:
                raise Exception(f"Transcription failed: {transcript.error}")
            
            return transcript.text
            
        except Exception as e:
            raise Exception(f"Error transcribing audio: {str(e)}")
    
    def summarize_text(self, text: str) -> Dict[str, Any]:
        """
        Generate summary, todos, and tags from text using AssemblyAI's summarization.
        
        Args:
            text: Input text to summarize
            
        Returns:
            Dictionary containing summary, todos, and tags
        """
        try:
            # For now, we'll use a simple approach since AssemblyAI doesn't have
            # built-in summarization like GPT. We'll create a basic summary
            # and extract potential todos and tags from the text.
            
            # Basic summarization - take first few sentences
            sentences = text.split('. ')
            summary = '. '.join(sentences[:3]) + '.' if len(sentences) > 3 else text
            
            # Extract potential todos (lines starting with action words)
            todos = []
            action_words = ['todo', 'need to', 'should', 'must', 'have to', 'remember to', 'don\'t forget']
            lines = text.split('\n')
            for line in lines:
                line_lower = line.lower().strip()
                if any(word in line_lower for word in action_words):
                    todos.append(line.strip())
            
            # If no todos found, create a generic one
            if not todos:
                todos = ["Review and organize this note"]
            
            # Extract potential tags (simple keyword extraction)
            tags = []
            common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
            
            words = text.lower().split()
            word_freq = {}
            for word in words:
                word = word.strip('.,!?;:"()[]{}')
                if len(word) > 3 and word not in common_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
            
            # Get top 5 most frequent words as tags
            tags = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
            tags = [tag[0] for tag in tags]
            
            # If no tags found, add a generic one
            if not tags:
                tags = ["note"]
            
            return {
                "summary": summary,
                "todos": todos,
                "tags": tags
            }
            
        except Exception as e:
            raise Exception(f"Error summarizing text: {str(e)}")

# Global instance
_assemblyai_service = None

def get_assemblyai_service() -> AssemblyAIService:
    """Get the global AssemblyAI service instance."""
    global _assemblyai_service
    if _assemblyai_service is None:
        _assemblyai_service = AssemblyAIService()
    return _assemblyai_service
