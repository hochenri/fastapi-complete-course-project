from fastapi import APIRouter, Depends
from sqlmodel import Session
from db import get_session
from models.task import Task
from models.user import User
from services import task_service
from core.dependencies import require_active_user, get_current_user

# import broadcast
from routers.ws import broadcast

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.get("/", dependencies=[Depends(require_active_user)])
def get_all(completed: bool | None = None, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return task_service.list_tasks(session, user,  completed)

@router.get("/paginated", dependencies=[Depends(require_active_user)])
def get_paginated(
    completed: bool | None = None,
    limit: int = 10,
    offset: int = 0,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user)
):
    return task_service.list_tasks_paginated(session, user, completed, limit, offset)

@router.get("/{task_id}", dependencies=[Depends(require_active_user)])
def get_one(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    return task_service.get_task_by_id(task_id, session, user)

@router.post("/", status_code=201, dependencies=[Depends(require_active_user)])
async def create(task: Task, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    await broadcast(f"Task created: {task.title}")
    return task_service.create_task(task, session, user)

@router.put("/{task_id}", dependencies=[Depends(require_active_user)])
async def update(task_id: int, updated: Task, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    await broadcast(f"Task {task_id} updated")
    return task_service.update_task(task_id, updated, session, user)

@router.delete("/{task_id}", status_code=204, dependencies=[Depends(require_active_user)])
def delete(task_id: int, session: Session = Depends(get_session), user: User = Depends(get_current_user)):
    task_service.delete_task(task_id, session, user)