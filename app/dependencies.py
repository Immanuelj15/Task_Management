from app.repositories.task_repository import InMemoryTaskRepository
from app.repositories.user_repository import InMemoryUserRepository
from app.services.task_service import TaskService, task_service
from app.services.user_service import UserService, user_service


def get_user_service() -> UserService:
    """Dependency provider for UserService."""
    return user_service


def get_task_service() -> TaskService:
    """Dependency provider for TaskService."""
    return task_service
