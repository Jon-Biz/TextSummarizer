"""
Main application module for the TextSummarizer backend.
This module initializes the FastAPI application and includes the API router.
"""

from fastapi import FastAPI
from config import configure_cors
from api import router

# Initialize FastAPI application
app = FastAPI(
    title="TextSummarizer API",
    description="API for transcribing audio and summarizing text",
    version="1.0.0"
)
# How fucking embarrassing. 
# This is required, because if the application halts unexpectedly,
# on subsequent restarts, FastAPI can't see the variable 'app'
# and will throw.
# refering to the variable allows it to be imported by uvicorn
print(app)

# Configure CORS
configure_cors(app)

# Include the API router
app.include_router(router, prefix="/api")

# Make the app instance available for import
__all__ = ['app']

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
