from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .settings import (
    CORS_ORIGINS,
    DATA_DIR,
    SETTINGS_FILE,
    load_settings,
    save_settings,
)

def configure_cors(app: FastAPI) -> None:
    """Configure CORS middleware for the FastAPI application."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

__all__ = [
    'configure_cors',
    'DATA_DIR',
    'SETTINGS_FILE',
    'load_settings',
    'save_settings',
]