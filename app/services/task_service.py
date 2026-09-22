import threading
from datetime import datetime
from app.models.task import Task, TaskStatus
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.user_service import user_service


class TaskService:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._id_counter: int = 1
        self._lock = threading.Lock()

    def create_task(self, task_in: TaskCreate) -> Task:
        with self._lock:
            # Validate assigned user exists if provided
            if task_in.assigned_user_id is not None:
                if not user_service.get_user_by_id(task_in.assigned_user_id):
                    raise ValueError(f"User with ID {task_in.assigned_user_id} does not exist.")

            now = datetime.utcnow()
            new_task = Task(
                id=self._id_counter,
                title=task_in.title,
                description=task_in.description,
                status=task_in.status,
                priority=task_in.priority,
                assigned_user_id=task_in.assigned_user_id,
                created_at=now,
                updated_at=now,
            )
            self._tasks[new_task.id] = new_task
            self._id_counter += 1
            return new_task

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self._tasks.get(task_id)

    def list_tasks(
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

    def iter_tasks_batches(self, batch_size: int = 10):
        from app.utils.iterators import TaskBatchIterator
        return TaskBatchIterator(list(self._tasks.values()), batch_size=batch_size)

    def iter_tasks_by_priority(self):
        from app.utils.iterators import TaskPriorityIterator
        return TaskPriorityIterator(list(self._tasks.values()))

    def stream_tasks(
        self,
        status: TaskStatus | None = None,
        assigned_user_id: int | None = None,
    ):
        from app.utils.iterators import stream_tasks_generator
        return stream_tasks_generator(
            list(self._tasks.values()),
            status=status,
            assigned_user_id=assigned_user_id,
        )


    def update_task(self, task_id: int, update_data: TaskUpdate) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if not task:
                return None

            if update_data.assigned_user_id is not None:
                if not user_service.get_user_by_id(update_data.assigned_user_id):
                    raise ValueError(f"User with ID {update_data.assigned_user_id} does not exist.")
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
            return task

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            if task_id in self._tasks:
                del self._tasks[task_id]
                return True
            return False

    def clear(self) -> None:
        """Reset internal store, helpful for unit testing."""
        with self._lock:
            self._tasks.clear()
            self._id_counter = 1


task_service = TaskService()
