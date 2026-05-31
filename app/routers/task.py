from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import crud, schemas

router = APIRouter()


@router.get("/", response_model=list[schemas.TaskOut])
def read_tasks(
    params: schemas.TaskQueryParams = Depends(),
    db: Session = Depends(get_db),
    ):
    return crud.get_tasks(db=db, q=params.q, is_completed=params.is_completed)


@router.post("/", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task(db, task_in)


@router.get("/{task_id}", response_model=schemas.TaskOut)
def read_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return crud.update_task(db, task, task_in)

@router.patch("/{task_id}", response_model=schemas.TaskOut)
def patch_task(task_id: int, task_in: schemas.TaskUpdate, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if not task_in.model_dump(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields provided for update")

    return crud.patch_task(db, task, task_in)

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    crud.delete_task(db, task)
    return None
