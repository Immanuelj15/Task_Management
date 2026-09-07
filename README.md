# Task Management API 🚀

A production-grade, modular RESTful API built with **FastAPI** and **Python 3.11+**, designed following clean code principles, separation of concerns, and industry-standard architecture.

---

## 📌 Features

- **Modular Architecture**: Clean separation between `models`, `schemas`, `services`, and `utils`.
- **User Management**:
  - User registration with unique username and email constraints.
  - Password hashing with random salt (SHA-256).
  - User authentication and lookup endpoints.
- **Task Management**:
  - CRUD operations for tasks (Create, Read, Update, Delete).
  - Task assignment to registered users with validation.
  - Status tracking (`todo`, `in_progress`, `completed`).
  - Priority management (`low`, `medium`, `high`).
  - Filtering by status and assigned user.
- **Data Validation**: Strict schema validation using **Pydantic v2** and custom regex validators.
- **Automated Testing**: Comprehensive test suite covering all endpoints with **Pytest** and **HTTPX**.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## 📂 Project Structure

```text
task-management-api/
│
├── app/
│   ├── main.py              # FastAPI application entrypoint & API routes
│   ├── config.py            # Centralized application configuration & settings
│   ├── models/              # Core data entity definitions
│   │   ├── __init__.py
│   │   ├── user.py          # User data model
│   │   └── task.py          # Task data model & status/priority enums
│   ├── schemas/             # Pydantic validation schemas (Request/Response)
│   │   ├── __init__.py
│   │   ├── user.py          # UserCreate, UserResponse, UserLogin schemas
│   │   └── task.py          # TaskCreate, TaskUpdate, TaskResponse schemas
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py  # User CRUD & authentication business logic
│   │   └── task_service.py  # Task CRUD & assignment business logic
│   └── utils/               # Reusable helper utilities
│       ├── __init__.py
│       ├── security.py      # Password hashing & verification with salt
│       └── validators.py    # Email & username validation logic
│
├── tests/                   # Automated Pytest suite
│   ├── __init__.py
│   ├── test_users.py        # User management endpoint tests
│   └── test_tasks.py        # Task management endpoint tests
│
├── .env.example             # Example environment configuration template
├── .gitignore               # Ignored files (venv, .env, __pycache__)
├── requirements.txt         # Pinned project dependencies
└── README.md                # Project documentation
```

---

## 🛠️ Architecture & Separation of Concerns

| Directory / Layer | Purpose | Example Responsibilities |
| :--- | :--- | :--- |
| **`app/models/`** | Defines internal data entities and enums. | `User`, `Task`, `TaskStatus`, `TaskPriority` |
| **`app/schemas/`** | Request validation & response serialization using Pydantic. | Validating email format, minimum password length. |
| **`app/services/`** | Encapsulates all business logic and storage operations. | Preventing duplicate emails, assigning tasks to users. |
| **`app/utils/`** | Reusable standalone helper functions. | Cryptographic password hashing (`hash_password`). |
| **`app/config.py`** | Environment configuration loader. | Centralizing app name, debug flag, host, port. |
| **`app/main.py`** | Application bootstrap and route definitions. | HTTP routing and status code mapping. |

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ installed ([python.org](https://www.python.org/downloads/))
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
Copy the sample environment file to `.env`:
- **Windows:**
  ```cmd
  copy .env.example .env
  ```
- **Linux/macOS:**
  ```bash
  cp .env.example .env
  ```

---

## 🏃 Running the Application

Start the development server using Uvicorn:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Once running, access:
- **API Base URL**: `http://127.0.0.1:8000/`
- **Swagger Interactive API Documentation**: `http://127.0.0.1:8000/docs`
- **ReDoc Alternative Documentation**: `http://127.0.0.1:8000/redoc`

---

## 📚 API Endpoints Reference

### Health
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | API health check and version info |

### User Management
| Method | Endpoint | Status | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/users/` | `201 Created` | Register a new user |
| `GET` | `/users/` | `200 OK` | List all registered users |
| `GET` | `/users/{user_id}` | `200 OK` | Get user details by ID |
| `POST` | `/users/login` | `200 OK` | Authenticate user credentials |

#### Example: Register User
```json
POST /users/
{
  "username": "alex_doe",
  "email": "alex@example.com",
  "password": "securepassword123",
  "full_name": "Alex Doe"
}
```

### Task Management
| Method | Endpoint | Status | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/tasks/` | `201 Created` | Create a new task |
| `GET` | `/tasks/` | `200 OK` | List tasks (supports `?status=` & `?assigned_user_id=`) |
| `GET` | `/tasks/{task_id}` | `200 OK` | Get task by ID |
| `PUT` | `/tasks/{task_id}` | `200 OK` | Update task details or status |
| `DELETE` | `/tasks/{task_id}` | `204 No Content` | Delete a task |

#### Example: Create Task
```json
POST /tasks/
{
  "title": "Design Database Schema",
  "description": "Create ER diagrams and define foreign keys",
  "status": "todo",
  "priority": "high",
  "assigned_user_id": 1
}
```

---

## 🧪 Running Automated Tests

Run the full Pytest test suite:

```bash
pytest tests/ -v
```

Output:
```text
tests/test_tasks.py::test_create_task_unassigned PASSED
tests/test_tasks.py::test_create_task_with_valid_assigned_user PASSED
tests/test_tasks.py::test_create_task_with_invalid_assigned_user PASSED
tests/test_tasks.py::test_list_tasks_and_filtering PASSED
tests/test_tasks.py::test_update_task_status PASSED
tests/test_tasks.py::test_delete_task PASSED
tests/test_users.py::test_root_endpoint PASSED
tests/test_users.py::test_create_user_success PASSED
tests/test_users.py::test_create_user_duplicate_username PASSED
tests/test_users.py::test_create_user_invalid_email PASSED
tests/test_users.py::test_get_user_by_id PASSED
tests/test_users.py::test_get_user_not_found PASSED
tests/test_users.py::test_user_authentication PASSED

======================= 13 passed in 1.18s =======================
```

---

## 🌿 Git Branching Strategy

This project strictly adheres to feature-branch workflows and clean Git hygiene:
- `main`: Production-ready release branch.
- `feature/user-management`: User model, schemas, hashing utility, user service, and tests.
- `feature/task-management`: Task model, schemas, assignment logic, task service, and tests.
- **Security Rule**: `.env` is listed in `.gitignore` to prevent leaking secret keys. Only `.env.example` is committed.
