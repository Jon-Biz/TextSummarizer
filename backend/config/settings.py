import os
from typing import List
from models import Settings

# Environment variables
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# Settings file configuration
SETTINGS_FILE = "settings.txt"
DATA_DIR = "data"

# CORS configuration
CORS_ORIGINS: List[str] = [
    "http://localhost:5173",
    "http://localhost:3000",
]

# Default settings
DEFAULT_SYSTEM_PROMPT = "Summarize the following text. Respond with just the summary:"
DEFAULT_OPENAI_API_KEY = ""
DEFAULT_OPENAI_ENDPOINT = ""

def load_settings() -> Settings:
    """Load settings from file or return defaults."""
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            settings = f.read().splitlines()
        return Settings(
            system_prompt=settings[0],
            openai_api_key=settings[1],
            openai_endpoint=settings[2]
        )
    return Settings(
        system_prompt=DEFAULT_SYSTEM_PROMPT,
        openai_api_key=DEFAULT_OPENAI_API_KEY,
        openai_endpoint=DEFAULT_OPENAI_ENDPOINT
    )

def save_settings(settings: Settings) -> None:
    """Save settings to file."""
    with open(SETTINGS_FILE, "w") as f:
        f.write(f"{settings.system_prompt}\n{settings.openai_api_key}\n{settings.openai_endpoint}")

# Initialize data directory
os.makedirs(DATA_DIR, exist_ok=True)