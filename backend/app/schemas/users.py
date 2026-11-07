from pydantic import BaseModel, Field

class User(BaseModel):
    login: str | None = Field(default=None, min_length=1, max_length=255)
    password: str | None = Field(default=None, min_length=1, max_length=255)
