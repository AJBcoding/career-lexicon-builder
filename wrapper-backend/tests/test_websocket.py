import pytest
from fastapi.testclient import TestClient
from main import app
import json

@pytest.fixture
def client():
    return TestClient(app)

def test_websocket_connection(client):
    with client.websocket_connect("/ws/test-project") as websocket:
        # Should receive welcome message
        data = websocket.receive_json()
        assert data["type"] == "connection"
        assert data["status"] == "connected"
        assert data["project_id"] == "test-project"

def test_websocket_ping_pong(client):
    with client.websocket_connect("/ws/test-project") as websocket:
        # Skip welcome message
        websocket.receive_json()

        # Send ping
        websocket.send_json({"type": "ping"})

        # Should receive pong
        data = websocket.receive_json()
        assert data["type"] == "pong"

def test_websocket_echo(client):
    with client.websocket_connect("/ws/test-project") as websocket:
        # Skip welcome message
        websocket.receive_json()

        # Send test message
        test_message = {"type": "test", "content": "hello"}
        websocket.send_json(test_message)

        # Should receive echo
        data = websocket.receive_json()
        assert data["type"] == "echo"
        assert data["data"] == test_message

def test_multiple_connections_same_project(client):
    with client.websocket_connect("/ws/test-project") as ws1:
        with client.websocket_connect("/ws/test-project") as ws2:
            # Both should receive welcome messages
            data1 = ws1.receive_json()
            data2 = ws2.receive_json()

            assert data1["type"] == "connection"
            assert data2["type"] == "connection"
