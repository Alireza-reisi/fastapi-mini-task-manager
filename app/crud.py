from sqlalchemy.orm import Session
from app import models, schemas
from sqlalchemy import or_


def get_tasks(db: Session, q: str | None = None, is_completed: bool | None = None):
    query = db.query(models.Task)

    if is_completed is not None:
        query = query.filter(models.Task.is_completed == is_completed)

    if q:
        q = q.strip()
        query = query.filter(
            or_(
                models.Task.title.ilike(f"%{q}%"),
                models.Task.description.ilike(f"%{q}%"),
            )
        )

    return query.order_by(models.Task.id.desc()).all()


def create_task(db: Session, task_in: schemas.TaskCreate) -> models.Task:
    task = models.Task(
        title=task_in.title,
        description=task_in.description,
        is_completed=task_in.is_completed,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).one_or_none()


def update_task(db: Session, task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    data = task_in.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def patch_task(db: Session, task: models.Task, task_in: schemas.TaskUpdate) -> models.Task:
    data = task_in.model_dump(exclude_unset=True)

    for key, value in data.items():
        setattr(task, key, value)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task: models.Task) -> None:
    db.delete(task)
    db.commit()