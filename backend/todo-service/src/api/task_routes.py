"""
API endpoints for Todo Service following OpenAPI contract
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from datetime import datetime
import uuid
import json

# Handle imports based on PYTHONPATH in container
try:
    from models.todo import Task
    from services.task_service import TaskService
    from shared.event_bus import create_event_bus, get_default_config
except ImportError:
    # Fallback for when running in container with different PYTHONPATH
    from models.todo import Task
    from services.task_service import TaskService
    from shared.event_bus import create_event_bus, get_default_config

router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])

# Initialize event bus
event_bus_config = get_default_config()
event_bus = create_event_bus(event_bus_config)

# Initialize task service
task_service = TaskService()


def validate_task_event_payload(event_type: str, payload: dict) -> bool:
    """
    Validate event payload before publishing
    """
    required_fields = {
        "task-created": ["task_id", "title", "user_id"],
        "task-updated": ["task_id", "updates", "user_id"],
        "task-deleted": ["task_id"]
    }
    
    if event_type not in required_fields:
        return False
    
    required = required_fields[event_type]
    for field in required:
        if field not in payload:
            return False
    
    # Additional validation based on event type
    if event_type == "task-created":
        if not isinstance(payload["task_id"], str) or len(payload["task_id"]) == 0:
            return False
        if not isinstance(payload["title"], str) or len(payload["title"]) == 0:
            return False
        if not isinstance(payload["user_id"], str) or len(payload["user_id"]) == 0:
            return False
    
    elif event_type == "task-updated":
        if not isinstance(payload["task_id"], str) or len(payload["task_id"]) == 0:
            return False
        if not isinstance(payload["user_id"], str) or len(payload["user_id"]) == 0:
            return False
        if not isinstance(payload["updates"], dict):
            return False
    
    elif event_type == "task-deleted":
        if not isinstance(payload["task_id"], str) or len(payload["task_id"]) == 0:
            return False
    
    return True


@router.post("/", response_model=Task)
async def create_task(task_data: dict, background_tasks: BackgroundTasks):
    """
    Create a new task
    """
    try:
        # Create the task
        task = await task_service.create_task(task_data)
        
        # Publish task-created event
        event_payload = {
            "task_id": str(task.id),
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "tags": task.tags,
            "status": task.status,
            "user_id": task.user_id,
            "recurrence_pattern": task.recurrence_pattern,
            "reminder_settings": task.reminder_settings,
            "created_at": task.created_at.isoformat(),
            "updated_at": task.updated_at.isoformat()
        }
        
        # Validate the event payload before publishing
        if validate_task_event_payload("task-created", event_payload):
            background_tasks.add_task(
                event_bus.publish, 
                "todo.task.created", 
                event_payload
            )
        else:
            print(f"Invalid event payload for task-created event: {event_payload}")
        
        return task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")


@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """
    Get a specific task by ID
    """
    try:
        task = await task_service.get_task_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving task: {str(e)}")


@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task_data: dict, background_tasks: BackgroundTasks):
    """
    Update a specific task
    """
    try:
        # Update the task
        updated_task = await task_service.update_task(task_id, task_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Publish task-updated event
        event_payload = {
            "task_id": str(updated_task.id),
            "updates": {
                "title": updated_task.title,
                "description": updated_task.description,
                "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
                "priority": updated_task.priority,
                "tags": updated_task.tags,
                "status": updated_task.status,
                "recurrence_pattern": updated_task.recurrence_pattern,
                "reminder_settings": updated_task.reminder_settings,
            },
            "user_id": updated_task.user_id
        }
        
        # Validate the event payload before publishing
        if validate_task_event_payload("task-updated", event_payload):
            background_tasks.add_task(
                event_bus.publish, 
                "todo.task.updated", 
                event_payload
            )
        else:
            print(f"Invalid event payload for task-updated event: {event_payload}")
        
        return updated_task
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")


@router.delete("/{task_id}")
async def delete_task(task_id: str, background_tasks: BackgroundTasks):
    """
    Delete a specific task
    """
    try:
        deleted = await task_service.delete_task(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Publish task-deleted event
        event_payload = {
            "task_id": task_id,
            "deleted_at": datetime.now().isoformat()
        }
        
        # Validate the event payload before publishing
        if validate_task_event_payload("task-deleted", event_payload):
            background_tasks.add_task(
                event_bus.publish, 
                "todo.task.deleted", 
                event_payload
            )
        else:
            print(f"Invalid event payload for task-deleted event: {event_payload}")
        
        return {"success": True}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting task: {str(e)}")


@router.get("/", response_model=dict)
async def list_tasks(
    user_id: Optional[str] = None,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    tag: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    """
    List tasks with optional filters
    """
    try:
        filters = {}
        if user_id:
            filters["user_id"] = user_id
        if status:
            filters["status"] = status
        if priority:
            filters["priority"] = priority
        if tag:
            filters["tag"] = tag
            
        tasks = await task_service.list_tasks(filters, limit, offset)
        total_count = await task_service.count_tasks(filters)
        
        return {
            "tasks": tasks,
            "total_count": total_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tasks: {str(e)}")