from unittest.loader import defaultTestLoader

from pydantic import BaseModel, Field
from datetime import datetime

class Events(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    date: datetime | None = Field(default=None)
