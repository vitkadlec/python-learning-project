from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import engine, Base, get_db
from .schemas import UserCreate, UserRead
from .crud import create_user, get_user, list_users, delete_user

app = FastAPI()

Base.metadata.create_all(bind=engine)


@app.post("/users/", response_model=UserRead)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@app.get("/users/{user_id}", response_model=UserRead)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return get_user(db, user_id)


@app.get("/users/", response_model=list[UserRead])
def list_users_endpoint(db: Session = Depends(get_db)):
    return list_users(db)


@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
