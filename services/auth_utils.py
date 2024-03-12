# auth_utils.py

from datetime import datetime, timedelta
from typing import Optional
from fastapi.security import OAuth2PasswordBearer
import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from models.user import User
from database.connection import get_db
from fastapi import Depends, HTTPException, status

# Define OAuth2 password bearer for token-based authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Set environment variables or a secret key for your application
SECRET_KEY = "fksjdkfs"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize password hashing library
pwd_context = CryptContext(schemes=["bcrypt"])


# Create access token
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Function to verify JWT token
def verify_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        # Decode the JWT token
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
 
        # Retrieve user from the database based on the username extracted from the token
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Middleware for user verification
def get_current_user(user: User = Depends(verify_token)):
    return user

