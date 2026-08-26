# Task Tracker API
Final Project

This repository represents the final version of the Task Tracker project completed within the scope of the course. The application continues to provide the original task management functionality while also including the required testing, CI, Docker, security, and AI-review evidence.

Final Project Highlights
The Task Tracker API and Kanban frontend remain within the intended project scope.
Automated tests are run through GitHub Actions on pushes and pull requests.
The application can be built and executed using Docker.
The /health endpoint can be used to confirm that the application is running.
AI-assisted development, security checks, and ownership evidence are documented in the docs/ directory.
Final Verification

The application can be started locally with:

uvicorn app.main:app --reload --port 8000

The health endpoint can then be checked at:

http://localhost:8000/health

The interactive API documentation is available at:

http://localhost:8000/docs
Testing

The complete test suite can be run with:

pytest -v

Tests were also configured to run automatically through the GitHub Actions CI workflow.

Docker Verification

The final application can be containerized using:

docker build -t task-tracker:dev .

and started with:

docker run -d --name tt-dev -p 8000:8000 task-tracker:dev

The running container can be verified using:

curl.exe http://localhost:8000/health
docker exec tt-dev whoami

The health endpoint should return a successful response, and the container is configured to run using the non-root appuser.

Evidence and Documentation

Supporting evidence for the final project is available in the docs/ directory, including:

docs/release-evidence.md
docs/final-ai-review.md
docs/ai-playbook.md
docs/security-review.md

These documents record the release checks, AI-assisted development process, security review, and ownership evidence.

AI Assistance

AI tools were used during development to support tasks such as:

Improving automated tests
Reviewing and implementing status transition rules
Preparing project documentation
Assisting with Docker configuration
Reviewing CI configuration
Supporting the security review

All AI-generated suggestions were reviewed against the actual repository before being accepted. Verification included automated tests, manual API checks, frontend testing, health endpoint checks, and direct review of the affected files.

One example of correcting an AI suggestion was an incorrect assumption that status-transition validation had already been implemented. After checking the code, I confirmed that the rule was missing and implemented the required validation based on the project requirements.

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

