from sqlalchemy.orm import Session
from . import models

# Function to retrieve all users from the database
def get_users(db: Session):
    return db.query(models.User).all()
