"""TaskService for managing todo tasks.

This module provides CRUD operations for tasks using in-memory storage.
"""

from typing import Optional
from src.models.task import Task


class TaskService:
    """
    Manages task CRUD operations with in-memory storage.
    """

    def __init__(self):
        """Initialize TaskService with empty in-memory storage."""
        self._tasks: dict[int, Task] = {}  # Storage: task_id -> Task
        self._next_id: int = 1              # Auto-increment counter

    def add_task(self, title: str, description: str = "") -> tuple[bool, str, int]:
        """
        Create a new task.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)

        Returns:
            Tuple of (success: bool, message: str, task_id: int)
            task_id is -1 if operation failed
        """
        # Validate title before creating Task
        if not title or not title.strip():
            return (False, "Task title cannot be empty", -1)

        task_id = self._next_id
        self._next_id += 1  # Increment for next task, never decrement

        try:
            task = Task(id=task_id, title=title, description=description)
            self._tasks[task_id] = task
            return (True, f"Task added successfully! (ID: {task_id})", task_id)
        except ValueError as e:
            # Should not happen if we validated title above, but catch anyway
            return (False, str(e), -1)

    def get_task(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by ID.

        Args:
            task_id: ID of the task to retrieve

        Returns:
            Task if found, None otherwise
        """
        return self._tasks.get(task_id)

    def list_tasks(self) -> list[Task]:
        """
        Get all tasks in insertion order.

        Returns:
            List of all tasks (empty list if no tasks)
        """
        return list(self._tasks.values())

    def update_task(self, task_id: int, title: Optional[str] = None,
                    description: Optional[str] = None) -> tuple[bool, str]:
        """
        Update task title and/or description.

        Args:
            task_id: ID of the task to update
            title: New title (optional, None to keep current)
            description: New description (optional, None to keep current)

        Returns:
            Tuple of (success: bool, message: str)
        """
        # Check if task exists
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        # Check if any changes provided
        if title is None and description is None:
            return (True, "No changes made")

        # Validate new title if provided
        if title is not None and (not title or not title.strip()):
            return (False, "Task title cannot be empty")

        task = self._tasks[task_id]

        # Update fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        return (True, "Task updated successfully!")

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Remove a task from storage.

        Args:
            task_id: ID of the task to delete

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        del self._tasks[task_id]
        return (True, f"Task deleted successfully! (ID: {task_id})")

    def toggle_status(self, task_id: int) -> tuple[bool, str]:
        """
        Toggle task between Complete and Incomplete.

        Args:
            task_id: ID of the task to toggle

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        task = self._tasks[task_id]

        # Flip status: Complete ↔ Incomplete
        if task.status == "Complete":
            task.status = "Incomplete"
        else:
            task.status = "Complete"

        return (True, f"Task marked as {task.status}!")
