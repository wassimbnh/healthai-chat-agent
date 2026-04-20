import json
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from chat.interface import AbstractChatService
from chat.ws_manager import ws_manager
from config.dependencies import get_chat_service, get_session_repository
from config.database import get_db
from session.interface import AbstractSessionRepo

logger = logging.getLogger(__name__)

router = APIRouter(prefix="", tags=["chat"])

@router.websocket("/ws/chat/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    db: Session = Depends(get_db),
    chat_service: AbstractChatService = Depends(get_chat_service),
) -> None:
    session_repository: AbstractSessionRepo = get_session_repository(db)

    try:
        session_uuid = UUID(session_id)
    except ValueError:
        logger.warning(f"Invalid session_id format: {session_id}")
        await websocket.close(code=4000, reason="Invalid session ID")
        return

    if not session_repository.get_session(session_uuid):
        logger.warning(f"Session not found: {session_id}")
        await websocket.close(code=4003, reason="Session not found")
        return

    await ws_manager.connect(session_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                parsed = json.loads(data)
            except json.JSONDecodeError:
                logger.warning(f"Invalid JSON from {session_id}")
                await websocket.send_text(json.dumps({"error": "Invalid JSON format"}))
                continue
            user_message = parsed.get("message")

            if not user_message:
                await websocket.send_text(json.dumps({"error": "No message provided"}))
                continue

            await ws_manager.send_personal_message(
                json.dumps({"type": "typing"}),
                websocket,
            )

            try:
                bot_response, message_id = await chat_service.process_message(
                    session_uuid, user_message
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
            except Exception as e:
                logger.error(f"Error processing message: {e}", exc_info=True)
                await websocket.send_text(json.dumps({"error": "Failed to process message"}))

    except WebSocketDisconnect:
        logger.info(f"Client disconnected: {session_id}")
        ws_manager.disconnect(session_id)
    except Exception as e:
        logger.error(f"WebSocket error for {session_id}: {e}", exc_info=True)
        await websocket.send_text(json.dumps({"error": "Connection error"}))