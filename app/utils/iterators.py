from collections.abc import Iterator
from typing import Any, Generator, Sequence, TypeVar
from app.models.task import Task, TaskPriority, TaskStatus

T = TypeVar("T")


class TaskBatchIterator(Iterator[list[Task]]):
    """
    Custom Iterator that yields batches of tasks of a specified batch size.
    Implements Python's Iterator Protocol (__iter__ and __next__).
    """

    def __init__(self, tasks: Sequence[Task], batch_size: int = 5) -> None:
        if batch_size <= 0:
            raise ValueError("batch_size must be greater than 0")
        self._tasks = list(tasks)
        self._batch_size = batch_size
        self._index = 0

    def __iter__(self) -> "TaskBatchIterator":
        return self

    def __next__(self) -> list[Task]:
        if self._index >= len(self._tasks):
            raise StopIteration
        batch = self._tasks[self._index : self._index + self._batch_size]
        self._index += self._batch_size
        return batch


class TaskPriorityIterator(Iterator[Task]):
    """
    Custom Iterator that traverses tasks according to business priority:
    HIGH -> MEDIUM -> LOW.
    """

    PRIORITY_ORDER = {
        TaskPriority.HIGH: 0,
        TaskPriority.MEDIUM: 1,
        TaskPriority.LOW: 2,
    }

    def __init__(self, tasks: Sequence[Task]) -> None:
        self._sorted_tasks = sorted(
            tasks,
            key=lambda t: self.PRIORITY_ORDER.get(t.priority, 99),
        )
        self._index = 0

    def __iter__(self) -> "TaskPriorityIterator":
        return self

    def __next__(self) -> Task:
        if self._index >= len(self._sorted_tasks):
            raise StopIteration
        task = self._sorted_tasks[self._index]
        self._index += 1
        return task


def stream_tasks_generator(
    tasks: Sequence[Task],
    status: TaskStatus | None = None,
    assigned_user_id: int | None = None,
) -> Generator[Task, None, None]:
    """
    Generator function that lazily filters and yields tasks one at a time.
    Demonstrates lazy evaluation and memory efficiency.
    """
    for task in tasks:
        if status is not None and task.status != status:
            continue
        if assigned_user_id is not None and task.assigned_user_id != assigned_user_id:
            continue
        yield task


def chunked_iterable(iterable: Sequence[T], chunk_size: int) -> Generator[list[T], None, None]:
    """
    Generic generator to chunk any iterable into fixed-size batches.
    """
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    for i in range(0, len(iterable), chunk_size):
        yield list(iterable[i : i + chunk_size])
