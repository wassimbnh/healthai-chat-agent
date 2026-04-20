import json
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from chat.agent import get_response
from chat.ws_manager import ws_manager
from config.database import get_db
from message.interface import AbstractMessageRepo
from message.repository import MessageRepository


router = APIRouter(prefix="", tags=["chat"])

def get_message_repository(db=Depends(get_db)) -> AbstractMessageRepo:
    return MessageRepository(db)

@router.websocket("/ws/chat/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket, session_id: str,
    message_repository: AbstractMessageRepo = Depends(get_message_repository),
    ) -> None:
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            user_message = json.loads(data).get("message")

            if not user_message:
                await websocket.send_text(json.dumps({"error": "No message provided"}))
                continue

            db = next(get_db())
            try:

                message_repository.create_message(
                    session_id=UUID(session_id),
                    role="USER",
                    content=user_message,
                )

                history = message_repository.get_last_n(
                    session_id=UUID(session_id),
                    n=5,
                )

                await ws_manager.send_personal_message(
                    json.dumps({"type": "typing"}),
                    websocket,
                )

                bot_response_content = await get_response(user_message, history)

                bot_msg_record = message_repository.create_message(
                    session_id=UUID(session_id),
                    role="BOT",
                    content=bot_response_content,
                )

                await ws_manager.send_personal_message(
                    json.dumps(
                        {
                            "message": bot_response_content,
                            "message_id": str(bot_msg_record.message_id),
                        }
                    ),
                    websocket,
                )
            except Exception as e:
                await websocket.send_text(json.dumps({"error": str(e)}))
            finally:
                db.close()
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)