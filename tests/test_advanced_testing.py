from unittest.mock import MagicMock, patch
import pytest
from fastapi.testclient import TestClient
from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate
from app.services.task_service import task_service


@pytest.mark.unit
@pytest.mark.parametrize(
    "status,priority",
    [
        (TaskStatus.TODO, TaskPriority.LOW),
        (TaskStatus.IN_PROGRESS, TaskPriority.MEDIUM),
        (TaskStatus.COMPLETED, TaskPriority.HIGH),
    ],
)
def test_parametrized_task_creation(client: TestClient, status: TaskStatus, priority: TaskPriority):
    """Test task creation across various status and priority combinations."""
    payload = {
        "title": f"Task for {status.value} - {priority.value}",
        "description": "Parametrized test run",
        "status": status.value,
        "priority": priority.value,
    }
    response = client.post("/tasks/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == status.value
    assert data["priority"] == priority.value


@pytest.mark.unit
@pytest.mark.parametrize(
    "invalid_email",
    [
        "plainaddress",
        "@missingusername.com",
        "username@.com",
        "username@com",
        "",
    ],
)
def test_parametrized_invalid_emails(client: TestClient, invalid_email: str):
    """Verify that invalid email formats are rejected by Pydantic validation."""
    response = client.post(
        "/users/",
        json={
            "username": "valid_user",
            "email": invalid_email,
            "password": "valid_password_123",
        },
    )
    assert response.status_code == 422


@pytest.mark.unit
def test_mocking_password_hashing(monkeypatch, client: TestClient):
    """Demonstrate mocking / monkeypatching internal security functions."""
    mock_hash = MagicMock(return_value="mocked_salt$mocked_hash_value")
    monkeypatch.setattr("app.services.user_service.hash_password", mock_hash)

    response = client.post(
        "/users/",
        json={
            "username": "mockeduser",
            "email": "mock@example.com",
            "password": "secretpassword",
        },
    )
    assert response.status_code == 201
    mock_hash.assert_called_once_with("secretpassword")


@pytest.mark.integration
def test_e2e_user_and_task_lifecycle(client: TestClient):
    """
    End-to-end integration test testing complete user journey:
    1. Register user
    2. Authenticate
    3. Create task assigned to user
    4. Filter task by user and status
    5. Update task to completed
    6. Verify final state
    """
    # 1. Register User
    user_payload = {
        "username": "sarah_connor",
        "email": "sarah@resistance.org",
        "password": "future_password_2029",
        "full_name": "Sarah Connor",
    }
    reg_resp = client.post("/users/", json=user_payload)
    assert reg_resp.status_code == 201
    user_id = reg_resp.json()["id"]

    # 2. Authenticate
    login_resp = client.post(
        "/users/login",
        json={"username": "sarah_connor", "password": "future_password_2029"},
    )
    assert login_resp.status_code == 200

    # 3. Create Task Assigned to Sarah
    task_payload = {
        "title": "Protect John Connor",
        "description": "High priority security assignment",
        "priority": "high",
        "assigned_user_id": user_id,
    }
    task_resp = client.post("/tasks/", json=task_payload)
    assert task_resp.status_code == 201
    task_id = task_resp.json()["id"]

    # 4. Filter tasks by user
    filter_resp = client.get(f"/tasks/?assigned_user_id={user_id}&status=todo")
    assert filter_resp.status_code == 200
    tasks = filter_resp.json()
    assert len(tasks) == 1
    assert tasks[0]["id"] == task_id

    # 5. Update task to completed
    update_resp = client.put(f"/tasks/{task_id}", json={"status": "completed"})
    assert update_resp.status_code == 200
    assert update_resp.json()["status"] == "completed"

    # 6. Verify completed filter
    completed_resp = client.get(f"/tasks/?assigned_user_id={user_id}&status=completed")
    assert completed_resp.status_code == 200
    assert len(completed_resp.json()) == 1


@pytest.mark.integration
def test_populated_fixture_queries(client: TestClient, populated_env):
    """Test utilizing the multi-entity populated_env fixture."""
    users = populated_env["users"]
    user1 = users[0]

    resp = client.get(f"/tasks/?assigned_user_id={user1.id}")
    assert resp.status_code == 200
    tasks = resp.json()
    assert len(tasks) == 2
