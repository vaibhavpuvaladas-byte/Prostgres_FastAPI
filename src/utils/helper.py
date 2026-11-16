from fastapi import Request, HTTPException
from sqlalchemy.orm import Session
from src.user.models import UserModel
from src.utils.settings import settings
from src.utils.db import get_db
from fastapi import Depends
import jwt

def is_authenticated(request: Request, db: Session = Depends(get_db)):
    auth_header = request.headers.get("Authorization")
    
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

    return user