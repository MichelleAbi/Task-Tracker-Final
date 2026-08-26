# AGENTS.md

## Project Overview

This repository contains a Task Tracker application built with FastAPI and a simple Kanban-style web interface.

The main technologies used are:

* FastAPI for the backend API
* In-memory storage for task data
* Pytest for automated testing
* HTML, CSS, and JavaScript for the frontend
* GitHub Actions for continuous integration, where configured
* Docker for containerized application execution, where configured

## Run Commands

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start the Backend

```bash
uvicorn main:app --reload --port 8000
```

### Run the Test Suite

```bash
python -m pytest
```

### Check Application Health

Send a GET request to:

```text
GET /health
```

Expected response:

```json
{"status":"ok"}
```

### Open the Frontend

The frontend entry point is:

```text
frontend/index.html
```

## Business Rules

The application follows these main rules:

* Task titles must contain actual text and cannot consist only of whitespace.
* Changes between task statuses are subject to validation rules.
* Tasks can be filtered according to their status.
* Tasks can be filtered by priority.
* Tasks support filtering by tag.
* The application provides task search functionality.
* Invalid status changes result in HTTP 422.
* Requests for tasks that do not exist return HTTP 404.

## Important Project Structure

The main project areas and files include:

```text
app/
frontend/
docs/
main.py
README.md
requirements.txt
```

When making changes, check the actual repository structure instead of assuming that a file or directory exists.

## Module 5 and Final Project Guardrails

* Read the relevant documentation and repository files before suggesting changes.
* Follow a documentation-first approach when working on project requirements.
* Store project evidence and supporting documentation in `docs/`.
* Do not create or claim files that are not actually present.
* Base statements about the implementation on real repository files.
* Clearly identify information as unconfirmed when it cannot be verified from the repository.
* Keep changes within the requirements and scope of the final project.

## AI Review Expectations

When using AI assistance:

* Explain the purpose of a proposed change before implementing it.
* Identify the actual files affected by the change.
* Avoid making assumptions about the codebase.
* Do not introduce unrelated features or unnecessary modifications.
* Follow the requirements established for the final project.
* Review AI-generated suggestions against the actual implementation before accepting them.

## Security and Governance

Never provide AI tools with:

* API keys
* Authentication tokens
* Passwords
* `.env` contents
* Credentials
* Real customer information
* Other private or personally identifiable information

Always verify:

* Test results before documenting them
* Files changed by AI-assisted work
* API responses and status codes
* Claims made in project documentation

All AI-generated or AI-assisted changes must be reviewed, tested, and approved before being included in the final repository.
