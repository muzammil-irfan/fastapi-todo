from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.todo import Todo
from models.user import User
from services.auth_utils import get_current_user
from datetime import datetime
from typing import Optional, List

router = APIRouter()

@router.get("/")
def read_todo(db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    """
    Retrieve all todos for the current user.
    """
    try:
        todos = db.query(Todo).filter(Todo.owner_id == current_user.id).all()
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{todo_id}")
def read_todo(todo_id: int, db: Session = Depends(get_db), current_user : User = Depends(get_current_user)):
    """
    Retrieve a todo by its ID for the current user.
    """
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def create_todo(
    title: str, description: str, status: str,
    db: Session = Depends(get_db), current_user : User = Depends(get_current_user)
):
    """
    Create a new todo for the current user.
    """
    try:
        new_todo = Todo(
            title=title,
            description=description,
            status=status,
            owner_id=current_user.id,
            created_at=datetime.now()
        )
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)
        return new_todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{todo_id}")
def update_todo(
    todo_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update a todo by its ID for the current user.
    """
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id, Todo.owner_id == current_user.id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if status is not None:
            todo.status = status

        db.commit()
        db.refresh(todo)
        return todo
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Retrieve the todo item from the database
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    # Check if the current user owns the todo item
    if todo.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You don't have permission to delete this todo item")
    
    # Delete the todo item from the database
    db.delete(todo)
    db.commit()
    
    return {"message": "Todo item deleted successfully"}