from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel
from fastapi import HTTPException
from src.utils.helper import is_authenticated
from src.user.models import UserModel
from fastapi import Depends

'''here is where the logic goes'''


def _get_user_id(user):
    if hasattr(user, "id") and not isinstance(user, dict):
        return user.id
    if isinstance(user, dict):
        return user.get("user", {}).get("id", user.get("id"))
    return getattr(user, "id", None)


def create_task(body:TaskSchema, db:Session , user : UserModel):

    data = body.model_dump()
    user_id = _get_user_id(user)
    new_task = TaskModel(title = data["title"], description = data["description"], is_completed = data["is_completed"] , user_id = user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}

def get_task(db:Session, user: UserModel):
    user_id = _get_user_id(user)
    tasks = db.query(TaskModel).filter(TaskModel.user_id == user_id).all()
    return {"message": "Tasks retrieved successfully", "tasks": tasks}

def get_task_by_id(task_id:int, db:Session , user : UserModel):
    user_id = _get_user_id(user)
    task = db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
    if task:
        return {"message": "Task retrieved successfully", "task": task}
    else:
        return {"message": "Task not found", "task": None}


def update_task(body:TaskSchema , task_id:int , db:Session , user : UserModel):
    user_id = _get_user_id(user)
    one_task=db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
    if not one_task:
        raise HTTPException(status_code=404, detail="Task not found")
    body = body.model_dump()
    for field , value in body.items():
        setattr(one_task, field, value)

    db.add(one_task)
    db.commit()
    db.refresh(one_task)
    return {"message": "Task updated successfully", "task": one_task}

def delete_task(task_id:int, db:Session , user : UserModel):
    user_id = _get_user_id(user)
    task =db.query(TaskModel).filter(TaskModel.id == task_id, TaskModel.user_id == user_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted successfully"}

