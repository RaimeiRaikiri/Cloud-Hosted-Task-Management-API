from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import app.database_models as database_models
from app.database import get_db
from app.models import TaskCreate, TaskResponse, TaskUpdate, User
from app.routers.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["Tasks"])

db = Annotated[Session, Depends(get_db)]
current_user = Annotated[User, Depends(get_current_user)]


@router.get("/", response_model=list[TaskResponse])
def get_tasks(db: db, current_user: current_user):
    # Number of tasks of a given current user
    number_of_tasks = (
        db.query(database_models.Task)
        .filter(database_models.Task.user_id == current_user.id)
        .count()
    )

    if number_of_tasks > 0:
        db_tasks = (
            db.query(database_models.Task)
            .filter(database_models.Task.user_id == current_user.id)
            .all()
        )

        return db_tasks
    else:
        return []


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: db, current_user: current_user):

    task_in_db = (
        db.query(database_models.Task)
        .filter(database_models.Task.id == task_id)
        .first()
    )

    if not task_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )

    if task_in_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed access to this task",
        )

    return task_in_db


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TaskResponse)
def create_task(task: TaskCreate, db: db, current_user: current_user):

    new_task = database_models.Task(
        **task.model_dump(),
        completed=False,
        user_id=current_user.id,
        created_at=datetime.now(timezone.utc),
    )

    try:
        db.add(new_task)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid task data"
        )

    db.refresh(new_task)

    return TaskResponse.model_validate(new_task)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskUpdate, db: db, current_user: current_user):

    task_in_db = (
        db.query(database_models.Task)
        .filter(database_models.Task.id == task_id)
        .first()
    )

    if not task_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )

    if task_in_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to update this task",
        )

    if task.title:
        task_in_db.title = task.title
    if task.description:
        task_in_db.description = task.description
    if task.completed is not None:
        task_in_db.completed = task.completed

    db.commit()

    return task_in_db


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: db, current_user: current_user):

    task_in_db = (
        db.query(database_models.Task)
        .filter(database_models.Task.id == task_id)
        .first()
    )

    if not task_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found"
        )

    if task_in_db.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not allowed to delete this task",
        )

    db.delete(task_in_db)
    db.commit()

    return None
