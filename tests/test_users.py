import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.user_service import user_service

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_tests():
    # Clear user store before each test
    user_service.clear()
    yield
    user_service.clear()


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


def test_create_user_success():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secretpassword123",
        "full_name": "Alice Johnson",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "alice"
    assert data["email"] == "alice@example.com"
    assert "password" not in data
    assert "hashed_password" not in data


def test_create_user_duplicate_username():
    payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secretpassword123",
    }
    resp1 = client.post("/users/", json=payload)
    assert resp1.status_code == 201

    duplicate_payload = {
        "username": "alice",
        "email": "different@example.com",
        "password": "secretpassword123",
    }
    resp2 = client.post("/users/", json=duplicate_payload)
    assert resp2.status_code == 400
    assert "already taken" in resp2.json()["detail"]


def test_create_user_invalid_email():
    payload = {
        "username": "bob123",
        "email": "not-an-email",
        "password": "secretpassword123",
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 422  # Pydantic validation error


def test_get_user_by_id():
    payload = {
        "username": "charlie",
        "email": "charlie@example.com",
        "password": "secretpassword123",
    }
    create_resp = client.post("/users/", json=payload)
    user_id = create_resp.json()["id"]

    get_resp = client.get(f"/users/{user_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["username"] == "charlie"


def test_get_user_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404


def test_user_authentication():
    payload = {
        "username": "diana",
        "email": "diana@example.com",
        "password": "mypassword123",
    }
    client.post("/users/", json=payload)

    # Valid credentials
    login_resp = client.post(
        "/users/login",
        json={"username": "diana", "password": "mypassword123"},
    )
    assert login_resp.status_code == 200
    assert login_resp.json()["username"] == "diana"

    # Invalid credentials
    bad_login = client.post(
        "/users/login",
        json={"username": "diana", "password": "wrongpassword"},
    )
    assert bad_login.status_code == 401
