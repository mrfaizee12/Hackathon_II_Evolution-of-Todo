"""TaskStatistics model for Phase I Advanced todo application.

This module defines TaskStatistics dataclass for task tracking and productivity insights.
"""

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class TaskStatistics:
    """Statistics for task tracking and productivity insights"""
    total_tasks: int
    completed_tasks: int
    incomplete_tasks: int
    completion_rate: float  # 0.0 to 1.0
    overdue_count: int
    due_today_count: int
    upcoming_count: int
    by_priority: Dict[str, int]  # {"high": count, "medium": count, "low": count}
    by_status: Dict[str, int]  # {"complete": count, "incomplete": count}
    average_completion_time_days: Optional[float] = None

    def __post_init__(self):
        # Validate completion_rate is between 0 and 1
        if not 0.0 <= self.completion_rate <= 1.0:
            raise ValueError("completion_rate must be between 0.0 and 1.0")

        # Validate counts are non-negative
        for count in [self.total_tasks, self.completed_tasks, self.incomplete_tasks,
                     self.overdue_count, self.due_today_count, self.upcoming_count]:
            if count < 0:
                raise ValueError("All counts must be non-negative")

        # Validate sum matches total
        if self.completed_tasks + self.incomplete_tasks != self.total_tasks:
            raise ValueError("completed_tasks + incomplete_tasks must equal total_tasks")

    @property
    def completion_percentage(self) -> int:
        """Completion rate as percentage (0-100)"""
        return int(self.completion_rate * 100)