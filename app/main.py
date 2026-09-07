from fastapi import FastAPI, HTTPException, status
from app.config import settings
from app.schemas.user import UserCreate, UserResponse, UserLogin
from app.services.user_service import user_service

app = FastAPI(
    title=settings.APP_NAME,
    description="Modular Production-Grade API for managing users and tasks",
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
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