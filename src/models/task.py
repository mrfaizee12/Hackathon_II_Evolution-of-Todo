"""Task model for todo application.

This module defines Task dataclass with validation for Phase I Advanced requirements.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from .enums import Priority, RecurrenceType


@dataclass
class RecurrenceRule:
    """Defines how a task recurs"""
    type: RecurrenceType = RecurrenceType.NONE
    interval_days: Optional[int] = None  # Only for CUSTOM type

    def __post_init__(self):
        if self.type == RecurrenceType.CUSTOM and self.interval_days is None:
            raise ValueError("CUSTOM recurrence requires interval_days")
        if self.interval_days is not None and self.interval_days < 1:
            raise ValueError("interval_days must be positive")


@dataclass
class Task:
    """
    Represents a single todo item with extended Phase I Advanced features.

    Attributes:
        id: Unique numeric identifier (auto-assigned, starts at 1)
        title: Short description of the task (required, non-empty)
        description: Optional detailed description (can be empty)
        due_date: Optional deadline for task completion (datetime, must be current or future)
        recurrence_rule: Optional recurrence pattern for the task
        status: Completion status ("Complete" or "Incomplete")
        priority: Task importance level (High, Medium, or Low; defaults to Medium)
        tags: Collection of text labels used for categorization and filtering (zero or more tags)
        created_at: When the task was created (defaults to now)
        completed_at: When the task was completed (optional, set when status = Complete)
    """
    id: int
    title: str
    description: str = ""
    due_date: Optional[datetime] = None
    recurrence_rule: RecurrenceRule = field(default_factory=RecurrenceRule)
    status: str = "Incomplete"
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def __post_init__(self):
        """
        Validate task data after initialization.

        Raises:
            ValueError: If title is empty, status is invalid, or due date is in the past
        """
        # Validate title (FR-009)
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate status
        if self.status not in ("Complete", "Incomplete"):
            raise ValueError(f"Invalid status: {self.status}. Must be 'Complete' or 'Incomplete'")

        # Validate due date is not in past
        if self.due_date and self.due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")

        # Validate tags are strings
        if self.tags:
            if not all(isinstance(tag, str) for tag in self.tags):
                raise TypeError("All tags must be strings")

        # Validate status consistency
        if self.status == "Complete" and not self.completed_at:
            self.completed_at = datetime.now()
        elif self.status == "Incomplete" and self.completed_at:
            self.completed_at = None

    @property
    def is_overdue(self) -> bool:
        """Check if task is overdue (due date passed and not completed)"""
        return (
            self.due_date is not None
            and self.due_date < datetime.now()
            and self.status != "Complete"
        )

    @property
    def is_due_today(self) -> bool:
        """Check if task is due today"""
        return (
            self.due_date is not None
            and self.due_date.date() == datetime.now().date()
            and self.status != "Complete"
        )

    @property
    def is_upcoming(self) -> bool:
        """Check if task is upcoming (within next 7 days)"""
        if not self.due_date or self.status == "Complete":
            return False
        days_until_due = (self.due_date - datetime.now()).days
        return 0 < days_until_due <= 7

    @property
    def is_recurring(self) -> bool:
        """Check if task has recurrence rule"""
        return self.recurrence_rule.type != RecurrenceType.NONE

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        priority_str = f"[{self.priority.value}]" if self.priority else ""
        status_str = f" | Status: {self.status}"
        due_date_str = f" | Due: {self.due_date.strftime('%Y-%m-%d %H:%M')}" if self.due_date else ""
        recurrence_str = f" | Recurring: {self.recurrence_rule.type.value}" if self.recurrence_rule.type != RecurrenceType.NONE else ""
        return f"ID: {self.id} | Title: {self.title} {priority_str}{due_date_str}{recurrence_str}{status_str}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        tags_repr = f", tags={self.tags}" if self.tags else ""
        due_date_repr = f", due_date={self.due_date!r}" if self.due_date else ""
        recurrence_repr = f", recurrence_rule={self.recurrence_rule!r}" if self.recurrence_rule else ""
        return f"Task(id={self.id}, title={self.title!r}, " \
                f"description={self.description!r}, status={self.status}, " \
                f"priority={self.priority}{due_date_repr}{recurrence_repr}{tags_repr})"
