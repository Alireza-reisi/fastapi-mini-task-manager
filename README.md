# FastAPI Task Management API

RESTful Task Management API built with **FastAPI** and **PostgreSQL** using **SQLAlchemy ORM**.  
It supports full **CRUD** operations, **search and filter** on tasks, interactive API documentation with **Swagger UI**, and production-ready deployment on Linux using **Gunicorn** and **systemd**.

---

## Table of Contents
- [Tech Stack](#tech-stack)
- [Project Features](#project-features)
- [Project Structure](#project-structure)
- [Database Model](#database-model)
- [API Endpoints](#api-endpoints)
- [PostgreSQL Setup](#postgresql-setup)
- [Setup Python Environment](#setup-python-environment)
- [Run the API](#run-the-api)
- [Troubleshooting](#troubleshooting)
- [Notes](#notes)

---

## Tech Stack
- Python 3.10+
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Gunicorn
- UvicornWorker
- systemd (Linux)

---

## Project Features
- Full CRUD operations for tasks
- Search in task `title` and `description`
- Filter tasks by `is_completed`
- Interactive API docs with Swagger UI
- PostgreSQL integration with SQLAlchemy ORM
- Production deployment using Gunicorn + systemd

---

## Project Structure
```bash
fastapi-mini-task-manager/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       └── tasks.py
│
├── .env
├── requirements.txt
└── README.md
```


---
## Database Model

The project contains one main model called `Task`.

| Field         | Type      | Description |
|--------------|-----------|-------------|
| id           | Integer   | Primary key |
| title        | String    | Task title |
| description  | String    | Optional description |
| isـcompleted | Boolean   | Completion status |
| created_at   | DateTime  | Task creation time |

---
## API Endpoints

### 1. Get all tasks
### Get all tasks (with Search & Filter)
**GET** `/tasks/`

Returns a list of all tasks. This endpoint also supports searching and filtering using query parameters.

#### Query parameters
- `q` (string, optional): Search in `title` and `description`
- `is_completed` (boolean, optional): Filter by completion status (`true` / `false`)

#### Example requests

Get all tasks:

    GET /tasks/

Filter only completed tasks:

    GET /tasks/?is_completed=true

Filter only incomplete tasks:

    GET /tasks/?is_completed=false

Search in title/description:

    GET /tasks/?q=fastapi

Search + filter together:

    GET /tasks/?q=deploy&is_completed=false

#### Example response

    [
      {
        "id": 1,
        "title": "Learn FastAPI",
        "description": "Practice CRUD operations",
        "is_completed": false,
        "created_at": "2025-05-31T10:30:00"
      }
    ]
`
---

### 2. Create a new task
**POST** `/tasks/`

Creates a new task.

Example request body:

    {
      "title": "Learn FastAPI",
      "description": "Practice CRUD operations"
    }

Example response:

    {
      "id": 1,
      "title": "Learn FastAPI",
      "description": "Practice CRUD operations",
      "isـcompleted": false,
      "created_at": "2025-05-31T10:30:00"
    }

---

### 3. Get a single task
**GET** `/tasks/{task_id}`

Returns a specific task by its ID.

Example response:

    {
      "id": 1,
      "title": "Learn FastAPI",
      "description": "Practice CRUD operations",
      "isـcompleted": false,
      "created_at": "2025-05-31T10:30:00"
    }

---

### 4. Update a task
**PUT** `/tasks/{task_id}`

Updates all fields of a task.

Example request body:

    {
      "title": "Learn FastAPI deeply",
      "description": "Update task content",
      "isـcompleted": true
    }

Example response:

    {
      "id": 1,
      "title": "Learn FastAPI deeply",
      "description": "Update task content",
      "isـcompleted": true,
      "created_at": "2025-05-31T10:30:00"
    }

---

### 5. Partially update a task
**PATCH** `/tasks/{task_id}`

Updates only the provided fields.

Example request body:

    {
      "isـcompleted": true
    }

Example response:

    {
      "id": 1,
      "title": "Learn FastAPI",
      "description": "Practice CRUD operations",
      "isـcompleted": true,
      "created_at": "2025-05-31T10:30:00"
    }

---

### 6. Delete a task
**DELETE** `/tasks/{task_id}`

Deletes a task by its ID.

Example response:

    {
      "message": "Task deleted successfully"
    }
`

---

## PostgreSQL Setup

### 1) Install PostgreSQL
Ubuntu/Debian:

    
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib

(اختیاری) بررسی نسخه:

    psql --version

---

### 2) Start & enable PostgreSQL service

    sudo systemctl enable --now postgresql
    sudo systemctl status postgresql

---

### 3) Create database (and optional user)

#### 3.1 Switch to `postgres` user

    sudo -i -u postgres

#### 3.2 Create database

    createdb task_db

#### 3.3 (Optional) Create a dedicated user + password

    createuser task_user
    psql -c "ALTER USER task_user WITH PASSWORD 'Alireza';"
    psql -c "GRANT ALL PRIVILEGES ON DATABASE task_db TO task_user;"

#### 3.4 Exit postgres user shell

    exit

---

### 4) Set `DATABASE_URL` in `.env`

Create a `.env` file in the project root and put **one** of the following:

Using default `postgres` user:

    DATABASE_URL=postgresql+psycopg2://postgres:YOUR_PASSWORD@localhost:5432/task_db

Using the dedicated user:

    DATABASE_URL=postgresql+psycopg2://task_user:STRONG_PASSWORD@localhost:5432/task_db
`
---
## Setup Python Environment (Local) + Install Gunicorn

### 1) Create and activate virtual environment

Linux/macOS:

    python3 -m venv venv
    source venv/bin/activate

---

### 2) Install project dependencies

Upgrade pip (recommended):

    python -m pip install --upgrade pip

Install requirements:

    python -m pip install -r requirements.txt
    python -m pip install gunicorn

---

### 3) Verify installations (important)

Make sure `python`, `pip`, and `gunicorn` are coming from the **venv**:

    which python
    which pip
    which gunicorn

Expected output should contain `.../venv/...`

Also you can check versions:

    python --version
    gunicorn --version

---
## Run the API (Local) + systemd (Production) + Gunicorn

### A) Run locally (Development / with reload)
From the project root (venv must be active):

    uvicorn main:app --reload --host 127.0.0.1 --port 8000

Open:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Quick test:

    curl http://127.0.0.1:8000/tasks/

---

### B) Run with systemd (Production)
> This is the recommended way for production (Gunicorn will be managed by systemd).

#### B.1 Create a systemd service file
Create:

    sudo nano /etc/systemd/system/task-api.service

Put this content inside (edit paths/user/env as needed):

    [Unit]
    Description=FastAPI Task Management API (Gunicorn)
    After=network.target

    [Service]
    User=www-data
    Group=www-data
    WorkingDirectory=/path/to/your/project

    EnvironmentFile=/path/to/your/project/.env

    ExecStart=/path/to/your/project/venv/bin/gunicorn \
      -w 2 \
      -k uvicorn.workers.UvicornWorker \
      -b 0.0.0.0:8000 \
      main:app

    Restart=always
    RestartSec=3

    [Install]
    WantedBy=multi-user.target

> Notes:
> - `User` can be your linux user (e.g. `ubuntu`) instead of `www-data`.
> - `WorkingDirectory` must be the project root (where `main.py` exists).
> - `ExecStart` must point to `.../venv/bin/gunicorn` (NOT `/usr/bin/gunicorn`).

#### B.2 Reload systemd and start the service

    sudo systemctl daemon-reload
    sudo systemctl enable --now task-api.service

Check status:

    sudo systemctl status task-api.service

View logs:

    sudo journalctl -u task-api.service -f

Quick test:

    curl http://127.0.0.1:8000/tasks/

---

### C) Run with Gunicorn (manual / Production-like)
> Use this if you don’t want systemd and just want to run it manually.

Important: run gunicorn from the venv:

    ./venv/bin/gunicorn -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app

Quick test:

    curl http://127.0.0.1:8000/tasks/

---

### D) Troubleshooting (common)

#### Port 8000 already in use
Find the process:

    sudo lsof -i :8000

Kill it (replace `<PID>`):

    sudo kill -9 <PID>

#### Verify gunicorn path (must be venv)
    which gunicorn
    ./venv/bin/gunicorn --version

--- 

## Notes
- Use `is_completed` and `created_at` consistently across the project.
- The search query parameter is `q`.
- For production, prefer `systemd` over manual Gunicorn execution.
- Make sure `.env` exists and contains the correct `DATABASE_URL`.


