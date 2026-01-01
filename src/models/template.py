"""TaskTemplate model for Phase I Advanced todo application.

This module defines TaskTemplate dataclass for rapid task creation.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List
from .enums import Priority


@dataclass
class TaskTemplate:
    """Template for rapid task creation"""
    id: str
    name: str  # User-defined template name (e.g., "Weekly Review")
    title: str  # Default task title
    description: Optional[str] = None
    priority: Optional[Priority] = None
    tags: Optional[List[str]] = None
    due_date_offset: Optional[str] = None  # "today", "tomorrow", "next_week", "next_month", None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Validate name is not empty
        if not self.name or not self.name.strip():
            raise ValueError("Template name cannot be empty")

        # Validate title is not empty
        if not self.title or not self.title.strip():
            raise ValueError("Template title cannot be empty")

        # Validate due_date_offset is one of allowed values
        valid_offsets = [None, "today", "tomorrow", "next_week", "next_month"]
        if self.due_date_offset not in valid_offsets:
            raise ValueError(f"Invalid due_date_offset: {self.due_date_offset}")

        # Validate tags if provided
        if self.tags and not all(isinstance(tag, str) for tag in self.tags):
            raise TypeError("All tags must be strings")

    def to_task(self, custom_fields: dict = None, id_generator=None) -> 'Task':
        """Create a Task from this template with optional custom field overrides"""
        from .enums import RecurrenceType
        from .task import RecurrenceRule

        due_date = self._calculate_due_date()

        # Use provided ID generator or default to a placeholder
        task_id = id_generator() if id_generator else "placeholder_id"

        # Import Task here to avoid circular import
        from .task import Task
        task = Task(
            id=task_id,
            title=self.title,
            description=self.description,
            priority=self.priority or Priority.MEDIUM,
            tags=self.tags.copy() if self.tags else [],
            due_date=due_date,
            recurrence_rule=RecurrenceRule(type=RecurrenceType.NONE),
            created_at=datetime.now(),
            completed_at=None
        )

        # Apply custom field overrides
        if custom_fields:
            if "title" in custom_fields:
                task.title = custom_fields["title"]
            if "description" in custom_fields:
                task.description = custom_fields["description"]
            if "priority" in custom_fields:
                task.priority = custom_fields["priority"]
            if "tags" in custom_fields:
                task.tags = custom_fields["tags"]
            if "due_date" in custom_fields:
                task.due_date = custom_fields["due_date"]

        return task

    def _calculate_due_date(self) -> Optional[datetime]:
        """Calculate actual due date from relative offset"""
        if not self.due_date_offset:
            return None

        today = datetime.now()
        today_end = datetime.combine(today.date(), datetime.max.time())

        offset_map = {
            "today": timedelta(0),
            "tomorrow": timedelta(days=1),
            "next_week": timedelta(weeks=1),
            "next_month": timedelta(days=30)
        }

        return today_end + offset_map.get(self.due_date_offset, timedelta(0))


# Note: The generate_id function will be provided by the service layer
# that manages templates, so we don't need it in the model itself.