from uuid import UUID

from fastapi import APIRouter, Depends, Query

from config.dependencies import get_db
from message.interface import AbstractMessageRepo
from message.repository import MessageRepository
from message.schema import MessageRead

router = APIRouter(prefix="/api/messages", tags=["messages"])


def get_message_repository(db=Depends(get_db)) -> AbstractMessageRepo:
    return MessageRepository(db)


@router.get("", response_model=list[MessageRead])
def get_messages(
    session_id: UUID = Query(..., description="Session ID to get messages for"),
    repository: AbstractMessageRepo = Depends(get_message_repository),
) -> list[MessageRead]:
    messages = repository.get_messages_by_session(session_id)
    return [MessageRead.model_validate(msg) for msg in messages]