from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, status

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPatchStatus
from ..models.user import User


def create_todo(session: Session, todo_create: TodoCreate, user_id: str) -> Todo:
    """
    Create a new todo for the authenticated user.
    """
    # Create the todo with the user_id
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed,
        user_id=user_id
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def get_todos_by_user(session: Session, user_id: str) -> List[Todo]:
    """
    Get all todos for the authenticated user.
    """
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos


def get_todo_by_id_and_user(session: Session, todo_id: str, user_id: str) -> Optional[Todo]:
    """
    Get a specific todo by its ID and ensure it belongs to the user.
    """
    statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo


def update_todo(session: Session, todo_id: str, todo_update: TodoUpdate, user_id: str) -> Optional[Todo]:
    """
    Update a specific todo if it belongs to the user.
    """
    todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not todo:
        return None

    # Update only the fields that are provided
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(todo, field, value)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def delete_todo(session: Session, todo_id: str, user_id: str) -> bool:
    """
    Delete a specific todo if it belongs to the user.
    """
    todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not todo:
        return False

    session.delete(todo)
    session.commit()

    return True


def update_todo_status(session: Session, todo_id: str, status_update: TodoPatchStatus, user_id: str) -> Optional[Todo]:
    """
    Update the completion status of a specific todo if it belongs to the user.
    """
    todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not todo:
        return None

    todo.completed = status_update.completed

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo