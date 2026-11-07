from src.tasks.dtos import TaskSchema
from sqlalchemy.orm import Session
from src.tasks.models import TaskModel

'''here is where the logic goes'''

def create_task(body:TaskSchema, db:Session):

    data = body.model_dump()
    new_task = TaskModel(title = data["title"], description = data["description"], is_completed = data["is_completed"])
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return {"message": "Task created successfully", "task": new_task}

def get_task(db:Session):
    tasks = db.query(TaskModel).all()
    return {"message": "Tasks retrieved successfully", "tasks": tasks}

