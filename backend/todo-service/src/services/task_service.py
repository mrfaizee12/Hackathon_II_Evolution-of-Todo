"""
Task service for Todo Service
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
# Import from the correct location based on PYTHONPATH
try:
    from models.todo import Task, TaskCreateRequest, TaskUpdateRequest
except ImportError:
    # Fallback for when running in container with different PYTHONPATH
    from models.todo import Task, TaskCreateRequest, TaskUpdateRequest


class TaskService:
    """
    Service class for handling task business logic
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using an in-memory store for demonstration
        self.tasks = {}
    
    async def create_task(self, task_data: Dict[str, Any]) -> Task:
        """
        Create a new task
        """
        task_id = str(uuid.uuid4())
        now = datetime.now()
        
        # Validate task data based on requirements
        title = task_data.get("title")
        if not title or len(title) < 1 or len(title) > 200:
            raise ValueError("Title is required and must be between 1-200 characters")
        
        due_date = task_data.get("due_date")
        if due_date and datetime.fromisoformat(due_date.replace('Z', '+00:00')) < now:
            raise ValueError("Due date must be in the future if provided")
        
        # Create the task object
        task = Task(
            id=task_id,
            title=task_data.get("title"),
            description=task_data.get("description"),
            due_date=datetime.fromisoformat(due_date.replace('Z', '+00:00')) if due_date else None,
            priority=task_data.get("priority", "medium"),
            tags=task_data.get("tags", []),
            status=task_data.get("status", "pending"),
            created_at=now,
            updated_at=now,
            recurrence_pattern=task_data.get("recurrence_pattern"),
            reminder_settings=task_data.get("reminder_settings"),
            user_id=task_data.get("user_id")
        )
        
        # Save to "database"
        self.tasks[task_id] = task
        
        return task
    
    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """
        Get a task by its ID
        """
        return self.tasks.get(task_id)
    
    async def update_task(self, task_id: str, task_data: Dict[str, Any]) -> Optional[Task]:
        """
        Update an existing task
        """
        task = self.tasks.get(task_id)
        if not task:
            return None
        
        # Update fields that are provided
        if "title" in task_data and task_data["title"] is not None:
            if len(task_data["title"]) < 1 or len(task_data["title"]) > 200:
                raise ValueError("Title must be between 1-200 characters")
            task.title = task_data["title"]
        
        if "description" in task_data and task_data["description"] is not None:
            task.description = task_data["description"]
        
        if "due_date" in task_data and task_data["due_date"] is not None:
            due_date = datetime.fromisoformat(task_data["due_date"].replace('Z', '+00:00'))
            if due_date < datetime.now():
                raise ValueError("Due date must be in the future")
            task.due_date = due_date
        
        if "priority" in task_data and task_data["priority"] is not None:
            task.priority = task_data["priority"]
        
        if "tags" in task_data and task_data["tags"] is not None:
            task.tags = task_data["tags"]
        
        if "status" in task_data and task_data["status"] is not None:
            # Validate status transition
            valid_statuses = ["pending", "in-progress", "completed", "cancelled"]
            if task_data["status"] not in valid_statuses:
                raise ValueError(f"Invalid status. Must be one of {valid_statuses}")
            task.status = task_data["status"]
        
        if "recurrence_pattern" in task_data and task_data["recurrence_pattern"] is not None:
            task.recurrence_pattern = task_data["recurrence_pattern"]
        
        if "reminder_settings" in task_data and task_data["reminder_settings"] is not None:
            task.reminder_settings = task_data["reminder_settings"]
        
        # Update the timestamp
        task.updated_at = datetime.now()
        
        # Save updated task
        self.tasks[task_id] = task
        
        return task
    
    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False
    
    async def list_tasks(self, filters: Dict[str, Any], limit: int, offset: int) -> List[Task]:
        """
        List tasks with optional filters
        """
        filtered_tasks = list(self.tasks.values())
        
        # Apply filters
        if "user_id" in filters:
            filtered_tasks = [task for task in filtered_tasks if task.user_id == filters["user_id"]]
        
        if "status" in filters:
            filtered_tasks = [task for task in filtered_tasks if task.status == filters["status"]]
        
        if "priority" in filters:
            filtered_tasks = [task for task in filtered_tasks if task.priority == filters["priority"]]
        
        # For tag filtering, check if any of the task's tags match the filter
        if "tag" in filters:
            filtered_tasks = [task for task in filtered_tasks if filters["tag"] in task.tags]
        
        # Apply pagination
        start_idx = offset
        end_idx = start_idx + limit
        return filtered_tasks[start_idx:end_idx]
    
    async def count_tasks(self, filters: Dict[str, Any]) -> int:
        """
        Count tasks matching the filters
        """
        return len(await self.list_tasks(filters, float('inf'), 0))