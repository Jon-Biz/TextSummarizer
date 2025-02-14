from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from faster_whisper import WhisperModel
import openai
import os
import uuid
import re
from typing import List
from pydantic import BaseModel

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
app = FastAPI()

from openai import OpenAI

client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key="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"
)

# Load settings from file
settings_file = "settings.txt"
if os.path.exists(settings_file):
    with open(settings_file, "r") as f:
        settings = f.read().splitlines()
    system_prompt = settings[0]
    openai_api_key = settings[1]
    openai_endpoint = settings[2]
else:
    system_prompt = "Summarize the following text. Respond with just the summary:"
    openai_api_key = ""
    openai_endpoint = ""

openai.api_key = openai_api_key

# Set up data directory
data_dir = "data"
os.makedirs(data_dir, exist_ok=True)

# CORS configuration
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class Transcript(BaseModel):
    id: str
    title: str
    content: str

class Summary(BaseModel):
    id: str
    title: str
    content: str

class Settings(BaseModel):
    system_prompt: str
    openai_api_key: str
    openai_endpoint: str

# Helper functions
def load_data() -> tuple[List[Transcript], List[Summary], Settings]:
    transcripts = []
    summaries = []

    for file_name in os.listdir(data_dir):
        if file_name.endswith(".txt"):
            transcript_path = os.path.join(data_dir, file_name)
            with open(transcript_path, "r") as f:
                transcript_content = f.read()
            transcript = Transcript(
                id=file_name.split(".")[0],
                title="",
                content=transcript_content,
            )
            transcripts.append(transcript)
        elif file_name.endswith(".md"):
            summary_path = os.path.join(data_dir, file_name)
            with open(summary_path, "r") as f:
                summary_content = f.read()
            title = summary_content.split("\n")[0][2:]
            content = "\n".join(summary_content.split("\n")[1:])
            summary = Summary(
                id=file_name.split(".")[0],
                title=title,
                content=content,
            )
            summaries.append(summary)

    return transcripts, summaries, Settings(
        system_prompt=system_prompt,
        openai_api_key=openai_api_key,
        openai_endpoint=openai_endpoint,
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
    # Generate unique filename
    unique_filename = f"{uuid.uuid4().hex}"
    file_extension = os.path.splitext(file.filename)[1]
    file_path = os.path.join(data_dir, f"{unique_filename}{file_extension}")

    # Transcribe audio
    try:
        print(f"Transcribing audio: {file.filename}")

        model = WhisperModel("large-v3", device="cpu", compute_type="float32")
        segments, info = model.transcribe(file.file, initial_prompt=None, word_timestamps=False)

        print(f"Transcription info: {info}")
        print(f"Transcription segments: {segments}")

        transcript = ""
        for segment in segments:
            print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
            transcript += segment.text + "\n"

        # Save transcript to file
        with open(file_path, "w") as f:
            f.write(transcript)

        print(f"Transcript saved to: {file_path}")
        print(f"Transcript: {transcript}")

        return {"transcript": transcript, "transcript_path": file_path}

    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return {"error": str(e)}

def sanitize_filename(filename):
    # Remove or replace characters that are not allowed in filenames
    sanitized = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Truncate to a reasonable length
    return sanitized[:255]

@app.post("/api/summarize")
async def summarize(transcript: str):
    print(f"transcript: {transcript}")

    # Summarize transcript with OpenAI
    response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[
        {
        "role": "user",
        "content": f"{system_prompt}\n\n{transcript}"
        }
    ]
    )

    summary = response.choices[0].message.content
    print(f"Generated summary: {summary}")

    # Get title for summary
    title_response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[
        {
        "role": "user",
        "content": f"Generate a short, descriptive title for this text:\n\n{transcript}"
        }
    ]
    )

    title = title_response.choices[0].message.content
    print(f"Generated title: {title}")

    # Sanitize title for filename
    sanitized_title = sanitize_filename(title)
    
    # Save summary to file
    summary_path = os.path.join(data_dir, f"{sanitized_title}.md")
    try:
        with open(summary_path, "w") as f:
            f.write(f"# {title}\n\n{summary}")
        print(f"Summary saved to: {summary_path}")
    except Exception as e:
        print(f"Error saving summary: {e}")
        # Fallback to a generic filename if sanitization fails
        summary_path = os.path.join(data_dir, f"summary_{uuid.uuid4().hex}.md")
        with open(summary_path, "w") as f:
            f.write(f"# {title}\n\n{summary}")
        print(f"Summary saved to fallback path: {summary_path}")

    return {"summary_path": summary_path}

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
    with open(settings_file, "w") as f:
        f.write(f"{system_prompt}\n{openai_api_key}\n{openai_endpoint}")

    return {"message": "Settings updated successfully"}
