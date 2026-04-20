from uuid import UUID

from chat.agent import get_response
from chat.interface import AbstractChatService
from message.interface import AbstractMessageRepo


class ChatService(AbstractChatService):
    def __init__(self, message_repository: AbstractMessageRepo) -> None:
        self._message_repository = message_repository

    async def process_message(self, session_id: UUID, message: str) -> tuple[str, UUID]:
        self._message_repository.create_message(
            session_id=session_id,
            role="USER",
            content=message,
        )

        history = self._message_repository.get_last_n(session_id=session_id, n=5)

        bot_response = await get_response(message, history)

        bot_msg = self._message_repository.create_message(
            session_id=session_id,
            role="BOT",
            content=bot_response,
        )

        return bot_response, bot_msg.message_id