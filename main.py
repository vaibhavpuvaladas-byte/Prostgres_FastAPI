from fastapi import FastAPI
from src.utils.db import Base , engine
from src.tasks.models import TaskModel
from src.tasks.routes import task_router
from src.user.routes import user_router

app = FastAPI()
Base.metadata.create_all(engine)

'Includes the task_router to the FastAPI application, allowing it to handle requests related to tasks.'
app.include_router(task_router) 

app.include_router(user_router)  # Assuming user_router is defined in src/user/routes.py

