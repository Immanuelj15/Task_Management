from fastapi import FastAPI, HTTPException, Request, status, Query
from fastapi.responses import JSONResponse
from app.config import settings
from app.exceptions import (
    BaseAppException,
    EntityNotFoundException,
    UserNotFoundException,
    TaskNotFoundException,
    UserAlreadyExistsException,
    ValidationAppException,
    AuthenticationException,
)
from app.models.task import TaskStatus
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services.user_service import user_service
from app.services.task_service import task_service

import time
import uuid
from app.logging_config import logger

app = FastAPI(
    title=settings.APP_NAME,
    description="Modular Production-Grade API for managing users and tasks",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)


@app.middleware("http")
async def logging_and_correlation_middleware(request: Request, call_next):
    """
    Middleware injecting X-Request-ID and logging request execution duration.
    """
    request_id = request.headers.get("X-Request-ID") or str(uuid.uuid4())
    start_time = time.perf_counter()
    logger.info(f"Incoming: {request.method} {request.url.path} [req_id={request_id}]")

    response = await call_next(request)

    duration_ms = (time.perf_counter() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    logger.info(
        f"Completed: {request.method} {request.url.path} "
        f"status={response.status_code} ({duration_ms:.2f}ms) [req_id={request_id}]"
    )
    return response



@app.exception_handler(BaseAppException)
async def domain_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """Centralized handler for all domain business exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.message,
            "error_code": exc.error_code,
            "message": exc.message,
            "details": exc.details,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Fallback handler for standard ValueErrors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )



@app.get("/", tags=["Health"])
def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "healthy",
        "message": "Task Management API is running smoothly",
    }


# ==================== User Management Routes ====================


@app.post(
    "/users/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Users"],
    summary="Register a new user",
)
def create_user(user_in: UserCreate):
    try:
        user = user_service.create_user(user_in)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.get(
    "/users/",
    response_model=list[UserResponse],
    tags=["Users"],
    summary="List all users",
)
def list_users(skip: int = 0, limit: int = 100):
    return user_service.list_users(skip=skip, limit=limit)


@app.get(
    "/users/{user_id}",
    response_model=UserResponse,
    tags=["Users"],
    summary="Get user by ID",
)
def get_user(user_id: int):
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return user


@app.post(
    "/users/login",
    response_model=UserResponse,
    tags=["Users"],
    summary="Authenticate a user",
)
def login_user(credentials: UserLogin):
    user = user_service.authenticate_user(
        username=credentials.username,
        password=credentials.password,
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return user


# ==================== Task Management Routes ====================


@app.post(
    "/tasks/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Tasks"],
    summary="Create a new task",
)
def create_task(task_in: TaskCreate):
    try:
        task = task_service.create_task(task_in)
        return task
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.get(
    "/tasks/",
    response_model=list[TaskResponse],
    tags=["Tasks"],
    summary="List all tasks with optional filters",
)
def list_tasks(
    task_status: TaskStatus | None = Query(None, alias="status"),
    assigned_user_id: int | None = Query(None),
    skip: int = 0,
    limit: int = 100,
):
    return task_service.list_tasks(
        status=task_status,
        assigned_user_id=assigned_user_id,
        skip=skip,
        limit=limit,
    )


@app.get(
    "/tasks/stream/batches",
    response_model=list[list[TaskResponse]],
    tags=["Tasks"],
    summary="Retrieve tasks chunked in batches using custom iterator",
)
def get_task_batches(batch_size: int = Query(5, ge=1, le=50)):
    iterator = task_service.iter_tasks_batches(batch_size=batch_size)
    return list(iterator)


@app.get(
    "/tasks/ordered/priority",
    response_model=list[TaskResponse],
    tags=["Tasks"],
    summary="Iterate tasks in strict priority order (HIGH -> MEDIUM -> LOW)",
)
def get_tasks_by_priority():
    iterator = task_service.iter_tasks_by_priority()
    return list(iterator)



@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Get task by ID",
)
def get_task(task_id: int):
    task = task_service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return task


@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse,
    tags=["Tasks"],
    summary="Update task details or status",
)
def update_task(task_id: int, update_data: TaskUpdate):
    try:
        updated = task_service.update_task(task_id, update_data)
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Task with id {task_id} not found",
            )
        return updated
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Tasks"],
    summary="Delete a task",
)
def delete_task(task_id: int):
    deleted = task_service.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found",
        )
    return None