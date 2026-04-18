from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from message.model import MessageTab


class AbstractMessageRepo(ABC):
    @abstractmethod
    def create_message(self, session_id: UUID, role: str, content: str) -> MessageTab: ...

    @abstractmethod
    def get_messages_by_session(self, session_id: UUID) -> list[MessageTab]: ...