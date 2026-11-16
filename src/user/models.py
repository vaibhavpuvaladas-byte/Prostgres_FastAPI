from sqlalchemy import Column, Integer, String, Boolean
from src.utils.db import Base


class UserModel(Base):
    __tablename__ = "users_table"  
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    username = Column(String(100), nullable=False)
    hash_password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

