"""TaskService for managing todo tasks.

This module provides CRUD operations for tasks using in-memory storage.
"""

from datetime import datetime, timedelta
from typing import Optional, List, Dict
from src.models.task import Task, RecurrenceRule
from src.models.enums import Priority, RecurrenceType, ActionType
from src.models.history import HistoryEntry, ActionHistory
from src.utils.validators import validate_due_date


class TaskService:
    """
    Manages task CRUD operations with in-memory storage.
    """

    def __init__(self):
        """Initialize TaskService with empty in-memory storage."""
        self._tasks: dict[int, Task] = {}  # Storage: task_id -> Task
        self._next_id: int = 1              # Auto-increment counter
        self._history: ActionHistory = ActionHistory(max_size=50)  # Undo history

    def add_task(self, title: str, description: str = "", due_date: datetime = None) -> tuple[bool, str, int]:
        """
        Create a new task.

        Args:
            title: Task title (required, non-empty)
            description: Task description (optional)
            due_date: Optional due date for the task

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
            task = Task(
                id=task_id,
                title=title,
                description=description,
                due_date=due_date
            )
            self._tasks[task_id] = task

            # Record in history
            history_entry = HistoryEntry(
                action=ActionType.ADD,
                timestamp=datetime.now(),
                task_id=task_id,
                task_snapshot=task
            )
            self._history.push(history_entry)

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
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        # Update fields
        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

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

        task = self._tasks[task_id]
        # Create a snapshot of the task before deletion for history
        task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        del self._tasks[task_id]

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.DELETE,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=task_snapshot
        )
        self._history.push(history_entry)

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
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        # Flip status: Complete ↔ Incomplete
        was_complete = task.status == "Complete"
        if task.status == "Complete":
            task.status = "Incomplete"
            task.completed_at = None
        else:
            task.status = "Complete"
            task.completed_at = datetime.now()

        # Check if this is a recurring task completion and handle auto-creation
        if not was_complete and task.status == "Complete" and task.is_recurring:
            self._handle_recurring_task_completion(task)

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.COMPLETE,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, f"Task marked as {task.status}!")

    def _handle_recurring_task_completion(self, original_task: Task):
        """
        Handle the completion of a recurring task by creating the next instance.
        """
        # Calculate the next due date based on the recurrence rule
        next_due_date = self._calculate_next_due_date(original_task.due_date, original_task.recurrence_rule)

        # Create a new task with the same properties as the original
        new_task_id = self._next_id
        self._next_id += 1

        new_task = Task(
            id=new_task_id,
            title=original_task.title,
            description=original_task.description,
            due_date=next_due_date,
            recurrence_rule=original_task.recurrence_rule,
            priority=original_task.priority,
            tags=original_task.tags.copy() if original_task.tags else [],
            status="Incomplete",
            created_at=datetime.now(),
            completed_at=None
        )

        self._tasks[new_task_id] = new_task

        # Update the history entry to include the auto-created task
        # We need to modify the last history entry to include the auto-created task
        if self._history.entries:
            last_entry = self._history.entries[-1]
            last_entry.auto_created_task_id = new_task_id
            last_entry.auto_created_task_snapshot = new_task

    def _calculate_next_due_date(self, current_due_date: datetime, rule: RecurrenceRule) -> datetime:
        """
        Calculate the next due date based on recurrence rule.
        """
        if not current_due_date:
            return datetime.now()

        if rule.type == RecurrenceType.DAILY:
            return current_due_date + timedelta(days=1)
        elif rule.type == RecurrenceType.WEEKLY:
            return current_due_date + timedelta(weeks=1)
        elif rule.type == RecurrenceType.CUSTOM:
            return current_due_date + timedelta(days=rule.interval_days)
        else:
            return current_due_date  # For NONE type, return current date

    def update_task_priority(self, task_id: int, priority: 'Priority') -> tuple[bool, str]:
        """
        Update task priority.

        Args:
            task_id: ID of task to update
            priority: New priority value (Priority.HIGH, MEDIUM, or LOW)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.priority = priority

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, "Task priority updated successfully!")

    def update_task_tags(self, task_id: int, tags: list[str]) -> tuple[bool, str]:
        """
        Update task tags (replace existing).

        Args:
            task_id: ID of task to update
            tags: New list of tags (replaces existing tags)

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.tags = tags

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, "Task tags updated successfully!")

    def search_tasks(self, keyword: str) -> list[Task]:
        """
        Case-insensitive search in title and description.

        Args:
            keyword: Search keyword (empty returns all tasks)

        Returns:
            List of matching tasks (all tasks if keyword empty)
        """
        if not keyword or not keyword.strip():
            return self.list_tasks()

        keyword_lower = keyword.lower().strip()
        return [
            task for task in self.list_tasks()
            if keyword_lower in task.title.lower() or
               keyword_lower in task.description.lower()
        ]

    def filter_tasks(self,
                  status_filter: 'FilterStatus' = None,
                  priority_filter: 'Priority' = None,
                  tag_filter: str = None) -> list[Task]:
        """
        Apply status, priority, and/or tag filters (AND logic).

        Args:
            status_filter: FilterStatus enum (None means no status filter)
            priority_filter: Priority enum (None means no priority filter)
            tag_filter: Tag string (None means no tag filter)

        Returns:
            List of filtered tasks
        """
        from src.models.enums import FilterStatus

        tasks = self.list_tasks()

        if status_filter is not None and status_filter != FilterStatus.ALL:
            if status_filter == FilterStatus.COMPLETE:
                tasks = [t for t in tasks if t.status == "Complete"]
            else:  # INCOMPLETE
                tasks = [t for t in tasks if t.status == "Incomplete"]

        if priority_filter is not None:
            tasks = [t for t in tasks if t.priority == priority_filter]

        if tag_filter is not None:
            tasks = [t for t in tasks if tag_filter in t.tags]

        return tasks

    def sort_tasks(self, tasks: list[Task], sort_by: 'SortBy') -> list[Task]:
        """
        Sort task list by title or priority (stable sort).

        Args:
            tasks: List of tasks to sort (does not modify input)
            sort_by: SortBy enum (sort criteria)

        Returns:
            New sorted list
        """
        from src.models.enums import SortBy

        sorted_tasks = tasks.copy()  # Don't modify input

        if sort_by == SortBy.TITLE_ASC:
            sorted_tasks.sort(key=lambda t: t.title.lower(), reverse=False)
        elif sort_by == SortBy.TITLE_DESC:
            sorted_tasks.sort(key=lambda t: t.title.lower(), reverse=True)
        elif sort_by == SortBy.PRIORITY_HIGH_LOW:
            priority_order = {Priority.HIGH: 0, Priority.MEDIUM: 1, Priority.LOW: 2}
            sorted_tasks.sort(key=lambda t: priority_order[t.priority])
        elif sort_by == SortBy.PRIORITY_LOW_HIGH:
            priority_order = {Priority.HIGH: 2, Priority.MEDIUM: 1, Priority.LOW: 0}
            sorted_tasks.sort(key=lambda t: priority_order[t.priority])

        return sorted_tasks

    # Phase I Advanced methods start here
    def set_due_date(self, task_id: int, due_date_str: str) -> tuple[bool, str]:
        """
        Set or update task due date with validation.

        Args:
            task_id: ID of the task to update
            due_date_str: Due date string in YYYY-MM-DD HH:MM format

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        is_valid, message, parsed_date = validate_due_date(due_date_str)
        if not is_valid:
            return (False, message)

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.due_date = parsed_date

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, f"Due date set to {parsed_date.strftime('%Y-%m-%d %H:%M')}")

    def clear_due_date(self, task_id: int) -> tuple[bool, str]:
        """
        Remove task due date.

        Args:
            task_id: ID of the task to update

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.due_date = None

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, "Due date cleared")

    def set_recurrence_rule(self, task_id: int, recurrence_type: RecurrenceType, interval_days: int = None) -> tuple[bool, str]:
        """
        Set or update task recurrence rule.

        Args:
            task_id: ID of the task to update
            recurrence_type: Type of recurrence (NONE, DAILY, WEEKLY, CUSTOM)
            interval_days: Number of days for CUSTOM recurrence

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        from src.utils.validators import validate_recurrence_rule
        is_valid, message = validate_recurrence_rule(recurrence_type, interval_days)
        if not is_valid:
            return (False, message)

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.recurrence_rule = RecurrenceRule(
            type=recurrence_type,
            interval_days=interval_days if recurrence_type == RecurrenceType.CUSTOM else None
        )

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, f"Recurrence rule set to {recurrence_type.value}")

    def clear_recurrence_rule(self, task_id: int) -> tuple[bool, str]:
        """
        Remove task recurrence rule (set to NONE).

        Args:
            task_id: ID of the task to update

        Returns:
            Tuple of (success: bool, message: str)
        """
        if task_id not in self._tasks:
            return (False, f"Task not found (ID: {task_id})")

        task = self._tasks[task_id]
        # Create a snapshot of the task before modification for history
        old_task_snapshot = Task(**{k: v for k, v in task.__dict__.items()})

        task.recurrence_rule = RecurrenceRule(type=RecurrenceType.NONE)

        # Record in history
        history_entry = HistoryEntry(
            action=ActionType.EDIT,
            timestamp=datetime.now(),
            task_id=task_id,
            task_snapshot=old_task_snapshot
        )
        self._history.push(history_entry)

        return (True, "Recurrence rule cleared")

    def get_overdue_tasks(self) -> List[Task]:
        """
        Get all overdue tasks.

        Returns:
            List of overdue tasks
        """
        return [task for task in self.list_tasks() if task.is_overdue]

    def get_due_today_tasks(self) -> List[Task]:
        """
        Get all tasks due today.

        Returns:
            List of tasks due today
        """
        return [task for task in self.list_tasks() if task.is_due_today]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """
        Get tasks due within the next N days.

        Args:
            days: Number of days to look ahead (default 7)

        Returns:
            List of upcoming tasks
        """
        from datetime import timedelta
        future_date = datetime.now() + timedelta(days=days)
        return [task for task in self.list_tasks()
                if task.due_date and
                datetime.now() < task.due_date <= future_date and
                task.status != "Complete"]

    def get_statistics(self) -> Dict:
        """
        Calculate and return task statistics.

        Returns:
            Dictionary with various statistics
        """
        all_tasks = self.list_tasks()
        total_tasks = len(all_tasks)

        if total_tasks == 0:
            return {
                "total_tasks": 0,
                "completed_tasks": 0,
                "incomplete_tasks": 0,
                "completion_rate": 0.0,
                "completion_percentage": 0,
                "overdue_count": 0,
                "due_today_count": 0,
                "upcoming_count": 0,
                "by_priority": {"high": 0, "medium": 0, "low": 0},
                "by_status": {"complete": 0, "incomplete": 0}
            }

        completed_tasks = [t for t in all_tasks if t.status == "Complete"]
        incomplete_tasks = [t for t in all_tasks if t.status == "Incomplete"]

        overdue_tasks = self.get_overdue_tasks()
        due_today_tasks = self.get_due_today_tasks()
        upcoming_tasks = self.get_upcoming_tasks()

        # Count by priority
        by_priority = {
            "high": len([t for t in all_tasks if t.priority == Priority.HIGH]),
            "medium": len([t for t in all_tasks if t.priority == Priority.MEDIUM]),
            "low": len([t for t in all_tasks if t.priority == Priority.LOW])
        }

        # Count by status
        by_status = {
            "complete": len(completed_tasks),
            "incomplete": len(incomplete_tasks)
        }

        completion_rate = len(completed_tasks) / total_tasks if total_tasks > 0 else 0.0

        return {
            "total_tasks": total_tasks,
            "completed_tasks": len(completed_tasks),
            "incomplete_tasks": len(incomplete_tasks),
            "completion_rate": completion_rate,
            "completion_percentage": int(completion_rate * 100),
            "overdue_count": len(overdue_tasks),
            "due_today_count": len(due_today_tasks),
            "upcoming_count": len(upcoming_tasks),
            "by_priority": by_priority,
            "by_status": by_status
        }

    def undo_last_action(self) -> tuple[bool, str]:
        """
        Undo the last action.

        Returns:
            Tuple of (success: bool, message: str)
        """
        last_entry = self._history.pop()
        if not last_entry:
            return (False, "No actions to undo")

        if last_entry.action == ActionType.ADD:
            # Remove the task that was added
            if last_entry.task_id in self._tasks:
                del self._tasks[last_entry.task_id]
                # Adjust the next_id if needed
                if last_entry.task_id == self._next_id - 1:
                    self._next_id = last_entry.task_id
            return (True, f"Undid adding task (ID: {last_entry.task_id})")

        elif last_entry.action == ActionType.DELETE:
            # Restore the deleted task
            self._tasks[last_entry.task_id] = last_entry.task_snapshot
            # Update next_id if needed
            task_id = last_entry.task_id
            if isinstance(task_id, int) and task_id >= self._next_id:
                self._next_id = task_id + 1
            return (True, f"Undid deleting task (ID: {last_entry.task_id})")

        elif last_entry.action in [ActionType.EDIT, ActionType.COMPLETE]:
            # Restore the previous state of the task
            if last_entry.task_id in self._tasks:
                old_task = last_entry.task_snapshot
                self._tasks[last_entry.task_id] = Task(**{k: v for k, v in old_task.__dict__.items()})

            # If this was a recurring task completion with auto-created task, delete the auto-created task
            if (last_entry.action == ActionType.COMPLETE and
                last_entry.auto_created_task_id and
                last_entry.auto_created_task_id in self._tasks):
                del self._tasks[last_entry.auto_created_task_id]

            return (True, f"Undid {last_entry.action.value} action on task (ID: {last_entry.task_id})")

        else:
            # Push the entry back since we don't know how to handle it
            self._history.push(last_entry)
            return (False, f"Cannot undo action: {last_entry.action.value}")
