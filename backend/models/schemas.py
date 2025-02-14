from pydantic import BaseModel

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