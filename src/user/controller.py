from argon2 import hash_password
from fastapi import HTTPException , Request 
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
    expiration_time = datetime.now() + timedelta(minutes=EXP_TIME_MINUTES)
    token = jwt.encode({"username": is_user.username , "_id": is_user.id, "exp": expiration_time}, settings.secret_key, settings.algorithm)
    
    return {"message": "User logged in successfully", "user": body, "token": token}


def is_authenticated(request: Request, db: Session):
    auth_header = request.headers.get("Authorization")
    
    # Fix: Explicitly check if the header exists and is formatted correctly
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    
    token = auth_header.split(" ")[1]

    # Fix: Wrap decode in a try/except to gracefully catch PyJWT errors
    try:
        data = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

    # PyJWT already verified the expiration, so we just check the database
    user = db.query(UserModel).filter(UserModel.username == data.get("username")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User is authenticated", "user": {"username": user.username, "id": user.id , "name": user.name, "email": user.email}}