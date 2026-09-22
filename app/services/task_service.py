import threading
from datetime import datetime
from app.exceptions import ValidationAppException
from app.models.task import Task, TaskStatus
from app.repositories.base import ITaskRepository
from app.repositories.task_repository import InMemoryTaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.user_service import UserService, user_service
from app.utils.context_managers import task_transaction
from app.utils.decorators import measure_time


class TaskService:
    """
    Business Logic Layer for Task Management.
    Adheres to SOLID:
    - SRP: Dedicated solely to business validation and orchestration.
    - DIP: Relies on ITaskRepository abstraction rather than concrete store.
    - OCP: Storage implementation can be swapped without touching TaskService.
    """

    def __init__(
        self,
        repository: ITaskRepository | None = None,
        user_service_instance: UserService | None = None,
    ) -> None:
        self.repository = repository or InMemoryTaskRepository()
        self.user_service = user_service_instance or user_service
        self._lock = threading.RLock()

    # Dynamic bridge to underlying storage for transaction context manager
    @property
    def _tasks(self) -> dict[int, Task]:
        if hasattr(self.repository, "_tasks"):
            return self.repository._tasks  # type: ignore[attr-defined]
        return {}

    @_tasks.setter
    def _tasks(self, val: dict[int, Task]) -> None:
        if hasattr(self.repository, "_tasks"):
            self.repository._tasks = val  # type: ignore[attr-defined]

    @property
    def _id_counter(self) -> int:
        if hasattr(self.repository, "_id_counter"):
            return self.repository._id_counter  # type: ignore[attr-defined]
        return 1

    @_id_counter.setter
    def _id_counter(self, val: int) -> None:
        if hasattr(self.repository, "_id_counter"):
            self.repository._id_counter = val  # type: ignore[attr-defined]

    @measure_time
    def create_task(self, task_in: TaskCreate, apply_pipeline: bool = True) -> Task:
        with self._lock:
            # Process input through OOP pipeline if enabled
            if apply_pipeline:
                from app.pipelines.task_pipeline import default_task_pipeline
                context = default_task_pipeline.execute(task_in)
                task_in = context.payload

            # Validate assigned user exists if provided
            if task_in.assigned_user_id is not None:
                if not self.user_service.get_user_by_id(task_in.assigned_user_id):
                    raise ValidationAppException(f"User with ID {task_in.assigned_user_id} does not exist.")

            now = datetime.utcnow()
            new_task = Task(
                id=0,
                title=task_in.title,
                description=task_in.description,
                status=task_in.status,
                priority=task_in.priority,
                assigned_user_id=task_in.assigned_user_id,
                created_at=now,
                updated_at=now,
            )
            return self.repository.add(new_task)

    def bulk_create_tasks(self, tasks_in: list[TaskCreate]) -> list[Task]:
        """
        Transactional bulk task creation using task_transaction context manager.
        Ensures atomicity: either all tasks are created, or all are rolled back.
        """
        created_tasks: list[Task] = []
        with self._lock:
            with task_transaction(self):
                for task_in in tasks_in:
                    task = self.create_task(task_in)
                    created_tasks.append(task)
        return created_tasks

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.repository.get_by_id(task_id)

    def list_tasks(
        self,
        status: TaskStatus | None = None,
        assigned_user_id: int | None = None,
        skip: int = 0,
        limit: int = 100,
    ) -> list[Task]:
        return self.repository.list_filtered(
            status=status,
            assigned_user_id=assigned_user_id,
            skip=skip,
            limit=limit,
        )

    def iter_tasks_batches(self, batch_size: int = 10):
        from app.utils.iterators import TaskBatchIterator
        return TaskBatchIterator(self.repository.list_all(0, 100000), batch_size=batch_size)

    def iter_tasks_by_priority(self):
        from app.utils.iterators import TaskPriorityIterator
        return TaskPriorityIterator(self.repository.list_all(0, 100000))

    def stream_tasks(
        self,
        status: TaskStatus | None = None,
        assigned_user_id: int | None = None,
    ):
        from app.utils.iterators import stream_tasks_generator
        return stream_tasks_generator(
            self.repository.list_all(0, 100000),
            status=status,
            assigned_user_id=assigned_user_id,
        )

    def update_task(self, task_id: int, update_data: TaskUpdate) -> Task | None:
        with self._lock:
            task = self.repository.get_by_id(task_id)
            if not task:
                return None

            if update_data.assigned_user_id is not None:
                if not self.user_service.get_user_by_id(update_data.assigned_user_id):
                    raise ValidationAppException(f"User with ID {update_data.assigned_user_id} does not exist.")
                task.assigned_user_id = update_data.assigned_user_id

            if update_data.title is not None:
                task.title = update_data.title
            if update_data.description is not None:
                task.description = update_data.description
            if update_data.status is not None:
                task.status = update_data.status
            if update_data.priority is not None:
                task.priority = update_data.priority

            task.updated_at = datetime.utcnow()
            return self.repository.update(task)

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self.repository.delete(task_id)

    def clear(self) -> None:
        """Reset internal store for testing."""
        with self._lock:
            self.repository.clear()


# Default singleton instance for application use
task_service = TaskService()
