"""HistoryService for managing undo functionality in Phase I Advanced todo application.

This module provides undo/redo management for user actions.
"""

from datetime import datetime
from typing import Optional, List
from src.models.history import HistoryEntry, ActionHistory
from src.models.enums import ActionType


class HistoryService:
    """Manages undo/redo functionality for user actions."""

    def __init__(self, action_history: ActionHistory = None):
        """Initialize HistoryService with ActionHistory."""
        self._history = action_history or ActionHistory(max_size=50)

    def record_action(self, entry: HistoryEntry):
        """Record an action in history."""
        self._history.push(entry)

    def undo(self) -> Optional[HistoryEntry]:
        """Undo and return the most recent action."""
        return self._history.pop()

    def peek(self) -> Optional[HistoryEntry]:
        """Peek at the most recent action without removing."""
        return self._history.peek()

    def get_recent(self, limit: int = 10) -> List[HistoryEntry]:
        """Get recent history entries."""
        return self._history.entries[-limit:] if limit < len(self._history.entries) else self._history.entries

    def clear(self):
        """Clear all history."""
        self._history.clear()

    def size(self) -> int:
        """Return the number of entries in history."""
        return self._history.size()

    def can_undo(self) -> bool:
        """Check if there are actions that can be undone."""
        return self._history.size() > 0

    def get_action_count_by_type(self, action_type: ActionType) -> int:
        """Get the count of actions of a specific type."""
        return sum(1 for entry in self._history.entries if entry.action == action_type)