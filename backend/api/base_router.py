from fastapi import APIRouter, Depends, HTTPException, Form
from datetime import timedelta
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from database.connection import get_db
from services.auth_utils import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from typing import Annotated

base_router : APIRouter = APIRouter()

@base_router.get("/")
def welcome():
    return "Mubarak, Its Working!"

# Define the password hashing context
pwd_context : CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Login endpoint for token generation
@base_router.post("/token")
def token(username: str = Form(...), password: str = Form(...), db: Session =  Depends(get_db)):
    # Authenticate the user
    user = db.query(User).filter(User.username == username).first()
    if not user or not pwd_context.verify(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    # Generate the access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )

    # Return the access token
    return {"access_token": access_token, "token_type": "bearer"}
