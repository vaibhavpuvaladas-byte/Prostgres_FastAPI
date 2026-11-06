from fastapi import FastAPI
from src.utils.db import Base , engine
from src.tasks.models import TaskModel
from src.tasks.routes import task_router

app = FastAPI()
Base.metadata.create_all(engine)

'Includes the task_router to the FastAPI application, allowing it to handle requests related to tasks.'
app.include_router(task_router) 
