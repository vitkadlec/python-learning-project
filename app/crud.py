from sqlalchemy.orm import Session
from fastapi import HTTPException
import re
from .models import User
from .schemas import UserCreate

def create_user(db: Session, user: UserCreate):

    db_user_by_username = db.query(User).filter(User.username == user.username).first()
    db_user_by_email = db.query(User).filter(User.email == user.email).first()

    if db_user_by_username and db_user_by_email:
        raise HTTPException(status_code=400, detail=f"Username {user.username} and email {user.email} are already taken.")

    if db_user_by_username:
        raise HTTPException(status_code=400, detail=f"Username {user.username} is already taken.")

    if db_user_by_email:
        raise HTTPException(status_code=400, detail=f"Email {user.email} is already in use.")

    db_user = User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    return user

def list_users(db: Session):
    return db.query(User).all()

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
