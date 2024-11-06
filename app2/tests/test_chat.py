# Define test cases for chat operations

from fastapi.testclient import TestClient
from app2 import app

client = TestClient(app)

def test_start_session():
    # Test starting a new chat session
    response = client.post("/start_session", json={"user_id": "user123"})
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_send_message():
    # Test sending a message in a chat session
    start_response = client.post("/start_session", json={"user_id": "user123"})
    session_id = start_response.json()["session_id"]
    response = client.post(f"/send_message/{session_id}", json={"message": "Hi there", "sender": "user"})
    assert response.status_code == 200
    assert response.json()["status"] == "Message added"

def test_get_history():
    # Test retrieving chat history for a user
    response = client.get("/get_history/user123")
    assert response.status_code == 200
    assert "sessions" in response.json()
