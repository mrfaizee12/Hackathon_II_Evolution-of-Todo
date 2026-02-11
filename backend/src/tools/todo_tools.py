"""
MCP (Model Context Protocol) Tools for AI Todo Management
These tools allow the AI agent to perform todo operations through function calling.
"""

from typing import List, Optional
from pydantic import BaseModel, Field 
from sqlmodel import Session, select
from ..models.todo import Todo, TodoCreate, TodoUpdate, RecurrenceType
from ..services.todo_service import TodoService
from datetime import datetime # Import datetime for parsing due_date

class AddTaskInput(BaseModel):
    """Input for adding a new task."""
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    tags: Optional[str] = ""
    due_date: Optional[str] = None  # ISO format date string
    ai_context: Optional[str] = "Added via AI assistant"
    # New recurrence fields for addTask
    recurrence_type: Optional[str] = "none" # "none", "daily", "weekly", "monthly"
    recurrence_interval: Optional[int] = None


class UpdateTaskInput(BaseModel):
    """Input for updating an existing task."""
    task_id: str  # UUID string
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[str] = None  # ISO format date string
    ai_context: Optional[str] = "Updated via AI assistant"
    # New recurrence fields for updateTask
    recurrence_type: Optional[str] = None # "none", "daily", "weekly", "monthly"
    recurrence_interval: Optional[int] = None


class CompleteTaskInput(BaseModel):
    """Input for completing a task."""
    task_id: str  # UUID string
    completed: bool = True


class DeleteTaskInput(BaseModel):
    """Input for deleting a task."""
    task_id: str  # UUID string


class ListTasksInput(BaseModel):
    """Input for listing tasks."""
    status: Optional[str] = None  # "all", "pending", "completed"
    limit: Optional[int] = 100
    offset: Optional[int] = 0

class SetRecurrenceInput(BaseModel):
    """Input for setting recurrence for a task."""
    task_id: str
    recurrence_type: str # "none", "daily", "weekly", "monthly"
    recurrence_interval: Optional[int] = None

class RemoveRecurrenceInput(BaseModel):
    """Input for removing recurrence from a task."""
    task_id: str

class SetDueDateInput(BaseModel):
    """Input for setting or updating the due date of a task."""
    task_id: str
    due_date: str # ISO format date string

class ListUpcomingTasksInput(BaseModel):
    """Input for listing upcoming tasks."""
    days_ahead: Optional[int] = Field(7, description="Number of days to look ahead for due tasks")
    include_overdue: Optional[bool] = Field(False, description="Whether to include overdue tasks")

class SetReminderInput(BaseModel):
    """Input for setting or updating the reminder time for a task."""
    task_id: str
    reminder_at: str # ISO format date string


def add_task(input_data: AddTaskInput, user_id: str, db_session: Session) -> dict:
    """
    Add a new task using the AI assistant.

    Args:
        input_data: Contains task details
        user_id: ID of the user creating the task
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        # Create todo data
        todo_data = TodoCreate(
            title=input_data.title,
            description=input_data.description,
            priority=input_data.priority,
            tags=input_data.tags,
            ai_generated=True,
            ai_context=input_data.ai_context,
            recurrence_type=RecurrenceType(input_data.recurrence_type), # Convert str to Enum
            recurrence_interval=input_data.recurrence_interval
        )

        # If due_date is provided, parse it
        if input_data.due_date:
            todo_data.due_date = datetime.fromisoformat(input_data.due_date.replace('Z', '+00:00'))

        # Use the existing TodoService to create the task
        todo_service = TodoService(db_session) # Pass db_session to service constructor
        created_todo = todo_service.create_todo(db_session, user_id, todo_data)

        return {
            "success": True,
            "message": "✅ Task added successfully.",
            "task_id": str(created_todo.id),
            "task_title": created_todo.title
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to add task: {str(e)}"
        }


def list_tasks(input_data: ListTasksInput, user_id: str, db_session: Session) -> dict:
    """
    List tasks for the user.

    Args:
        input_data: Contains filtering options
        user_id: ID of the user whose tasks to list
        db_session: Database session

    Returns:
        Dictionary with list of tasks
    """
    try:
        # Use the existing TodoService to get tasks
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # Prepare filters based on input
        filters = {}
        if input_data.status == "pending":
            filters["completed"] = False
        elif input_data.status == "completed":
            filters["completed"] = True

        # Get all todos for the user with filters
        statement = select(Todo).where(Todo.user_id == user_id)

        if "completed" in filters:
            statement = statement.where(Todo.completed == filters["completed"])

        statement = statement.offset(input_data.offset).limit(input_data.limit)
        results = db_session.exec(statement).all()

        tasks = []
        for todo in results:
            task_info = {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority,
                "tags": todo.tags,
                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                "created_at": todo.created_at.isoformat(),
                "recurrence_type": todo.recurrence_type,
                "recurrence_interval": todo.recurrence_interval,
                "next_occurrence": todo.next_occurrence.isoformat() if todo.next_occurrence else None,
                "reminder_at": todo.reminder_at.isoformat() if todo.reminder_at else None,
            }
            tasks.append(task_info)

        return {
            "success": True,
            "message": f"Retrieved {len(tasks)} tasks",
            "tasks": tasks,
            "total_count": len(tasks)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list tasks: {str(e)}"
        }


def update_task(input_data: UpdateTaskInput, user_id: str, db_session: Session) -> dict:
    """
    Update an existing task.

    Args:
        input_data: Contains task ID and updates
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        # Use the existing TodoService to update the task
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # First, verify the task belongs to the user
        statement = select(Todo).where(Todo.id == input_data.task_id, Todo.user_id == user_id)
        todo = db_session.exec(statement).first()

        if not todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }

        # Prepare update data
        update_data = TodoUpdate(
            title=input_data.title,
            description=input_data.description,
            completed=input_data.completed,
            priority=input_data.priority,
            tags=input_data.tags,
            ai_context=input_data.ai_context,
            recurrence_type=RecurrenceType(input_data.recurrence_type) if input_data.recurrence_type else None,
            recurrence_interval=input_data.recurrence_interval
        )

        # If due_date is provided, parse it
        if input_data.due_date:
            update_data.due_date = datetime.fromisoformat(input_data.due_date.replace('Z', '+00:00'))

        # Update the task
        updated_todo = todo_service.update_todo(db_session, input_data.task_id, user_id, update_data)

        return {
            "success": True,
            "message": "✏️ Task updated successfully.",
            "task_id": str(updated_todo.id),
            "task_title": updated_todo.title
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update task: {str(e)}"
        }


def complete_task(input_data: CompleteTaskInput, user_id: str, db_session: Session) -> dict:
    """
    Mark a task as completed or uncompleted.

    Args:
        input_data: Contains task ID and completion status
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        # Use the existing TodoService to update the task
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # First, verify the task belongs to the user
        statement = select(Todo).where(Todo.id == input_data.task_id, Todo.user_id == user_id)
        todo = db_session.exec(statement).first()

        if not todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }

        # Prepare update data
        update_data = TodoUpdate(completed=input_data.completed)

        # Update the task
        updated_todo = todo_service.update_todo_status(db_session, input_data.task_id, user_id, update_data) # Use update_todo_status

        return {
            "success": True,
            "message": "✅ Task marked as completed.",
            "task_id": str(updated_todo.id),
            "task_title": updated_todo.title,
            "completed": updated_todo.completed
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to update task completion: {str(e)}"
        }


def delete_task(input_data: DeleteTaskInput, user_id: str, db_session: Session) -> dict:
    """
    Delete a task.

    Args:
        input_data: Contains task ID to delete
        user_id: ID of the user whose task to delete
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        # Use the existing TodoService to delete the task
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # First, verify the task belongs to the user
        statement = select(Todo).where(Todo.id == input_data.task_id, Todo.user_id == user_id)
        todo = db_session.exec(statement).first()

        if not todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }

        # Delete the task
        todo_service.delete_todo(db_session, input_data.task_id, user_id)

        return {
            "success": True,
            "message": "🗑️ Task deleted successfully.",
            "task_id": input_data.task_id
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }


def get_all_tasks(user_id: str, db_session: Session) -> dict:
    """
    Get all tasks for a user.

    Args:
        user_id: ID of the user whose tasks to retrieve
        db_session: Database session

    Returns:
        Dictionary with list of all tasks
    """
    try:
        # Use the existing TodoService to get tasks
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # Get all todos for the user
        statement = select(Todo).where(Todo.user_id == user_id)
        results = db_session.exec(statement).all()

        tasks = []
        for todo in results:
            task_info = {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority,
                "tags": todo.tags,
                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                "created_at": todo.created_at.isoformat(),
                "recurrence_type": todo.recurrence_type,
                "recurrence_interval": todo.recurrence_interval,
                "next_occurrence": todo.next_occurrence.isoformat() if todo.next_occurrence else None,
                "reminder_at": todo.reminder_at.isoformat() if todo.reminder_at else None,
            }
            tasks.append(task_info)

        return {
            "success": True,
            "message": f"Retrieved {len(tasks)} tasks",
            "tasks": tasks,
            "total_count": len(tasks)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to retrieve all tasks: {str(e)}"
        }


def mark_task_done(task_id: str, user_id: str, db_session: Session) -> dict:
    """
    Mark a task as done/completed.

    Args:
        task_id: ID of the task to mark as done
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        # Use the existing TodoService to update the task
        todo_service = TodoService(db_session) # Pass db_session to service constructor

        # First, verify the task belongs to the user
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = db_session.exec(statement).first()

        if not todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }

        # Prepare update data to mark as completed
        update_data = TodoUpdate(completed=True)

        # Update the task
        updated_todo = todo_service.update_todo_status(db_session, task_id, user_id, update_data) # Use update_todo_status

        return {
            "success": True,
            "message": f"Successfully marked task '{updated_todo.title}' as done",
            "task_id": str(updated_todo.id),
            "task_title": updated_todo.title,
            "completed": updated_todo.completed
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to mark task as done: {str(e)}"
        }

def set_task_recurrence(input_data: SetRecurrenceInput, user_id: str, db_session: Session) -> dict:
    """
    Set or update recurrence settings for a task.

    Args:
        input_data: Contains task ID, recurrence type, and interval
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        todo_service = TodoService(db_session)
        # Create a TodoUpdate object with only the recurrence fields
        todo_update = TodoUpdate(
            recurrence_type=RecurrenceType(input_data.recurrence_type),
            recurrence_interval=input_data.recurrence_interval
        )
        updated_todo = todo_service.update_todo(db_session, input_data.task_id, user_id, todo_update)
        if not updated_todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }
        return {
            "success": True,
            "message": f"✅ Recurrence set for task '{updated_todo.title}'. Type: {updated_todo.recurrence_type}, Interval: {updated_todo.recurrence_interval}",
            "task_id": str(updated_todo.id),
            "recurrence_type": updated_todo.recurrence_type
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to set task recurrence: {str(e)}"
        }

def remove_task_recurrence(input_data: RemoveRecurrenceInput, user_id: str, db_session: Session) -> dict:
    """
    Remove recurrence settings from a task.

    Args:
        input_data: Contains task ID
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        todo_service = TodoService(db_session)
        todo_update = TodoUpdate(
            recurrence_type=RecurrenceType.NONE,
            recurrence_interval=None,
            next_occurrence=None
        )
        updated_todo = todo_service.update_todo(db_session, input_data.task_id, user_id, todo_update)
        if not updated_todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }
        return {
            "success": True,
            "message": f"✅ Recurrence removed from task '{updated_todo.title}'.",
            "task_id": str(updated_todo.id),
            "recurrence_type": updated_todo.recurrence_type
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to remove task recurrence: {str(e)}"
        }

def set_task_due_date(input_data: SetDueDateInput, user_id: str, db_session: Session) -> dict:
    """
    Set or update the due date for a task.

    Args:
        input_data: Contains task ID and new due date
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        todo_service = TodoService(db_session)
        todo_update = TodoUpdate(due_date=datetime.fromisoformat(input_data.due_date.replace('Z', '+00:00')))
        updated_todo = todo_service.update_todo(db_session, input_data.task_id, user_id, todo_update)
        if not updated_todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }
        return {
            "success": True,
            "message": f"🗓️ Due date set for task '{updated_todo.title}' to {updated_todo.due_date.isoformat()}.",
            "task_id": str(updated_todo.id),
            "due_date": updated_todo.due_date.isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to set due date: {str(e)}"
        }

def list_upcoming_tasks(input_data: ListUpcomingTasksInput, user_id: str, db_session: Session) -> dict:
    """
    List tasks with upcoming due dates for the user.

    Args:
        input_data: Contains filtering options for upcoming tasks
        user_id: ID of the user whose tasks to list
        db_session: Database session

    Returns:
        Dictionary with list of upcoming tasks
    """
    try:
        todo_service = TodoService(db_session)
        upcoming_todos = todo_service.get_upcoming_tasks(
            db_session,
            user_id,
            days_ahead=input_data.days_ahead,
            include_overdue=input_data.include_overdue
        )

        tasks = []
        for todo in upcoming_todos:
            task_info = {
                "id": str(todo.id),
                "title": todo.title,
                "description": todo.description,
                "completed": todo.completed,
                "priority": todo.priority,
                "tags": todo.tags,
                "due_date": todo.due_date.isoformat() if todo.due_date else None,
                "created_at": todo.created_at.isoformat(),
                "recurrence_type": todo.recurrence_type,
                "recurrence_interval": todo.recurrence_interval,
                "next_occurrence": todo.next_occurrence.isoformat() if todo.next_occurrence else None,
                "reminder_at": todo.reminder_at.isoformat() if todo.reminder_at else None,
            }
            tasks.append(task_info)

        return {
            "success": True,
            "message": f"Retrieved {len(tasks)} upcoming tasks",
            "tasks": tasks,
            "total_count": len(tasks)
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to list upcoming tasks: {str(e)}"
        }

def set_task_reminder(input_data: SetReminderInput, user_id: str, db_session: Session) -> dict:
    """
    Set or update the reminder time for a task.

    Args:
        input_data: Contains task ID and new reminder time
        user_id: ID of the user whose task to update
        db_session: Database session

    Returns:
        Dictionary with result of the operation
    """
    try:
        todo_service = TodoService(db_session)
        todo_update = TodoUpdate(reminder_at=datetime.fromisoformat(input_data.reminder_at.replace('Z', '+00:00')))
        updated_todo = todo_service.update_todo(db_session, input_data.task_id, user_id, todo_update)
        if not updated_todo:
            return {
                "success": False,
                "message": "Task not found or does not belong to user"
            }
        return {
            "success": True,
            "message": f"⏰ Reminder set for task '{updated_todo.title}' at {updated_todo.reminder_at.isoformat()}.",
            "task_id": str(updated_todo.id),
            "reminder_at": updated_todo.reminder_at.isoformat()
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to set reminder: {str(e)}"
        }