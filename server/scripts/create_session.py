"""Script to create a session with a hardcoded ID."""

import sys
from pathlib import Path
from uuid import UUID

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import Session, engine
from session.repository import SessionRepository

HARDCODED_SESSION_ID = UUID("00000000-0000-0000-0000-000000000001")
HARDCODED_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


def main() -> None:
    with Session(bind=engine) as db:
        repo = SessionRepository(db)
        session = repo.create_session_with_id(HARDCODED_USER_ID, HARDCODED_SESSION_ID)
        print(f"Created session: {session.session_id} for user: {session.user_id}")


if __name__ == "__main__":
    main()