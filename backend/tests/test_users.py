from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models.base import Base
from app.main import app

SQL_ALCHEMY_URL = 'sqlite:///./test.db'

engine = create_engine(
    SQL_ALCHEMY_URL,
    connect_args = {'check_same_thread': False},
)

TestingSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind=engine)

def ovveride_get_db():
    db = TestingSession
    try:
        yield db
    finally:
        db.close()

# app.dependency_overrides[]
