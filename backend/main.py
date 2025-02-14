from fastapi import FastAPI
from config import configure_cors
from api import router

app = FastAPI()
__all__ = ['app']
configure_cors(app)

# Include the API router
app.include_router(router, prefix="/api")
