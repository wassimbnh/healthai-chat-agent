from fastapi import Depends
from sqlalchemy.orm import Session

from chat.interface import AbstractChatService
from chat.service import ChatService
from config.database import get_db
from message.interface import AbstractMessageRepo
from message.repository import MessageRepository
from session.interface import AbstractSessionRepo
from session.repository import SessionRepository


def get_session_repository(db: Session = Depends(get_db)) -> AbstractSessionRepo:
    return SessionRepository(db)


def get_message_repository(db: Session = Depends(get_db)) -> AbstractMessageRepo:
    return MessageRepository(db)


def get_chat_service(message_repository: AbstractMessageRepo = Depends(get_message_repository)) -> AbstractChatService:
    return ChatService(message_repository)
