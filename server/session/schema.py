from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class SessionCreate(BaseModel):
    user_id: UUID


class SessionRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    session_id: UUID
    user_id: UUID
    created_at: datetime
