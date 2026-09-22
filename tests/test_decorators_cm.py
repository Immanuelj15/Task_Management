import time
import pytest
from app.schemas.task import TaskCreate
from app.services.task_service import task_service
from app.services.user_service import user_service
from app.utils.context_managers import TimerContext, task_transaction
from app.utils.decorators import audit_action, measure_time, retry


@pytest.fixture(autouse=True)
def clean_stores():
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


def test_measure_time_decorator():
    @measure_time
    def sample_work():
        time.sleep(0.01)
        return "done"

    result = sample_work()
    assert result == "done"
    assert hasattr(sample_work, "last_execution_time_ms")
    assert sample_work.last_execution_time_ms >= 5.0


def test_retry_decorator_succeeds_eventually():
    call_count = 0

    @retry(max_attempts=3, delay_seconds=0.001, exceptions=(ValueError,))
    def flaky_func():
        nonlocal call_count
        call_count += 1
        if call_count < 2:
            raise ValueError("Temporary failure")
        return "success"

    assert flaky_func() == "success"
    assert call_count == 2


def test_retry_decorator_raises_after_max_attempts():
    call_count = 0

    @retry(max_attempts=2, delay_seconds=0.001, exceptions=(RuntimeError,))
    def always_fails():
        nonlocal call_count
        call_count += 1
        raise RuntimeError("Persistent error")

    with pytest.raises(RuntimeError, match="Persistent error"):
        always_fails()

    assert call_count == 2


def test_audit_action_decorator():
    @audit_action("export_data")
    def export(filename: str):
        return f"exported {filename}"

    res = export("report.csv")
    assert res == "exported report.csv"
    assert len(export.audit_log) == 1
    assert export.audit_log[0]["action"] == "export_data"


def test_timer_context_manager():
    with TimerContext("database_query") as timer:
        time.sleep(0.01)

    assert timer.name == "database_query"
    assert timer.elapsed_ms >= 5.0


def test_task_transaction_rollback_on_failure():
    # Pre-populate one task
    task_service.create_task(TaskCreate(title="Initial Task"))
    assert len(task_service.list_tasks()) == 1

    # Attempt transactional bulk creation with an invalid task in the middle
    items = [
        TaskCreate(title="Valid Task 1"),
        TaskCreate(title="Failing Task", assigned_user_id=9999),  # Non-existent user
    ]

    with pytest.raises(ValueError, match="does not exist"):
        task_service.bulk_create_tasks(items)

    # State must be rolled back completely to initial single task!
    assert len(task_service.list_tasks()) == 1
    assert task_service.list_tasks()[0].title == "Initial Task"


def test_task_transaction_success():
    items = [
        TaskCreate(title="Bulk Task 1"),
        TaskCreate(title="Bulk Task 2"),
    ]
    created = task_service.bulk_create_tasks(items)
    assert len(created) == 2
    assert len(task_service.list_tasks()) == 2
