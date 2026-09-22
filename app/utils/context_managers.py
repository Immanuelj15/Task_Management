import time
from contextlib import contextmanager
from typing import Any, Generator


class TimerContext:
    """
    Class-based Context Manager implementing __enter__ and __exit__.
    Measures elapsed execution time of a code block.
    """

    def __init__(self, name: str = "operation") -> None:
        self.name = name
        self.start_time: float = 0.0
        self.elapsed_ms: float = 0.0

    def __enter__(self) -> "TimerContext":
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self.elapsed_ms = (time.perf_counter() - self.start_time) * 1000
        # Return False to propagate exceptions normally
        return False


@contextmanager
def task_transaction(task_service: Any) -> Generator[None, None, None]:
    """
    Generator-based Context Manager (@contextmanager) for atomic rollback.
    Takes a snapshot of internal store before mutations.
    If an unhandled exception occurs inside the block, rolls back state.
    """
    # Create shallow snapshot of tasks dictionary and id counter
    tasks_snapshot = dict(task_service._tasks)
    id_snapshot = task_service._id_counter
    try:
        yield
    except Exception:
        # Atomic Rollback
        task_service._tasks = tasks_snapshot
        task_service._id_counter = id_snapshot
        raise
