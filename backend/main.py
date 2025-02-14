from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import openai
from typing import List
from models import Transcript, Summary, Settings
from config import configure_cors, load_settings, save_settings
from repository import TranscriptRepository, SummaryRepository
from services import TranscriptionService, SummarizationService

app = FastAPI()
__all__ = ['app']
configure_cors(app)

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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"
)

# Load initial settings
settings = load_settings()
system_prompt = settings.system_prompt
openai_api_key = settings.openai_api_key
openai_endpoint = settings.openai_endpoint
openai.api_key = openai_api_key

# Initialize services
transcription_service = TranscriptionService()
summarization_service = SummarizationService(client, system_prompt)

# Helper functions
def load_data() -> tuple[List[Transcript], List[Summary], Settings]:
    """Load all data using repositories."""
    return (
        TranscriptRepository.load_all(),
        SummaryRepository.load_all(),
        Settings(
            system_prompt=system_prompt,
            openai_api_key=openai_api_key,
            openai_endpoint=openai_endpoint,
        )
    )

@app.get("/api/data")
def get_data() -> dict[str, list]:
    transcripts, summaries, settings = load_data()
    return {
        "transcripts": [transcript.dict() for transcript in transcripts],
        "summaries": [summary.dict() for summary in summaries],
        "settings": settings.dict(),
    }

@app.post("/api/transcribe")
async def transcribe(file: UploadFile = File(...)):
    return transcription_service.transcribe(file)

@app.post("/api/summarize")
async def summarize(transcript: str):
    return summarization_service.generate_summary(transcript)

@app.get("/api/settings")
def get_settings():
    _, _, settings = load_data()
    return settings.dict()

@app.put("/api/settings")
def update_settings(settings: Settings):
    global system_prompt, openai_api_key, openai_endpoint
    system_prompt = settings.system_prompt
    openai_api_key = settings.openai_api_key
    openai_endpoint = settings.openai_endpoint
    openai.api_key = openai_api_key

    # Save settings to file
    save_settings(settings)

    return {"message": "Settings updated successfully"}
