from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import Base

SQLALCHEMY_DATABASE_URL = "postgresql://muzammil-irfan:Wb1B0PjaxykM@ep-bold-credit-a421szht.us-east-1.aws.neon.tech/neondb?sslmode=require"

engine = create_engine(SQLALCHEMY_DATABASE_URL)


# Function to create a database session
def get_session():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()

def create_database():
    get_session()
    Base.metadata.create_all(bind=engine)