from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime

from ..models.todo import Todo, TodoCreate, TodoRead, TodoUpdate, TodoPatchStatus, RecurrenceType
from ..models.user import User
from ..database.database import get_session
from ..middleware.auth import get_current_active_user
from ..services.todo_service import TodoService
from ..events.publisher import InMemoryEventPublisher # Using In-memory for now

todo_router = APIRouter()

# Instantiate event publisher (could be a dependency in a more complex setup)
event_publisher = InMemoryEventPublisher()

@todo_router.post("/todos", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_new_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the authenticated user.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        todo = todo_service.create_todo(session, str(current_user.id), todo_create)
        return todo
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the todo"
        )


@todo_router.get("/todos", response_model=List[TodoRead])
def read_todos(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    search: Optional[str] = None,
    priority: Optional[str] = None,
    tags: Optional[str] = None,
    due_date_from: Optional[str] = None,
    due_date_to: Optional[str] = None,
    completed: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None
):
    """
    Get all todos for the authenticated user with optional search, filtering, and sorting.
    """
    try:
        # Convert date strings to datetime objects if provided
        due_date_from_dt = None
        due_date_to_dt = None
        if due_date_from:
            from datetime import datetime
            due_date_from_dt = datetime.fromisoformat(due_date_from.replace('Z', '+00:00'))
        if due_date_to:
            from datetime import datetime
            due_date_to_dt = datetime.fromisoformat(due_date_to.replace('Z', '+00:00'))

        todo_service = TodoService(session=session, event_publisher=event_publisher)
        todos = todo_service.get_todos_by_user(
            session,
            str(current_user.id),
            search=search,
            completed=completed,
            priority=priority,
            tags=tags,
            due_date_from=due_date_from_dt,
            due_date_to=due_date_to_dt,
            sort=sort,
            order=order
        )
        return todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving todos"
        )


@todo_router.put("/todos/{todo_id}", response_model=TodoRead)
def update_existing_todo(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update an existing todo for the authenticated user.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        updated_todo = todo_service.update_todo(session, todo_id, str(current_user.id), todo_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the todo"
        )


@todo_router.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_todo(
    todo_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Delete a todo for the authenticated user.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        success = todo_service.delete_todo(session, todo_id, str(current_user.id))
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        # Return 204 No Content on successful deletion
        return
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while deleting the todo"
        )


@todo_router.patch("/todos/{todo_id}/status", response_model=TodoRead)
def update_todo_completion_status(
    todo_id: str,
    status_update: TodoPatchStatus,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Update the completion status of a todo for the authenticated user.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        updated_todo = todo_service.update_todo_status(session, todo_id, str(current_user.id), status_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the todo status"
        )

# --- New Endpoints for Advanced Todo Features ---

class RecurrenceSettings(TodoUpdate):
    recurrence_type: RecurrenceType = RecurrenceType.NONE
    recurrence_interval: Optional[int] = None

class DueDateUpdate(TodoUpdate):
    due_date: Optional[datetime] = None

class ReminderUpdate(TodoUpdate):
    reminder_at: Optional[datetime] = None

@todo_router.put("/todos/{todo_id}/recurrence", response_model=TodoRead)
def set_todo_recurrence(
    todo_id: str,
    recurrence_settings: RecurrenceSettings,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Set or update recurrence settings for a task.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        # Create a TodoUpdate object with only the recurrence fields
        todo_update = TodoUpdate(
            recurrence_type=recurrence_settings.recurrence_type,
            recurrence_interval=recurrence_settings.recurrence_interval
        )
        updated_todo = todo_service.update_todo(session, todo_id, str(current_user.id), todo_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while setting recurrence: {e}"
        )

@todo_router.delete("/todos/{todo_id}/recurrence", response_model=TodoRead)
def remove_todo_recurrence(
    todo_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Remove recurrence settings from a task.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        # Set recurrence fields to None to remove them
        todo_update = TodoUpdate(
            recurrence_type=RecurrenceType.NONE,
            recurrence_interval=None,
            next_occurrence=None # Also clear next_occurrence
        )
        updated_todo = todo_service.update_todo(session, todo_id, str(current_user.id), todo_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while removing recurrence: {e}"
        )

@todo_router.put("/todos/{todo_id}/due-date", response_model=TodoRead)
def set_todo_due_date(
    todo_id: str,
    due_date_update: DueDateUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Set or update due date for a task.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        todo_update = TodoUpdate(due_date=due_date_update.due_date)
        updated_todo = todo_service.update_todo(session, todo_id, str(current_user.id), todo_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while setting due date: {e}"
        )

@todo_router.put("/todos/{todo_id}/reminder", response_model=TodoRead)
def set_todo_reminder(
    todo_id: str,
    reminder_update: ReminderUpdate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session)
):
    """
    Configure reminder for a task.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        todo_update = TodoUpdate(reminder_at=reminder_update.reminder_at)
        updated_todo = todo_service.update_todo(session, todo_id, str(current_user.id), todo_update)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo not found or doesn't belong to user"
            )
        return updated_todo
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while setting reminder: {e}"
        )

@todo_router.get("/todos/upcoming", response_model=List[TodoRead])
def get_upcoming_todos(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
    days_ahead: int = Query(7, description="Number of days to look ahead for due tasks"),
    include_overdue: bool = Query(False, description="Whether to include overdue tasks")
):
    """
    Get upcoming tasks with due dates.
    """
    try:
        todo_service = TodoService(session=session, event_publisher=event_publisher)
        upcoming_todos = todo_service.get_upcoming_tasks(
            session,
            str(current_user.id),
            days_ahead=days_ahead,
            include_overdue=include_overdue
        )
        return upcoming_todos
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while retrieving upcoming todos: {e}"
        )