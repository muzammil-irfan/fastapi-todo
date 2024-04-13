# Import necessary modules
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from . import Base

# Define Todo model
class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    status = Column(String, default="progress") # progress, complete
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime)

    # Relationship with users
    owner = relationship("User", back_populates="todo_items")
