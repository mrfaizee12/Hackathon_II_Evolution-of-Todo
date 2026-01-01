"""History models for Phase I Advanced todo application.

This module defines HistoryEntry and ActionHistory dataclasses for undo functionality.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from .enums import ActionType


if TYPE_CHECKING:
    from .task import Task


@dataclass
class HistoryEntry:
    """Represents a single user action for undo"""
    action: ActionType
    timestamp: datetime
    task_id: str
    task_snapshot: 'Task'  # Complete task state before action
    auto_created_task_id: Optional[str] = None  # Set for recurring task completions
    auto_created_task_snapshot: Optional['Task'] = None  # For undo restore
    additional_data: Optional[dict] = None  # For bulk operations

    def __post_init__(self):
        # Validate action type
        if not isinstance(self.action, ActionType):
            raise TypeError(f"action must be ActionType, got {type(self.action)}")

        # Validate task snapshot exists
        if not self.task_snapshot:
            raise ValueError("task_snapshot is required")

        # Validate auto_created_task_id matches action type
        if self.action == ActionType.COMPLETE and self.auto_created_task_id:
            if not self.auto_created_task_snapshot:
                raise ValueError("auto_created_task_snapshot required when auto_created_task_id set")


@dataclass
class ActionHistory:
    """Stack-based undo history with FIFO eviction"""
    entries: List[HistoryEntry] = field(default_factory=list)
    max_size: int = 50

    def __post_init__(self):
        if self.max_size < 1:
            raise ValueError("max_size must be positive")

    def push(self, entry: HistoryEntry):
        """Add entry to history, enforce FIFO eviction"""
        self.entries.append(entry)

        # FIFO: Remove oldest if over limit
        if len(self.entries) > self.max_size:
            self.entries.pop(0)

    def pop(self) -> Optional[HistoryEntry]:
        """Remove and return most recent entry"""
        return self.entries.pop() if self.entries else None

    def peek(self) -> Optional[HistoryEntry]:
        """Return most recent entry without removing"""
        return self.entries[-1] if self.entries else None

    def clear(self):
        """Remove all history entries"""
        self.entries.clear()

    def size(self) -> int:
        """Return current number of entries"""
        return len(self.entries)