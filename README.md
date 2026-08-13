# Task Tracker API

A learning-focused REST API built with Python and FastAPI, using in-memory storage for task
management, plus a vanilla HTML/CSS/JavaScript Kanban board frontend. Built as part of the
AI-Assisted Coding course (Modules 2-4).

## Prerequisites

- Python 3.11+ (course target; developed locally against a newer version)
- pip

## Local setup

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run the app locally

```powershell
uvicorn app.main:app --reload --port 8000
```

- API base URL: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- Frontend: open `frontend/index.html` directly in a browser

## Run tests

```powershell
pytest -v
```

## Run with Docker

Build the image:
```powershell
docker build -t task-tracker:dev .
```

Run the container:
```powershell
docker run -d --name tt-dev -p 8000:8000 task-tracker:dev
```

Verify it's running:
```powershell
curl.exe http://localhost:8000/health
docker exec tt-dev whoami
```

Stop and remove:
```powershell
docker stop tt-dev
docker rm tt-dev
```

## CI workflow

GitHub Actions runs on every push and pull request:
1. Checks out the repo
2. Sets up Python 3.11
3. Installs dependencies from `requirements.txt`
4. Runs `pytest -v`

See `.github/workflows/ci.yml`.

## Project structure
## Project conventions

- **Status values:** exactly `ToDo`, `InProgress`, `Done`
- **Priority values:** exactly `Low`, `Medium`, `High`
- **Valid status transitions:** `ToDo → InProgress`, `InProgress → Done`, `Done → InProgress`.
  Same-status and skip-ahead transitions are rejected with HTTP 422.
- **Storage:** in-memory only. Data is lost on server restart. No database.
- **No authentication** — a learning-project scope decision, documented in `docs/security-review.md`.

## Current limitations

- No persistence across restarts
- No authentication or authorization
- No real-time sync between multiple open browser tabs
- CORS is currently permissive (`allow_origins=["*"]`) for local development

## Decision notes

See `docs/decisions/` for technical decision records.
task-tracker/
├── app/
│ ├── main.py
│ ├── models.py
│ ├── storage.py
│ ├── business_rules.py
│ ├── core/config.py
│ └── api/routes/health.py
├── frontend/
│ └── index.html
├── tests/
│ ├── conftest.py
│ └── test_tasks.py
├── Dockerfile
├── .dockerignore
├── .github/workflows/ci.yml
├── requirements.txt
└── README.md