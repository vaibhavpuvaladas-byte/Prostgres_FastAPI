from argon2 import hash_password
from fastapi import HTTPException 
from src.user.dtos import UserSchema
from src.user.dtos import LoginSchema
from sqlalchemy.orm import Session
from src.user.models import UserModel
from pwdlib import PasswordHash
import jwt
from src.utils.settings import settings
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()
def get_password_hash(password):
    return password_hash.hash(password)


def register_user(body:UserSchema, db:Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()
    if is_user:
        return {"message": "User already exists"}

    is_email = db.query(UserModel).filter(UserModel.email == body.email).first()
    if is_email:
        return {"message": "Email already exists"}

    hash_password = get_password_hash(body.password)
    
    new_user = UserModel(name=body.name, username=body.username, email=body.email, hash_password=hash_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User registered successfully", "user": body}


def login_user(body:LoginSchema, db:Session):
    is_user = db.query(UserModel).filter(UserModel.username == body.username).first()

    if not is_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not password_hash.verify(body.password, is_user.hash_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    EXP_TIME_MINUTES = settings.EXP_TIME_MINUTES
    expiration_time = datetime.utcnow() + timedelta(minutes=EXP_TIME_MINUTES)
    token = jwt.encode({"username": is_user.username , "_id": is_user.id, "exp": expiration_time}, settings.secret_key, settings.algorithm)
    
    return {"message": "User logged in successfully", "user": body, "token": token}
