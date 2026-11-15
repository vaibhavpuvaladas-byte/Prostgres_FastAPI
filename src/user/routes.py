from fastapi import APIRouter , Depends , status , Request
from sqlalchemy.orm import Session
from src.tasks.controller import create_task, get_task, get_task_by_id, update_task, delete_task
from src.utils.db import get_db
from src.user.dtos import UserSchema , UserResponseSchema , LoginSchema
from src.user import controller

user_router = APIRouter(prefix="/user")

@user_router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return controller.register_user(body, db)

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: LoginSchema, db: Session = Depends(get_db)):
    return controller.login_user(body, db)

@user_router.get("/auth", status_code=status.HTTP_200_OK)
def is_auth(request: Request,db: Session = Depends(get_db)):
    return controller.is_authenticated(request, db)