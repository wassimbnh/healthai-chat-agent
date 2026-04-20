import pytest

from message.repository import MessageRepository


def test_get_messages_empty_for_new_session(client, test_user_id) -> None:
    session_response = client.post("/api/sessions", json={"user_id": test_user_id})
    session_id = session_response.json()["session_id"]

    response = client.get(f"/api/messages?session_id={session_id}")

    assert response.status_code == 200
    assert response.json() == []


def test_get_messages_returns_messages_in_order(client, db_session, test_user_id) -> None:
    session_response = client.post("/api/sessions", json={"user_id": test_user_id})
    session_id = session_response.json()["session_id"]

    repo = MessageRepository(db_session)
    repo.create_message(session_id, "USER", "Hello")
    repo.create_message(session_id, "BOT", "Hi there!")
    repo.create_message(session_id, "USER", "How are you?")

    response = client.get(f"/api/messages?session_id={session_id}")

    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 3
    assert messages[0]["role"] == "USER"
    assert messages[0]["content"] == "Hello"
    assert messages[1]["role"] == "BOT"
    assert messages[1]["content"] == "Hi there!"
    assert messages[2]["role"] == "USER"
    assert messages[2]["content"] == "How are you?"