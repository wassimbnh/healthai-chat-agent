import sys
from pathlib import Path
from uuid import UUID

sys.path.insert(0, str(Path(__file__).parent.parent))

from config.database import Session, engine, Base
from session.model import SessionTab as SessionModel   # import all models so Base knows about them
from message.model import MessageTab                   # ← triggers Base registration
from session.repository import SessionRepository

HARDCODED_SESSION_ID = UUID("00000000-0000-0000-0000-000000000001")
HARDCODED_USER_ID    = UUID("00000000-0000-0000-0000-000000000001")


def main() -> None:
    # create all tables first
    Base.metadata.create_all(bind=engine)

    with Session(bind=engine) as db:
        exists = db.query(SessionModel).filter(
            SessionModel.session_id == str(HARDCODED_SESSION_ID)
        ).first()

        if exists:
            print(f"Session {HARDCODED_SESSION_ID} already exists, skipping.")
            return

        repo = SessionRepository(db)
        session = repo.create_session_with_id(HARDCODED_USER_ID, HARDCODED_SESSION_ID)
        print(f"Created session: {session.session_id} for user: {session.user_id}")


if __name__ == "__main__":
    main()