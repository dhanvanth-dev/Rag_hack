from fastapi import FastAPI
from app.api import router

app = FastAPI(
    title="HackRx Adaptive RAG System",
    version="1.0"
)

app.include_router(router, prefix="/api/v1")
