"""Reminder models for Phase I Advanced todo application.

This module defines ReminderSummary dataclass for reminder categories.
"""

from dataclasses import dataclass
from typing import List
from .task import Task


@dataclass
class ReminderSummary:
    """Summary of tasks by reminder category"""
    overdue: List[Task]
    due_today: List[Task]
    upcoming: List[Task]

    @property
    def total_count(self) -> int:
        """Total number of tasks needing attention"""
        return len(self.overdue) + len(self.due_today) + len(self.upcoming)

    @property
    def has_overdue(self) -> bool:
        """Check if any overdue tasks exist"""
        return len(self.overdue) > 0

    @property
    def has_due_today(self) -> bool:
        """Check if any tasks due today exist"""
        return len(self.due_today) > 0

    @property
    def has_upcoming(self) -> bool:
        """Check if any upcoming tasks exist"""
        return len(self.upcoming) > 0