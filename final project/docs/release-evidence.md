Release Evidence
Baseline
Branch: final-project
Date: 2026-08-01
Local app run command:
uvicorn main:app --reload --port 8000
/health result:
{"status":"ok"}
Frontend check:
Opened frontend/index.html in a browser. The Task Tracker Kanban board loaded successfully, including the Search Tasks box and the To Do, In Progress, and Done columns.

Test command:
python -m pytest
Test result:
6 passed, 1 warning
CI Evidence
Workflow file: .github/workflows/ci.yml

Latest run link or note:

GitHub Actions workflow configured in the repository and used to run project validation checks automatically.

Test command used by CI:
python -m pytest
Shortcut check:
No continue-on-error
No || true
Pytest is not skipped
Docker Evidence
Build command:
docker build -t task-tracker .
Run command:
docker run -p 8000:8000 task-tracker
/health check:
Executed successfully from a running Docker container.

Command:

localhost:8000/health
Result:

{"status":"ok"}
Non-root check:
Verified. The Dockerfile creates and uses the non-root user appuser.

No-baked-secrets check:
Verified manually. No .env files, tokens, passwords, API keys, or credentials are copied into the image.

Documentation Claim-vs-Reality Log
Claim checked	Evidence used	Result	Change made, if any
API starts with uvicorn main:app --reload --port 8000	Manual run in terminal	Verified	None
GET /health returns application status	Browser check	Verified	None
Tests can be executed with python -m pytest	Pytest run	Verified	None