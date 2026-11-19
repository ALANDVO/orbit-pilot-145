import sys
sys.path.insert(0, ".")

from api.bot import router, BotTaskRequest
from fastapi.testclient import TestClient


def test_run_bot_task():
    """Test POST /bot/run accepts valid request and returns status."""
    client = TestClient(router)
    response = client.post("/bot/run", json={"task_id": "test-task-001", "priority": 5, "timeout": 60})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "queued"
    assert data["task_id"] == "test-task-001"
    assert data["priority"] == 5
    assert data["timeout"] == 60


def test_run_bot_task_empty_task_id():
    """Test POST /bot/run rejects empty task_id with 400."""
    client = TestClient(router)
    response = client.post("/bot/run", json={"task_id": "", "priority": 5, "timeout": 60})
    assert response.status_code == 400


def test_run_bot_task_priority_too_high():
    """Test POST /bot/run rejects priority > 10 with 422 (Pydantic validation)."""
    client = TestClient(router)
    response = client.post("/bot/run", json={"task_id": "test-task", "priority": 15, "timeout": 60})
    assert response.status_code == 422


def test_run_bot_task_timeout_zero():
    """Test POST /bot/run rejects timeout=0 with 422 (Pydantic validation)."""
    client = TestClient(router)
    response = client.post("/bot/run", json={"task_id": "test-task", "priority": 5, "timeout": 0})
    assert response.status_code == 422


def test_check_bot_status():
    """Test GET /bot/status/{task_id} returns status."""
    client = TestClient(router)
    response = client.get("/bot/status/test-task-002")
    assert response.status_code == 200
    data = response.json()
    assert data["task_id"] == "test-task-002"
    assert data["status"] == "pending"
