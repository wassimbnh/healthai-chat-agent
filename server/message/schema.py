from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class MessageCreate(BaseModel):
    session_id: UUID
    role: str
    content: str


class MessageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    message_id: UUID
    session_id: UUID
    role: str
    content: str
    created_at: datetime