from datetime import date, datetime, timezone
from typing import Optional
from uuid import uuid4

from app.models import TaskCreate, TaskPriority, TaskResponse, TaskStatus, TaskUpdate

_tasks: dict[str, TaskResponse] = {}


def _compute_overdue(due_date: Optional[date], status: TaskStatus) -> bool:
    if due_date is None:
        return False
    if status == TaskStatus.DONE:
        return False
    return due_date < date.today()


def _with_computed_overdue(task: TaskResponse) -> TaskResponse:
    # is_overdue is never trusted from stored state — always recomputed
    # against today's date so it can't go stale between requests.
    return task.model_copy(update={
        "is_overdue": _compute_overdue(task.due_date, task.status)
    })


def add_task(payload: TaskCreate) -> TaskResponse:
    now = datetime.now(timezone.utc)
    task_id = str(uuid4())
    description = payload.description if payload.description is not None else ""
    task = TaskResponse(
        id=task_id,
        title=payload.title,
        description=description,
        status=payload.status,
        priority=payload.priority,
        assignee=payload.assignee,
        due_date=payload.due_date,
        tags=payload.tags,
        created_at=now,
        updated_at=now,
    )
    _tasks[task_id] = task
    return _with_computed_overdue(task)


def get_all_tasks(
    status: Optional[TaskStatus] = None,
    priority: Optional[TaskPriority] = None,
    overdue: Optional[bool] = None,
    tag: Optional[str] = None,
) -> list[TaskResponse]:
    tasks = list(_tasks.values())
    if status is not None:
        tasks = [t for t in tasks if t.status == status]
    if priority is not None:
        tasks = [t for t in tasks if t.priority == priority]
    if tag is not None:
        tasks = [t for t in tasks if tag in t.tags]

    tasks = [_with_computed_overdue(t) for t in tasks]

    if overdue is not None:
        tasks = [t for t in tasks if t.is_overdue == overdue]

    return tasks


def get_task_by_id(task_id: str) -> Optional[TaskResponse]:
    task = _tasks.get(task_id)
    if task is None:
        return None
    return _with_computed_overdue(task)


def update_task(task_id: str, payload: TaskUpdate) -> Optional[TaskResponse]:
    existing = _tasks.get(task_id)
    if existing is None:
        return None
    updates = payload.model_dump(exclude_unset=True)
    if not updates:
        return _with_computed_overdue(existing)
    now = datetime.now(timezone.utc)
    updated = existing.model_copy(update={**updates, "updated_at": now})
    _tasks[task_id] = updated
    return _with_computed_overdue(updated)


def delete_task(task_id: str) -> bool:
    if task_id not in _tasks:
        return False
    del _tasks[task_id]
    return True


def _reset() -> None:
    _tasks.clear()