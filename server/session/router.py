from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from config.dependencies import get_session_repository
from session.interface import AbstractSessionRepo
from session.schema import SessionCreate, SessionRead


router = APIRouter(prefix="/api/sessions", tags=["sessions"])


@router.post("", response_model=SessionRead, status_code=status.HTTP_201_CREATED)
def create_session(
    payload: SessionCreate,
    repository: AbstractSessionRepo = Depends(get_session_repository),
) -> SessionRead:
    session = repository.create_session(payload.user_id)
    return SessionRead.model_validate(session)


@router.get("/{session_id}", response_model=SessionRead)
def get_session(
    session_id: UUID,
    repository: AbstractSessionRepo = Depends(get_session_repository),
) -> SessionRead:
    session = repository.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found")
    return SessionRead.model_validate(session)
