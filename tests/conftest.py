import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.task import TaskPriority, TaskStatus
from app.schemas.task import TaskCreate
from app.schemas.user import UserCreate
from app.services.task_service import task_service
from app.services.user_service import user_service


@pytest.fixture(autouse=True)
def reset_service_state():
    """Autouse fixture resetting user and task memory state before each test."""
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


@pytest.fixture
def client() -> TestClient:
    """Provides a fresh FastAPI test client."""
    return TestClient(app)


@pytest.fixture
def user_factory():
    """Factory fixture for creating registered users."""
    def _create_user(
        username: str = "testuser",
        email: str = "test@example.com",
        password: str = "securepassword123",
        full_name: str | None = "Test User",
    ):
        return user_service.create_user(
            UserCreate(
                username=username,
                email=email,
                password=password,
                full_name=full_name,
            )
        )
    return _create_user


@pytest.fixture
def task_factory(user_factory):
    """Factory fixture for creating tasks."""
    def _create_task(
        title: str = "Sample Task",
        description: str = "Sample Description",
        priority: TaskPriority = TaskPriority.MEDIUM,
        status: TaskStatus = TaskStatus.TODO,
        assigned_user_id: int | None = None,
    ):
        return task_service.create_task(
            TaskCreate(
                title=title,
                description=description,
                priority=priority,
                status=status,
                assigned_user_id=assigned_user_id,
            )
        )
    return _create_task


@pytest.fixture
def populated_env(user_factory, task_factory):
    """Fixture pre-populating multiple users and tasks for integration scenarios."""
    user1 = user_factory(username="alice", email="alice@test.com")
    user2 = user_factory(username="bob", email="bob@test.com")

    t1 = task_factory(title="Write API specs", priority=TaskPriority.HIGH, assigned_user_id=user1.id)
    t2 = task_factory(title="Set up CI pipeline", priority=TaskPriority.HIGH, assigned_user_id=user2.id)
    t3 = task_factory(title="Refactor auth", priority=TaskPriority.MEDIUM, assigned_user_id=user1.id)
    t4 = task_factory(title="Write unit tests", priority=TaskPriority.LOW, assigned_user_id=None)

    return {
        "users": [user1, user2],
        "tasks": [t1, t2, t3, t4],
    }
