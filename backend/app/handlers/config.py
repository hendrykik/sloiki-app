from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


ENV_FILE = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_FILE)

    SECRET_KEY: str = ""
    ALGORITHM: str = ""
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    HOST_URL: str = ""
    DB_NAME: str = ""
    DB_USER: str = ""
    DB_PASSWORD: str = ""

    @property
    def DATABASE_URL(self) -> str:
        # return "sqlite:///./todosapp.db'"
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.HOST_URL}/{self.DB_NAME}"


@lru_cache
def get_settings() -> Settings:
    return Settings()
