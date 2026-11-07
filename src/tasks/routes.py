from fastapi import APIRouter , Depends
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.tasks.controller import create_task
from src.tasks.controller import get_task

task_router = APIRouter(prefix="/tasks")
@task_router.post("/create")
def create_new_task_route(body: TaskSchema, db: Session = Depends(get_db)):
    return create_task(body, db)


@task_router.get("/all_tasks")
def get_all_tasks_route(db: Session = Depends(get_db)):
    return get_task(db)