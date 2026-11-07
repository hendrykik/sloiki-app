from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.handlers.database import get_session

router = APIRouter()

db_dependency = Annotated[Session, Depends(get_session)]

@router.get("/user", status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    results = db.query()
    return results
