import os
from typing import List
from models import Transcript
from config import DATA_DIR

class TranscriptRepository:
    """Repository for handling transcript file operations."""
    
    @staticmethod
    def load_all() -> List[Transcript]:
        """Load all transcripts from the data directory."""
        transcripts = []
        for file_name in os.listdir(DATA_DIR):
            if file_name.endswith(".txt"):
                transcript_path = os.path.join(DATA_DIR, file_name)
                try:
                    with open(transcript_path, "r") as f:
                        transcript_content = f.read()
                    transcript = Transcript(
                        id=file_name.split(".")[0],
                        title="",
                        content=transcript_content,
                    )
                    transcripts.append(transcript)
                except Exception as e:
                    print(f"Error loading transcript {file_name}: {e}")
        return transcripts

    @staticmethod
    def save(file_id: str, content: str, extension: str = ".txt") -> str:
        """Save a transcript to file and return the file path."""
        file_path = os.path.join(DATA_DIR, f"{file_id}{extension}")
        with open(file_path, "w") as f:
            f.write(content)
        return file_path