from fastapi import APIRouter, Depends
from database.connection import get_db
from models.user import User
from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from models.user import User
from passlib.context import CryptContext
from datetime import datetime, timedelta
from services.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from models.todo import Todo

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


router = APIRouter()


@router.get("/")
def read_user(db: Session = Depends(get_db)):
    user = db.query(User).all() 
    return user

@router.get("/{user_id}")
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    return user

# Signup endpoint
@router.post("/signup/")
async def signup(username: str, email: str, password: str, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.add(user)
    db.commit()
    return {"message": "User created successfully"}

# Login endpoint 
@router.post("/login/")
async def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "username": user.username,"email":user.email, "user_id": user.id} 


