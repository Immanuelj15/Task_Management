import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models.task import Task, TaskPriority, TaskStatus
from app.services.task_service import task_service
from app.services.user_service import user_service
from app.utils.iterators import (
    TaskBatchIterator,
    TaskPriorityIterator,
    stream_tasks_generator,
    chunked_iterable,
)

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_teardown():
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


def test_task_batch_iterator():
    tasks = [
        Task(id=i, title=f"Task {i}", description="", priority=TaskPriority.LOW)
        for i in range(1, 8)
    ]
    iterator = TaskBatchIterator(tasks, batch_size=3)
    batches = list(iterator)
    assert len(batches) == 3
    assert len(batches[0]) == 3
    assert len(batches[1]) == 3
    assert len(batches[2]) == 1  # 7th task alone


def test_task_batch_iterator_invalid_batch_size():
    tasks = [Task(id=1, title="Task 1", description="")]
    with pytest.raises(ValueError, match="batch_size must be greater than 0"):
        TaskBatchIterator(tasks, batch_size=0)


def test_task_priority_iterator():
    tasks = [
        Task(id=1, title="Low 1", description="", priority=TaskPriority.LOW),
        Task(id=2, title="High 1", description="", priority=TaskPriority.HIGH),
        Task(id=3, title="Medium 1", description="", priority=TaskPriority.MEDIUM),
        Task(id=4, title="High 2", description="", priority=TaskPriority.HIGH),
    ]
    iterator = TaskPriorityIterator(tasks)
    ordered = list(iterator)
    priorities = [t.priority for t in ordered]
    assert priorities == [
        TaskPriority.HIGH,
        TaskPriority.HIGH,
        TaskPriority.MEDIUM,
        TaskPriority.LOW,
    ]


def test_stream_tasks_generator():
    tasks = [
        Task(id=1, title="T1", description="", status=TaskStatus.TODO, assigned_user_id=1),
        Task(id=2, title="T2", description="", status=TaskStatus.COMPLETED, assigned_user_id=1),
        Task(id=3, title="T3", description="", status=TaskStatus.TODO, assigned_user_id=2),
    ]
    # Filter by status
    gen = stream_tasks_generator(tasks, status=TaskStatus.TODO)
    todo_tasks = list(gen)
    assert len(todo_tasks) == 2
    assert {t.id for t in todo_tasks} == {1, 3}

    # Filter by user
    gen_user = stream_tasks_generator(tasks, assigned_user_id=1)
    user_tasks = list(gen_user)
    assert len(user_tasks) == 2
    assert {t.id for t in user_tasks} == {1, 2}


def test_chunked_iterable():
    data = [1, 2, 3, 4, 5]
    chunks = list(chunked_iterable(data, 2))
    assert chunks == [[1, 2], [3, 4], [5]]

    with pytest.raises(ValueError, match="chunk_size must be greater than 0"):
        list(chunked_iterable(data, -1))


def test_api_task_batches_endpoint():
    # Create 6 tasks
    for i in range(1, 7):
        client.post(
            "/tasks/",
            json={"title": f"Task {i}", "description": "desc", "priority": "medium"},
        )

    response = client.get("/tasks/stream/batches?batch_size=4")
    assert response.status_code == 200
    batches = response.json()
    assert len(batches) == 2
    assert len(batches[0]) == 4
    assert len(batches[1]) == 2


def test_api_tasks_priority_endpoint():
    client.post("/tasks/", json={"title": "T Low", "priority": "low"})
    client.post("/tasks/", json={"title": "T High", "priority": "high"})
    client.post("/tasks/", json={"title": "T Med", "priority": "medium"})

    response = client.get("/tasks/ordered/priority")
    assert response.status_code == 200
    tasks = response.json()
    assert [t["priority"] for t in tasks] == ["high", "medium", "low"]
