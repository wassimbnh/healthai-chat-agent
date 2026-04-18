from uuid import uuid4

from fastapi.testclient import TestClient


def test_create_session_and_fetch_it_back(client: TestClient) -> None:
    user_id = str(uuid4())

    create_response = client.post("/api/sessions", json={"user_id": user_id})

    assert create_response.status_code == 201
    created_session = create_response.json()
    assert created_session["user_id"] == user_id
    assert "session_id" in created_session
    assert "created_at" in created_session

    session_id = created_session["session_id"]
    get_response = client.get(f"/api/sessions/{session_id}")

    assert get_response.status_code == 200
    assert get_response.json() == created_session


def test_get_session_returns_404_for_unknown_session(client: TestClient) -> None:
    response = client.get(f"/api/sessions/{uuid4()}")

    assert response.status_code == 404
    assert response.json() == {"detail": "Session not found"}


def test_create_multiple_sessions_for_same_user(client: TestClient) -> None:
    user_id = str(uuid4())

    response1 = client.post("/api/sessions", json={"user_id": user_id})
    assert response1.status_code == 201
    session1 = response1.json()

    response2 = client.post("/api/sessions", json={"user_id": user_id})
    assert response2.status_code == 201
    session2 = response2.json()

    assert session1["session_id"] != session2["session_id"]
    assert session1["user_id"] == session2["user_id"] == user_id


def test_create_session_returns_422_for_missing_user_id(client: TestClient) -> None:
    response = client.post("/api/sessions", json={})

    assert response.status_code == 422
