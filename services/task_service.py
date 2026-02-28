from sqlmodel import Session, select
from models.task import Task
from models.user import User
from fastapi import HTTPException

def create_task(task: Task, session: Session, user: User) -> Task:
    task.user_id = user.id
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_task_by_id(task_id: int, session: Session, user: User) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    elif task.user_id != user.id:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

def update_task(task_id: int, updated: Task, session: Session, user: User) -> Task:
    task = get_task_by_id(task_id, session, user)
    task.title = updated.title
    task.description = updated.description
    task.completed = updated.completed
    session.commit()
    session.refresh(task)
    return task

def delete_task(task_id: int, session: Session, user: User) -> None:
    task = get_task_by_id(task_id, session, user)
    session.delete(task)
    session.commit()

def list_tasks(session: Session, user: User, completed: bool | None = None) -> list[Task]:
    query = select(Task).where(Task.user_id == user.id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    return session.exec(query).all()

def list_tasks_paginated(
    session: Session,
    user: User,
    completed: bool | None = None,
    limit: int = 10,
    offset: int = 0
) -> list[Task]:
    query = select(Task).where(Task.user_id == user.id)
    if completed is not None:
        query = query.where(Task.completed == completed)
    query = query.offset(offset).limit(limit)
    return session.exec(query).all()