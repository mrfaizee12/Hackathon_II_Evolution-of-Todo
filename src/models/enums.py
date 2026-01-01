"""Enums for Phase I Advanced todo application.

This module defines enumerations for priority, sorting, filtering, and advanced features.
"""

from enum import Enum


class Priority(Enum):
    """Task importance levels for Phase I Advanced."""

    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"

    def __str__(self) -> str:
        """Return string representation for display."""
        return self.value


class SortBy(Enum):
    """Sort criteria for task list display."""

    TITLE_ASC = "Title (A-Z)"
    TITLE_DESC = "Title (Z-A)"
    PRIORITY_HIGH_LOW = "Priority (High to Low)"
    PRIORITY_LOW_HIGH = "Priority (Low to High)"


class FilterStatus(Enum):
    """Completion status filter options."""

    ALL = "All"
    COMPLETE = "Complete"
    INCOMPLETE = "Incomplete"


class RecurrenceType(Enum):
    """Types of recurrence for tasks."""

    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    CUSTOM = "custom"


class ActionType(Enum):
    """Types of actions that can be recorded in history."""

    ADD = "add"
    EDIT = "edit"
    DELETE = "delete"
    COMPLETE = "complete"
    BULK_COMPLETE = "bulk_complete"
    BULK_DELETE = "bulk_delete"
