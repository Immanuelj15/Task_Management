import pytest
from fastapi.testclient import TestClient
from app.exceptions import (
    BaseAppException,
    UserNotFoundException,
    TaskNotFoundException,
    UserAlreadyExistsException,
    ValidationAppException,
    AuthenticationException,
)
from app.main import app
from app.services.task_service import task_service
from app.services.user_service import user_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_stores():
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


def test_exception_properties():
    exc = BaseAppException("Something failed", error_code="CUSTOM_ERR", status_code=418)
    assert exc.message == "Something failed"
    assert exc.error_code == "CUSTOM_ERR"
    assert exc.status_code == 418

    user_not_found = UserNotFoundException(42)
    assert user_not_found.status_code == 404
    assert user_not_found.error_code == "USER_NOT_FOUND"
    assert "42" in user_not_found.message

    task_not_found = TaskNotFoundException(101)
    assert task_not_found.status_code == 404
    assert task_not_found.error_code == "TASK_NOT_FOUND"

    dup_user = UserAlreadyExistsException("username", "testuser")
    assert dup_user.status_code == 400
    assert dup_user.error_code == "USER_ALREADY_EXISTS"

    auth_err = AuthenticationException()
    assert auth_err.status_code == 401
    assert auth_err.error_code == "INVALID_CREDENTIALS"

    val_err = ValidationAppException("Title cannot be empty")
    assert val_err.status_code == 400
    assert val_err.error_code == "VALIDATION_FAILED"


def test_duplicate_user_returns_structured_exception_response():
    payload = {
        "username": "charlie_app",
        "email": "charlie@example.com",
        "password": "mypassword123",
    }
    r1 = client.post("/users/", json=payload)
    assert r1.status_code == 201

    # Second creation should trigger UserAlreadyExistsException
    r2 = client.post("/users/", json=payload)
    assert r2.status_code == 400
    data = r2.json()
    assert "already taken" in data["detail"]


def test_task_invalid_user_returns_validation_exception_response():
    task_payload = {
        "title": "Invalid Assigned Task",
        "assigned_user_id": 99999,
    }
    resp = client.post("/tasks/", json=task_payload)
    assert resp.status_code == 400
    data = resp.json()
    assert "does not exist" in data["detail"]
