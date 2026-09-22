import threading
from typing import Sequence
from app.models.task import Task, TaskPriority, TaskStatus
from app.repositories.base import ITaskRepository


class InMemoryTaskRepository(ITaskRepository):
    """
    In-memory implementation of ITaskRepository.
    Thread-safe storage dedicated strictly to task persistence (SRP).
    """

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._id_counter: int = 1
        self._lock = threading.RLock()

    def get_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Task]:
        tasks = list(self._tasks.values())
        return tasks[skip : skip + limit]

    def list_filtered(
        self,
        status: TaskStatus | None = None,
        assigned_user_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        tasks = list(self._tasks.values())
        if status is not None:
            tasks = [t for t in tasks if t.status == status]
        if assigned_user_id is not None:
            tasks = [t for t in tasks if t.assigned_user_id == assigned_user_id]
        return tasks[skip : skip + limit]

    def add(self, task: Task) -> Task:
        with self._lock:
            task.id = self._id_counter
            self._tasks[task.id] = task
            self._id_counter += 1
            return task

    def update(self, task: Task) -> Task | None:
        with self._lock:
            if task.id in self._tasks:
                self._tasks[task.id] = task
                return task
            return None

    def delete(self, task_id: int) -> bool:
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._id_counter = 1
