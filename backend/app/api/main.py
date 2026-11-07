from turtle import title

from fastapi import APIRouter

from app.api.routes import users
from app.api.routes import health

api_router = APIRouter()
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(health.router, prefix='/health', tags=['health'])
