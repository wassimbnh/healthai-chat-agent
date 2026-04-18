from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from session.model import SessionTab


class AbstractSessionRepo(ABC):
    @abstractmethod
    def create_session(self, user_id: UUID) -> SessionTab: ...

    @abstractmethod
    def get_session(self, session_id: UUID) -> SessionTab | None: ...
