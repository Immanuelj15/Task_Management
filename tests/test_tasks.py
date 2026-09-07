import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import user_service
from app.services.task_service import task_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


def test_create_task_unassigned():
    payload = {
        "title": "Write documentation",
        "description": "Write project README and API guide",
        "priority": "high",
        "status": "todo",
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Write documentation"
    assert data["status"] == "todo"
    assert data["priority"] == "high"
    assert data["assigned_user_id"] is None


def test_create_task_with_valid_assigned_user():
    # First create a user
    user_resp = client.post(
        "/users/",
        json={
            "username": "developer1",
            "email": "dev1@example.com",
            "password": "password123",
        },
    )
    user_id = user_resp.json()["id"]

    payload = {
        "title": "Implement auth middleware",
        "description": "Add JWT verification",
        "assigned_user_id": user_id,
        "priority": "high",
    }
    task_resp = client.post("/tasks/", json=payload)
    assert task_resp.status_code == 201
    data = task_resp.json()
    assert data["assigned_user_id"] == user_id


def test_create_task_with_invalid_assigned_user():
    payload = {
        "title": "Invalid task",
        "description": "Should fail",
        "assigned_user_id": 9999,
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 400
    assert "does not exist" in response.json()["detail"]


def test_list_tasks_and_filtering():
    # Create two tasks
    client.post(
        "/tasks/",
        json={"title": "Task One", "status": "todo", "priority": "low"},
    )
    client.post(
        "/tasks/",
        json={"title": "Task Two", "status": "completed", "priority": "high"},
    )

    # All tasks
    all_resp = client.get("/tasks/")
    assert all_resp.status_code == 200
    assert len(all_resp.json()) == 2

    # Filter by status=completed
    completed_resp = client.get("/tasks/?status=completed")
    assert completed_resp.status_code == 200
    completed_tasks = completed_resp.json()
    assert len(completed_tasks) == 1
    assert completed_tasks[0]["title"] == "Task Two"


def test_update_task_status():
    create_resp = client.post(
        "/tasks/",
        json={"title": "Refactor router", "status": "todo"},
    )
    task_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/tasks/{task_id}",
        json={"status": "in_progress", "priority": "high"},
    )
    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["status"] == "in_progress"
    assert updated_data["priority"] == "high"


def test_delete_task():
    create_resp = client.post(
        "/tasks/",
        json={"title": "Temporary task"},
    )
    task_id = create_resp.json()["id"]

    del_resp = client.delete(f"/tasks/{task_id}")
    assert del_resp.status_code == 204

    # Fetching deleted task should return 404
    get_resp = client.get(f"/tasks/{task_id}")
    assert get_resp.status_code == 404
