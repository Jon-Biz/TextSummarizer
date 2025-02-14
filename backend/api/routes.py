from fastapi import APIRouter, File, UploadFile
from models import Settings
from services import TranscriptionService, SummarizationService
from config import load_settings, save_settings
from typing import List, Dict

from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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"
)

# Load initial settings
settings = load_settings()
system_prompt = settings.system_prompt

# Initialize services
transcription_service = TranscriptionService()
summarization_service = SummarizationService(client, system_prompt)

# Create router
router = APIRouter()

@router.get("/data")
def get_data(
    transcripts_service=transcription_service, 
    summaries_service=summarization_service
) -> Dict[str, List]:
    """Retrieve all transcripts, summaries, and settings."""
    transcripts = transcripts_service.load_all()
    summaries = summaries_service.load_all()
    
    return {
        "transcripts": [transcript.dict() for transcript in transcripts],
        "summaries": [summary.dict() for summary in summaries],
        "settings": settings.dict(),
    }

@router.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):
    """Transcribe an uploaded audio file."""
    return transcription_service.transcribe(file)

@router.post("/summarize")
async def summarize(transcript: str):
    """Generate a summary for a given transcript."""
    return summarization_service.generate_summary(transcript)

@router.get("/settings")
def get_settings():
    """Retrieve current application settings."""
    return settings.dict()

@router.put("/settings")
def update_settings(settings_update: Settings):
    """Update application settings."""
    global settings, system_prompt
    settings = settings_update
    system_prompt = settings_update.system_prompt

    # Save settings to file
    save_settings(settings_update)

    return {"message": "Settings updated successfully"}