from datetime import datetime
from pydantic import BaseModel, Field
from app.models.task import TaskStatus, TaskPriority


class TaskBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100, description="Task title")
    description: str = Field(default="", max_length=1000, description="Task description")
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, description="Task priority level")
    assigned_user_id: int | None = Field(default=None, description="ID of assigned user")


class TaskCreate(TaskBase):
    status: TaskStatus = Field(default=TaskStatus.TODO, description="Initial task status")


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
