# Task Management API 🚀

A production-grade, modular RESTful API built with **FastAPI** and **Python 3.11+**, designed following clean code principles, separation of concerns, and industry-standard architecture.

---

## 🚀 15-Day Engineering Curriculum Implementation

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
| **D11** | **Branching** | [`7329143`](https://github.com/Immanuelj15/Task_Management/commit/7329143) | Git branching governance, naming convention validation (`validate_branch_name.py`), branch protection policy. |
| **D12** | **Git Large Files** | [`3899bb8`](https://github.com/Immanuelj15/Task_Management/commit/3899bb8) | Git LFS configuration (`.gitattributes`), pre-commit file size guard (`check_large_files.py`), binary handling guide. |
| **D13** | **PR / Review** | [`adf9736`](https://github.com/Immanuelj15/Task_Management/commit/adf9736) | Pull Request template, issue templates, code review rubric, GitHub Actions automated CI workflow (`ci.yml`). |
| **D14** | **Merge Conflicts** | [`6c6fb4c`](https://github.com/Immanuelj15/Task_Management/commit/6c6fb4c) | Merge conflict resolution playbook, marker scanner & simulator (`merge_conflict_simulator.py`), `git rerere` guidance. |
| **D15** | **Readiness Audit** | [`HEAD`](https://github.com/Immanuelj15/Task_Management) | Automated 6-pillar production readiness audit engine (`readiness_audit.py`) and verification scorecard. |

---

## 📁 Project Structure

```text
task-management-api/
│
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md     # Standardized Pull Request template (D13)
│   └── workflows/
│       └── ci.yml                   # Automated GitHub Actions CI pipeline (D13)
│
├── app/
│   ├── main.py                      # Application entrypoint, routing, middleware & handlers
│   ├── config.py                    # Centralized settings & environment loader (D1)
│   ├── dependencies.py              # Dependency injection providers (D8)
│   ├── exceptions.py                # Domain-driven custom exception hierarchy (D6)
│   ├── logging_config.py            # Structured rotating file & console logging (D7)
│   ├── models/                      # Core data entity definitions
│   │   ├── __init__.py
│   │   ├── user.py                  # User data model
│   │   └── task.py                  # Task data model & status/priority enums
│   ├── pipelines/                   # Composable OOP data processing pipelines (D3)
│   │   ├── __init__.py
│   │   ├── base.py                  # PipelineStage ABC, PipelineContext, Pipeline engine
│   │   └── task_pipeline.py         # SanitizationStage, AutoPriorityStage, AuditStage
│   ├── repositories/                # Repository pattern data access layer (D8)
│   │   ├── __init__.py
│   │   ├── base.py                  # IUserRepository, ITaskRepository protocols (ISP)
│   │   ├── user_repository.py       # InMemoryUserRepository implementation
│   │   └── task_repository.py       # InMemoryTaskRepository implementation
│   ├── schemas/                     # Pydantic validation schemas (D4)
│   │   ├── __init__.py
│   │   ├── common.py                # Generic APIResponse[T] and PaginatedResponse[T]
│   │   ├── user.py                  # UserCreate, UserResponse, UserLogin schemas
│   │   └── task.py                  # TaskCreate, TaskUpdate, TaskResponse schemas
│   ├── services/                    # Business logic layer (D8)
│   │   ├── __init__.py
│   │   ├── user_service.py          # User CRUD & authentication business logic
│   │   └── task_service.py          # Task CRUD, pipeline orchestration & transactions
│   └── utils/                       # Reusable helper utilities
│       ├── __init__.py
│       ├── context_managers.py      # TimerContext, task_transaction rollback (D5)
│       ├── decorators.py            # @measure_time, @retry, @audit_action (D5)
│       ├── iterators.py             # Custom iterators & streaming generators (D2)
│       ├── profiler.py              # MemoryProfiler (tracemalloc) & ExecutionProfiler (D10)
│       ├── security.py              # Password hashing & verification with salt
│       └── validators.py            # Email & username validation logic
│
├── docs/
│   ├── GIT_BRANCHING_STRATEGY.md     # Branching hierarchy, naming & governance (D11)
│   ├── GIT_LARGE_FILES.md           # Git LFS & binary handling guide (D12)
│   ├── CODE_REVIEW_GUIDELINES.md    # Engineering code review rubric (D13)
│   ├── MERGE_CONFLICT_RESOLUTION.md # Conflict resolution playbook & rerere (D14)
│   └── PRODUCTION_READINESS_AUDIT.md # Production readiness audit scorecard (D15)
│
├── scripts/
│   ├── validate_branch_name.py      # Git branch naming validator (D11)
│   ├── check_large_files.py         # Pre-commit & CI file size guard (D12)
│   ├── merge_conflict_simulator.py  # Conflict marker scanner & resolver (D14)
│   └── readiness_audit.py           # Automated 6-pillar production readiness audit (D15)
│
├── tests/                           # Complete Test Suite (100+ tests passing)
│   ├── conftest.py                  # Pytest fixtures & factories (D9)
│   ├── test_advanced_testing.py     # Parameterized & E2E integration tests (D9)
│   ├── test_branching_policy.py     # Branching governance tests (D11)
│   ├── test_config.py               # Environment & config tests (D1)
│   ├── test_decorators_cm.py        # Decorators & context managers tests (D5)
│   ├── test_exceptions.py           # Domain exceptions tests (D6)
│   ├── test_git_large_files.py      # Git LFS & large files tests (D12)
│   ├── test_iterators.py            # Iterator & streaming tests (D2)
│   ├── test_logging.py              # Logging & Correlation ID tests (D7)
│   ├── test_merge_conflicts.py      # Merge conflict resolution tests (D14)
│   ├── test_pipeline.py             # OOP Pipeline tests (D3)
│   ├── test_pr_governance.py        # PR templates & CI tests (D13)
│   ├── test_profiling.py            # Memory & execution profiler tests (D10)
│   ├── test_readiness_audit.py      # Production readiness audit tests (D15)
│   ├── test_schemas.py              # Pydantic & type hint tests (D4)
│   ├── test_solid.py                # SOLID principles tests (D8)
│   ├── test_tasks.py                # Task CRUD & filter tests
│   └── test_users.py                # User registration & auth tests
│
├── .env.example                     # Environment configuration template (D1)
├── .gitattributes                   # Git LFS tracking & line-ending normalization (D12)
├── .gitignore                       # Ignored files (venv, .env, logs/, etc.)
├── pytest.ini                       # Pytest test discovery & markers configuration (D9)
├── requirements.txt                 # Pinned project dependencies
└── README.md                        # Project documentation
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

### 3. Setup Virtual Environment
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run Test Suite
```bash
pytest
```

### 6. Run Production Readiness Audit
```bash
python scripts/readiness_audit.py
```
