from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from session.interface import AbstractSessionRepo
from session.model import SessionTab


class SessionRepository(AbstractSessionRepo):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_session(self, user_id: UUID) -> SessionTab:
        chat_session = SessionTab(user_id=str(user_id))
        self.db.add(chat_session)
        self.db.commit()
        self.db.refresh(chat_session)
        return chat_session

    def create_session_with_id(self, user_id: UUID, session_id: UUID) -> SessionTab:
        chat_session = SessionTab(session_id=str(session_id), user_id=str(user_id))
        self.db.add(chat_session)
        self.db.commit()
        self.db.refresh(chat_session)
        return chat_session

    def get_session(self, session_id: UUID) -> SessionTab | None:
        statement = select(SessionTab).where(SessionTab.session_id == str(session_id))
        return self.db.scalar(statement)
