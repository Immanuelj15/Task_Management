from datetime import datetime
from typing import Annotated
from pydantic import BaseModel, Field, computed_field, model_validator
from app.models.task import TaskPriority, TaskStatus

TaskTitle = Annotated[str, Field(min_length=3, max_length=100, description="Task title")]
TaskDesc = Annotated[str, Field(default="", max_length=1000, description="Task description")]


class TaskBase(BaseModel):
    title: TaskTitle
    description: TaskDesc = ""
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority level")
    assigned_user_id: int | None = Field(default=None, description="ID of assigned user")


class TaskCreate(TaskBase):
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Initial task status")

    @model_validator(mode="after")
    def validate_task_rules(self) -> "TaskCreate":
        # Rule: HIGH priority tasks must have at least 5 chars title for clarity
        if self.priority == TaskPriority.HIGH and len(self.title.strip()) < 5:
            raise ValueError("High priority tasks must have a descriptive title of at least 5 characters.")
        return self


class TaskUpdate(BaseModel):
    title: str | None = Field(None, min_length=3, max_length=100)
    description: str | None = Field(None, max_length=1000)
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    assigned_user_id: int | None = None


class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    assigned_user_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

    @computed_field  # type: ignore[misc]
    @property
    def is_assigned(self) -> bool:
        """Computed field indicating if task is assigned to a user."""
        return self.assigned_user_id is not None

    @computed_field  # type: ignore[misc]
    @property
    def priority_weight(self) -> int:
        """Numeric rank for sorting tasks by importance."""
        weights = {
            TaskPriority.HIGH: 3,
            TaskPriority.MEDIUM: 2,
            TaskPriority.LOW: 1,
        }
        return weights.get(self.priority, 1)

