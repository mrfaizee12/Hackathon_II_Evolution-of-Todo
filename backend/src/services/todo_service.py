from sqlmodel import Session, select
from typing import List, Optional
from fastapi import HTTPException, status
from datetime import datetime

from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoPatchStatus
from ..models.user import User


def create_todo(session: Session, todo_create: TodoCreate, user_id: str) -> Todo:
    """
    Create a new todo for the authenticated user.
    """
    # Process tags to ensure they are properly formatted (comma-separated)
    processed_tags = ""
    if todo_create.tags:
        tag_list = [tag.strip() for tag in todo_create.tags.split(',') if tag.strip()]
        processed_tags = ",".join(tag_list)

    # Create the todo with the user_id
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed,
        priority=todo_create.priority,
        tags=processed_tags,
        due_date=todo_create.due_date,
        user_id=user_id
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    return todo


def get_todos_by_user(
    session: Session,
    user_id: str,
    search: Optional[str] = None,
    completed: Optional[bool] = None,
    priority: Optional[str] = None,
    tags: Optional[str] = None,
    due_date_from: Optional[datetime] = None,
    due_date_to: Optional[datetime] = None,
    sort: Optional[str] = "created_at",
    order: Optional[str] = "desc"
) -> List[Todo]:
    """
    Get all todos for the authenticated user with filtering, searching, and sorting.
    """
    statement = select(Todo).where(Todo.user_id == user_id)

    # Filter by completion status
    if completed is not None:
        statement = statement.where(Todo.completed == completed)

    # Filter by priority
    if priority:
        statement = statement.where(Todo.priority == priority)

    # Filter by tags (tags are stored as comma-separated string)
    if tags:
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        for tag in tag_list:
            statement = statement.where(Todo.tags.ilike(f"%{tag}%"))

    # Filter by due date range
    if due_date_from:
        statement = statement.where(Todo.due_date >= due_date_from)
    if due_date_to:
        statement = statement.where(Todo.due_date <= due_date_to)

    # Search by keyword (title or description)
    if search:
        search_filter = f"%{search}%"
        statement = statement.where(
            (Todo.title.ilike(search_filter)) | (Todo.description.ilike(search_filter))
        )

    # Sorting logic
    if sort in ["priority", "created_at", "due_date", "title"]:
        sort_attr = getattr(Todo, sort)
    else:
        sort_attr = Todo.created_at  # Default to created_at

    if order == "desc":
        statement = statement.order_by(sort_attr.desc())
    else:
        statement = statement.order_by(sort_attr.asc())

    todos = session.exec(statement).all()
    return todos


def get_todo_by_id_and_user(session: Session, todo_id: str, user_id: str) -> Optional[Todo]:
    """
    Get a specific todo by its ID and ensure it belongs to the user.
    """
    statement = select(Todo).where(Todo.id == todo_id).where(Todo.user_id == user_id)
    todo = session.exec(statement).first()
    return todo


def update_todo(session: Session, todo_id: str, todo_update: TodoUpdate, user_id: str) -> Optional[Todo]:
    """
    Update a specific todo if it belongs to the user.
    """
    todo = get_todo_by_id_and_user(session, todo_id, user_id)
    if not todo:
        return None

    # Process tags if they are being updated
    if todo_update.tags is not None:
        tag_list = [tag.strip() for tag in todo_update.tags.split(',') if tag.strip()]
        processed_tags = ",".join(tag_list)
        todo.tags = processed_tags

    # Update only the other fields that are provided
    update_data = todo_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if field != 'tags':  # Skip tags since we handled it separately
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