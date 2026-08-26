# main.py — application entry point.
# Creates the FastAPI app, registers routers, and defines startup behavior.

from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.models import TaskCreate, TaskResponse, TaskStatus, TaskPriority, TaskUpdate
from app import storage

from app.business_rules import validate_status_transition
# Create the FastAPI application instance.
# The title and version appear in the auto-generated /docs (Swagger UI).
app = FastAPI(
    title="Task Tracker API",
    version="0.1.0",
    description="A learning-focused REST API built with FastAPI and JSON file storage.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers.
# All routes defined in health_router are mounted at the root path.
# Add future routers here (e.g., tasks, projects) as the app grows.
app.include_router(health_router)


# Optional: log the active environment on startup so it's clear which
# .env values were loaded (helpful when switching between dev/prod configs).
@app.on_event("startup")
async def on_startup() -> None:
    print(f"[startup] APP_ENV={settings.app_env}  PORT={settings.port}")


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)

@app.get("/tasks", response_model=list[TaskResponse], tags=["tasks"])
def list_tasks(
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    overdue: bool | None = None,
    tag: str | None = None,
) -> list[TaskResponse]:
    return storage.get_all_tasks(status=status, priority=priority, overdue=overdue, tag=tag)

@app.get("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def get_task(task_id: str) -> TaskResponse:
    task = storage.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return task

@app.patch("/tasks/{task_id}", response_model=TaskResponse, tags=["tasks"])
def patch_task(task_id: str, payload: TaskUpdate) -> TaskResponse:
    if payload.status is not None:
        existing = storage.get_task_by_id(task_id)
        if existing is None:
            raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
        validate_status_transition(existing.status, payload.status)

    updated = storage.update_task(task_id, payload)
    if updated is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")
    return updated

@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: str) -> None:
    deleted = storage.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")