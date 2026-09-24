# Task Management API 🚀

A production-grade, modular RESTful API built with **FastAPI** and **Python 3.11+**, designed following clean code principles, separation of concerns, and industry-standard architecture.

---

## 🏆 10-Day Engineering Curriculum Implementation

| Day | Topic | Commit Hash | Key Implementation Highlights |
| :--- | :--- | :--- | :--- |
| **D1** | **Env Setup** | [`8a483dc`](https://github.com/Immanuelj15/Task_Management/commit/8a483dc) | Lightweight, dependency-free `.env` loader, profile validation (`dev`/`test`/`staging`/`prod`), port boundaries. |
| **D2** | **Iterators** | [`e6f2cf8`](https://github.com/Immanuelj15/Task_Management/commit/e6f2cf8) | `TaskBatchIterator`, `TaskPriorityIterator`, generator streaming (`stream_tasks_generator`), batch endpoints. |
| **D3** | **OOP / Pipeline** | [`6af23a2`](https://github.com/Immanuelj15/Task_Management/commit/6af23a2) | Composable OOP pipeline (`PipelineStage[T]`, `Pipeline[T]`), `SanitizationStage`, `AutoPriorityStage`, `AuditStage`. |
| **D4** | **Type Hints & Pydantic** | [`dc9f273`](https://github.com/Immanuelj15/Task_Management/commit/dc9f273) | Strict typing with `Annotated`, generic wrappers `APIResponse[T]`, `PaginatedResponse[T]`, `@model_validator`, `@computed_field`. |
| **D5** | **Decorators / CM** | [`d2ace59`](https://github.com/Immanuelj15/Task_Management/commit/d2ace59) | Function decorators (`@measure_time`, `@retry`, `@audit_action`), class-based `TimerContext`, `@contextmanager` atomic `task_transaction`. |
| **D6** | **Exceptions** | [`6a9e801`](https://github.com/Immanuelj15/Task_Management/commit/6a9e801) | Domain exception hierarchy (`BaseAppException`, `EntityNotFound`, `DuplicateEntity`), centralized FastAPI exception handlers. |
| **D7** | **Logging** | [`6233cc2`](https://github.com/Immanuelj15/Task_Management/commit/6233cc2) | Structured logging with rotating file handler (`logs/app.log`) & console stream, Request Correlation ID (`X-Request-ID`) middleware. |
| **D8** | **SOLID Refactor** | [`911fbec`](https://github.com/Immanuelj15/Task_Management/commit/911fbec) | Repository Pattern (`IUserRepository`, `ITaskRepository`), Interface Segregation, Dependency Inversion with FastAPI `Depends()`. |
| **D9** | **Testing** | [`280e5fa`](https://github.com/Immanuelj15/Task_Management/commit/280e5fa) | Advanced Pytest suite (`pytest.ini`, `conftest.py`), fixtures, `@pytest.mark.parametrize`, mocking/monkeypatching, E2E integration test. |
| **D10** | **Debug & Profile** | [`98490e7`](https://github.com/Immanuelj15/Task_Management/commit/98490e7) | Runtime diagnostics, memory profiling (`tracemalloc`), execution profiling (`cProfile`), endpoints `/debug/memory`, `/debug/profiler/tasks`. |

---

## 📂 Project Structure

```text
task-management-api/
│
├── app/
│   ├── main.py              # Application entrypoint, routing, middleware & handlers
│   ├── config.py            # Centralized settings & environment loader (D1)
│   ├── dependencies.py      # Dependency injection providers (D8)
│   ├── exceptions.py        # Domain-driven custom exception hierarchy (D6)
│   ├── logging_config.py    # Structured rotating file & console logging (D7)
│   ├── models/              # Core data entity definitions
│   │   ├── __init__.py
│   │   ├── user.py          # User data model
│   │   └── task.py          # Task data model & status/priority enums
│   ├── pipelines/           # Composable OOP data processing pipelines (D3)
│   │   ├── __init__.py
│   │   ├── base.py          # PipelineStage ABC, PipelineContext, Pipeline engine
│   │   └── task_pipeline.py # SanitizationStage, AutoPriorityStage, AuditStage
│   ├── repositories/        # Repository pattern data access layer (D8)
│   │   ├── __init__.py
│   │   ├── base.py          # IUserRepository, ITaskRepository protocols (ISP)
│   │   ├── user_repository.py # InMemoryUserRepository implementation
│   │   └── task_repository.py # InMemoryTaskRepository implementation
│   ├── schemas/             # Pydantic validation schemas (D4)
│   │   ├── __init__.py
│   │   ├── common.py        # Generic APIResponse[T] and PaginatedResponse[T]
│   │   ├── user.py          # UserCreate, UserResponse, UserLogin schemas
│   │   └── task.py          # TaskCreate, TaskUpdate, TaskResponse schemas
│   ├── services/            # Business logic layer (D8)
│   │   ├── __init__.py
│   │   ├── user_service.py  # User CRUD & authentication business logic
│   │   └── task_service.py  # Task CRUD, pipeline orchestration & transactions
│   └── utils/               # Reusable helper utilities
│       ├── __init__.py
│       ├── context_managers.py # TimerContext, task_transaction rollback (D5)
│       ├── decorators.py    # @measure_time, @retry, @audit_action (D5)
│       ├── iterators.py     # Custom iterators & streaming generators (D2)
│       ├── profiler.py      # MemoryProfiler (tracemalloc) & ExecutionProfiler (D10)
│       ├── security.py      # Password hashing & verification with salt
│       └── validators.py    # Email & username validation logic
│
├── tests/                   # Comprehensive Automated Test Suite (74 tests)
│   ├── conftest.py          # Central Pytest fixtures & factories (D9)
│   ├── test_advanced_testing.py # Parameterized & E2E integration tests (D9)
│   ├── test_config.py       # Environment & config tests (D1)
│   ├── test_decorators_cm.py # Decorator & Context Manager tests (D5)
│   ├── test_exceptions.py   # Domain exception & error response tests (D6)
│   ├── test_iterators.py    # Iterator & streaming tests (D2)
│   ├── test_logging.py      # Logging & Correlation ID tests (D7)
│   ├── test_pipeline.py     # OOP Pipeline stages tests (D3)
│   ├── test_profiling.py    # Memory & execution profiler tests (D10)
│   ├── test_schemas.py      # Pydantic & type hint tests (D4)
│   ├── test_solid.py        # SOLID principles & DI override tests (D8)
│   ├── test_tasks.py        # Task CRUD & filter tests
│   └── test_users.py        # User registration & auth tests
│
├── pytest.ini               # Pytest test discovery & markers configuration (D9)
├── .env.example             # Environment configuration template (D1)
├── .gitignore               # Ignored files (venv, .env, logs/, etc.)
├── requirements.txt         # Pinned project dependencies
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.11+ installed ([python.org](https://www.python.org/downloads/))
- Git installed ([git-scm.com](https://git-scm.com/))

### 2. Clone Repository
```bash
git clone https://github.com/Immanuelj15/Task_Management.git
cd Task_Management/task-management-api
```

### 3. Create & Activate Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\Activate.ps1
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Environment Configuration
```bash
copy .env.example .env
```

---

## 🏃 Running the Application

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive Documentation:
- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

---

## 📚 API Endpoints Summary

### Health & Diagnostics
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API health check & version |
| `GET` | `/debug/memory` | Real-time memory allocation stats (`tracemalloc`) |
| `GET` | `/debug/profiler/tasks` | Execution profiling for task retrieval |
| `GET` | `/debug/system` | Platform, Python runtime, and GC diagnostics |

### User Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/users/` | Register a new user |
| `GET` | `/users/` | List all users |
| `GET` | `/users/{user_id}` | Get user by ID |
| `POST` | `/users/login` | Authenticate user credentials |

### Task Management
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/tasks/` | Create a task (processed via OOP pipeline) |
| `GET` | `/tasks/` | List tasks (supports `?status=` & `?assigned_user_id=`) |
| `GET` | `/tasks/stream/batches` | Chunked task iterator streaming |
| `GET` | `/tasks/ordered/priority` | Retrieve tasks ordered by priority hierarchy |
| `GET` | `/tasks/{task_id}` | Get task by ID |
| `PUT` | `/tasks/{task_id}` | Update task details or status |
| `DELETE` | `/tasks/{task_id}` | Delete task |

---

## 🧪 Running Automated Tests

Run the full suite of **74 unit, integration, and E2E tests**:

```bash
pytest -v
```

Output:
```text
============================= 74 passed in 2.26s ==============================
```
