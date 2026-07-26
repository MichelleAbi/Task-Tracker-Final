# main.py — application entry point.

from fastapi import FastAPI, status

from app.core.config import settings
from app.api.routes.health import router as health_router
from app.models import TaskCreate, TaskResponse
from app import storage

app = FastAPI(
    title="Task Tracker API",
    version="0.1.0",
    description="A learning-focused REST API built with FastAPI and JSON file storage.",
)

app.include_router(health_router)


@app.on_event("startup")
async def on_startup() -> None:
    print(f"[startup] APP_ENV={settings.app_env}  PORT={settings.port}")


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(payload: TaskCreate) -> TaskResponse:
    return storage.add_task(payload)