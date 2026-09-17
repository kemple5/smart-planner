from fastapi.testclient import TestClient
from notification_service.main import app

client = TestClient(app)


def test_webhook_receives_task():
    payload = {
        "id": "11111111-1111-1111-1111-111111111111",
        "title": "Тест",
        "description": "",
        "status": "new",
        "created_at": "2024-01-01T00:00:00Z",
    }
    resp = client.post("/api/webhooks/task_created", json=payload)
    assert resp.status_code == 200
    assert resp.json()["status"] == "received"