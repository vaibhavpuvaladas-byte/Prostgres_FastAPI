from fastapi import FastAPI
from src.utils.db import Base , engine
from src.tasks.models import TaskModel

app = FastAPI()
Base.metadata.create_all(engine)