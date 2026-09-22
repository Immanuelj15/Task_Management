from typing import Any, Generic, Protocol, Sequence, TypeVar
from app.models.task import Task, TaskPriority, TaskStatus
from app.models.user import User

T = TypeVar("T")
ID = TypeVar("ID")


class IReadOnlyRepository(Protocol[T, ID]):
    """ISP: Interface for read-only data access operations."""

    def get_by_id(self, entity_id: ID) -> T | None:
        ...

    def list_all(self, skip: int = 0, limit: int = 100) -> Sequence[T]:
        ...


class IWriteRepository(Protocol[T, ID]):
    """ISP: Interface for mutation operations."""

    def add(self, entity: T) -> T:
        ...

    def update(self, entity_id: ID, entity: T) -> T | None:
        ...

    def delete(self, entity_id: ID) -> bool:
        ...


class IUserRepository(Protocol):
    """Contract for user data access."""

    def get_by_id(self, user_id: int) -> User | None:
        ...

    def get_by_username(self, username: str) -> User | None:
        ...

    def get_by_email(self, email: str) -> User | None:
        ...

    def list_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        ...

    def add(self, user: User) -> User:
        ...

    def update(self, user: User) -> User | None:
        ...

    def delete(self, user_id: int) -> bool:
        ...

    def clear(self) -> None:
        ...


class ITaskRepository(Protocol):
    """Contract for task data access."""

    def get_by_id(self, task_id: int) -> Task | None:
        ...

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        ...

    def list_filtered(
        self,
        status: TaskStatus | None = None,
        assigned_user_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        ...

    def add(self, task: Task) -> Task:
        ...

    def update(self, task: Task) -> Task | None:
        ...

    def delete(self, task_id: int) -> bool:
        ...

    def clear(self) -> None:
        ...
