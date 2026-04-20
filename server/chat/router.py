import json
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from chat.interface import AbstractChatService
from chat.ws_manager import ws_manager
from config.dependencies import get_chat_service


router = APIRouter(prefix="", tags=["chat"])


@router.websocket("/ws/chat/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    chat_service: AbstractChatService = Depends(get_chat_service),
) -> None:
    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            user_message = json.loads(data).get("message")

            if not user_message:
                await websocket.send_text(json.dumps({"error": "No message provided"}))
                continue

            await ws_manager.send_personal_message(
                json.dumps({"type": "typing"}),
                websocket,
            )

            bot_response, message_id = await chat_service.process_message(
                UUID(session_id), user_message
            )

            await ws_manager.send_personal_message(
                json.dumps(
                    {
                        "message": bot_response,
                        "message_id": str(message_id),
                    }
                ),
                websocket,
            )
    except WebSocketDisconnect:
        ws_manager.disconnect(session_id)
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))