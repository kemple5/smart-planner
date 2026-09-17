from fastapi.testclient import TestClient
from task_service.main import app

client = TestClient(app)


def test_create_task_returns_full_payload():
    resp = client.post("/api/tasks", json={"title": "Купить хлеб", "description": "вечером"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["title"] == "Купить хлеб"
    assert body["status"] == "new"
    assert body["id"]
    assert body["created_at"].endswith("Z")


def test_list_and_delete():
    created = client.post("/api/tasks", json={"title": "temp"}).json()
    assert client.get(f"/api/tasks/{created['id']}").status_code == 200
    assert client.delete(f"/api/tasks/{created['id']}").status_code == 204
    assert client.get(f"/api/tasks/{created['id']}").status_code == 404