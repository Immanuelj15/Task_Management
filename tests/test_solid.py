import pytest
from fastapi.testclient import TestClient
from app.dependencies import get_user_service
from app.main import app
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User
from app.repositories.base import ITaskRepository, IUserRepository
from app.repositories.task_repository import InMemoryTaskRepository
from app.repositories.user_repository import InMemoryUserRepository
from app.schemas.user import UserCreate
from app.services.task_service import TaskService
from app.services.user_service import UserService


def test_user_repository_crud():
    repo = InMemoryUserRepository()
    user = User(
        id=0,
        username="solid_user",
        email="solid@example.com",
        hashed_password="hashed_pw_123",
    )
    saved = repo.add(user)
    assert saved.id == 1
    assert repo.get_by_username("solid_user") is not None
    assert repo.get_by_email("solid@example.com") is not None

    saved.full_name = "Solid Architecture"
    updated = repo.update(saved)
    assert updated is not None
    assert updated.full_name == "Solid Architecture"

    assert repo.delete(saved.id) is True
    assert repo.get_by_id(saved.id) is None


def test_task_repository_crud():
    repo = InMemoryTaskRepository()
    task = Task(id=0, title="SOLID Task", description="Testing ISP")
    saved = repo.add(task)
    assert saved.id == 1
    assert repo.get_by_id(1) is not None

    filtered = repo.list_filtered(status=TaskStatus.TODO)
    assert len(filtered) == 1

    assert repo.delete(1) is True
    assert repo.get_by_id(1) is None


def test_liskov_substitution_principle():
    """
    Verify that an alternative repository implementation adhering to ITaskRepository
    can seamlessly substitute InMemoryTaskRepository in TaskService (LSP & OCP).
    """
    class MockTaskRepository(ITaskRepository):
        def __init__(self):
            self.store = {}
            self.counter = 1

        def get_by_id(self, task_id: int):
            return self.store.get(task_id)

        def list_all(self, skip=0, limit=100):
            return list(self.store.values())[skip : skip + limit]

        def list_filtered(self, status=None, assigned_user_id=None, skip=0, limit=100):
            return list(self.store.values())[skip : skip + limit]

        def add(self, task: Task):
            task.id = self.counter
            self.store[task.id] = task
            self.counter += 1
            return task

        def update(self, task: Task):
            self.store[task.id] = task
            return task

        def delete(self, task_id: int):
            return self.store.pop(task_id, None) is not None

        def clear(self):
            self.store.clear()

    mock_repo = MockTaskRepository()
    service = TaskService(repository=mock_repo)

    from app.schemas.task import TaskCreate
    created = service.create_task(TaskCreate(title="Substituted Repo Task"))
    assert created.id == 1
    assert service.get_task_by_id(1) is not None


def test_dependency_injection_override():
    """Verify FastAPI dependency injection override (DIP)."""
    custom_repo = InMemoryUserRepository()
    custom_service = UserService(repository=custom_repo)

    app.dependency_overrides[get_user_service] = lambda: custom_service
    client = TestClient(app)

    try:
        response = client.post(
            "/users/",
            json={
                "username": "di_user",
                "email": "di@example.com",
                "password": "secret_password_123",
            },
        )
        assert response.status_code == 201
        assert response.json()["username"] == "di_user"
        # Ensure it was saved in the overridden repository
        assert custom_repo.get_by_username("di_user") is not None
    finally:
        app.dependency_overrides.clear()
