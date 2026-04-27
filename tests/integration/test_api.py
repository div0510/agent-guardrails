import pytest

fastapi = pytest.importorskip("fastapi")
from fastapi.testclient import TestClient

from src.api.app import app


client = TestClient(app)


def test_post_response_shape_is_consistent() -> None:
    response = client.post("/v1/respond", json={"prompt": "Summarize https://docs.agno.com/teams/overview"})
    assert response.status_code == 200
    payload = response.json()

    assert set(payload.keys()) == {"request_id", "status", "event", "data", "error"}
    assert payload["status"] == "success"
    assert payload["event"] == "final"
    assert "final_response" in payload["data"]


def test_stream_info_documents_websocket_contract() -> None:
    response = client.get("/v1/respond/stream-info")
    assert response.status_code == 200
    payload = response.json()

    assert payload["websocket_uri"] == "/v1/respond/stream"
    assert payload["envelope_keys"] == ["request_id", "status", "event", "data", "error"]


def test_websocket_stream_uses_same_envelope_shape() -> None:
    with client.websocket_connect("/v1/respond/stream") as websocket:
        websocket.send_json({"prompt": "Summarize https://docs.agno.com/tools/mcp/overview", "request_id": "req-123"})

        first = websocket.receive_json()
        assert set(first.keys()) == {"request_id", "status", "event", "data", "error"}
        assert first["event"] == "start"
        assert first["request_id"] == "req-123"

        events = [first["event"]]
        while True:
            message = websocket.receive_json()
            assert set(message.keys()) == {"request_id", "status", "event", "data", "error"}
            events.append(message["event"])
            if message["event"] == "end":
                break

        assert "chunk" in events
        assert "final" in events
        assert events[-1] == "end"
