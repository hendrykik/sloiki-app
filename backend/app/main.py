from fastapi import FastAPI
from app.api.main import api_router

app = FastAPI(title="Sloiki Backend")
app.include_router(api_router)
