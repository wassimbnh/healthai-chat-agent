from fastapi import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from session.interface import AbstractSessionRepo
from session.repository import SessionRepository


def get_session_repository(db: Session = Depends(get_db)) -> AbstractSessionRepo:
    return SessionRepository(db)
