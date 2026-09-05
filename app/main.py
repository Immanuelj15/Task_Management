from fastapi import FastAPI

app = FastAPI(
    title="Task Management API",
    description="API for managing users and tasks",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Task Management API is running"
    }