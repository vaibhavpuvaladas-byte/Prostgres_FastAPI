from fastapi import APIRouter , Depends
from src.tasks.dtos import TaskSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.tasks.controller import create_task
from src.tasks.controller import get_task
from src.tasks.controller import get_task_by_id
from src.tasks.controller import update_task
from src.tasks.controller import delete_task
from src.utils.helper import is_authenticated
from src.user.models import UserModel

task_router = APIRouter(prefix="/tasks")
@task_router.post("/create")
def create_new_task_route(body: TaskSchema, db: Session = Depends(get_db) , user : UserModel = Depends(is_authenticated)):
    return create_task(body, db)


@task_router.get("/all_tasks")
def get_all_tasks_route(db: Session = Depends(get_db)):
    return get_task(db)

@task_router.get("/get_task/{task_id}")
def get_one_task(task_id:int, db:Session = Depends(get_db) ,  user : UserModel = Depends(is_authenticated)):
    return get_task_by_id(task_id, db)

@task_router.put("/update_task/{task_id}")
def update_task_route(body: TaskSchema, task_id:int, db: Session = Depends(get_db) ,  user : UserModel = Depends(is_authenticated)):
    return update_task(body, task_id, db)

@task_router.delete("/delete_task/{task_id}")
def delete_task_route(task_id:int, db: Session = Depends(get_db) ,  user : UserModel = Depends(is_authenticated)):
    return delete_task(task_id, db)