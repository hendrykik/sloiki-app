from app.handlers.config import get_settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


settings = get_settings()
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args={'check_same_thread': False}, # for sqllite
)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
