from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any
from uuid import UUID


class AbstractChatService(ABC):
    @abstractmethod
    async def process_message(self, session_id: UUID, message: str) -> tuple[str, UUID]: ...