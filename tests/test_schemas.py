from datetime import datetime
import pytest
from app.models.task import TaskPriority, TaskStatus
from app.schemas.common import APIResponse, PaginationMeta, PaginatedResponse
from app.schemas.task import TaskCreate, TaskResponse
from app.schemas.user import UserCreate, UserResponse


def test_api_response_generic():
    resp = APIResponse[dict](message="All good", data={"key": "value"})
    assert resp.success is True
    assert resp.data == {"key": "value"}
    assert isinstance(resp.timestamp, datetime)


def test_pagination_meta_and_paginated_response():
    meta = PaginationMeta.create(total=25, skip=10, limit=5)
    assert meta.total_items == 25
    assert meta.page == 3  # (10 // 5) + 1
    assert meta.total_pages == 5
    assert meta.has_next is True
    assert meta.has_prev is True

    paginated = PaginatedResponse[str](items=["item1", "item2"], meta=meta)
    assert len(paginated.items) == 2
    assert paginated.meta.total_pages == 5


def test_task_create_high_priority_validation():
    # Short title for HIGH priority should fail
    with pytest.raises(ValueError, match="at least 5 characters"):
        TaskCreate(title="Bug", priority=TaskPriority.HIGH)

    # Adequate title for HIGH priority should succeed
    task = TaskCreate(title="Bug in payment", priority=TaskPriority.HIGH)
    assert task.title == "Bug in payment"


def test_task_response_computed_fields():
    resp_unassigned = TaskResponse(
        id=1,
        title="Test Task",
        description="",
        status=TaskStatus.TODO,
        priority=TaskPriority.HIGH,
        assigned_user_id=None,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    assert resp_unassigned.is_assigned is False
    assert resp_unassigned.priority_weight == 3

    resp_assigned = TaskResponse(
        id=2,
        title="Test Task 2",
        description="",
        status=TaskStatus.COMPLETED,
        priority=TaskPriority.LOW,
        assigned_user_id=42,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    assert resp_assigned.is_assigned is True
    assert resp_assigned.priority_weight == 1


def test_user_create_password_same_as_username():
    with pytest.raises(ValueError, match="Password cannot be identical to username"):
        UserCreate(
            username="john_doe",
            email="john@example.com",
            password="john_doe",
        )


def test_user_response_computed_display_name():
    resp_with_full_name = UserResponse(
        id=1,
        username="johndoe",
        email="john@example.com",
        full_name="Johnathan Doe",
        is_active=True,
        created_at=datetime.utcnow(),
    )
    assert resp_with_full_name.display_name == "Johnathan Doe"

    resp_no_full_name = UserResponse(
        id=2,
        username="janedoe",
        email="jane@example.com",
        full_name=None,
        is_active=True,
        created_at=datetime.utcnow(),
    )
    assert resp_no_full_name.display_name == "janedoe"
