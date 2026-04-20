from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from message.interface import AbstractMessageRepo
from message.model import MessageTab


class MessageRepository(AbstractMessageRepo):
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_message(self, session_id: UUID, role: str, content: str) -> MessageTab:
        message = MessageTab(session_id=str(session_id), role=role, content=content)
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_by_session(self, session_id: UUID) -> list[MessageTab]:
        statement = (
            select(MessageTab)
            .where(MessageTab.session_id == str(session_id))
            .order_by(MessageTab.created_at.asc())
        )
        return list(self.db.execute(statement).scalars().all())

    def get_last_n(self, session_id: UUID, n: int) -> list[MessageTab]:
        statement = (
            select(MessageTab)
            .where(MessageTab.session_id == str(session_id))
            .order_by(MessageTab.created_at.desc())
            .limit(n)
        )
        latest_first = list(self.db.execute(statement).scalars().all())
        return list(reversed(latest_first))