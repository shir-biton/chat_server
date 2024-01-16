from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field


class Message(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    sender: str
    room: str
    message: str
