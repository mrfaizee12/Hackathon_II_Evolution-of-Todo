"""Task model for the todo application.

This module defines the Task dataclass with validation for Phase I requirements.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique numeric identifier (auto-assigned, starts at 1)
        title: Short description of the task (required, non-empty)
        description: Optional detailed description (can be empty)
        status: Completion status ("Complete" or "Incomplete")
    """
    id: int
    title: str
    description: str = ""
    status: str = "Incomplete"

    def __post_init__(self):
        """
        Validate task data after initialization.

        Raises:
            ValueError: If title is empty or status is invalid
        """
        # Validate title (FR-009)
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        # Validate status
        if self.status not in ("Complete", "Incomplete"):
            raise ValueError(f"Invalid status: {self.status}. Must be 'Complete' or 'Incomplete'")

    def __str__(self) -> str:
        """Return user-friendly string representation."""
        return f"ID: {self.id} | Title: {self.title} | Status: {self.status}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging."""
        return (f"Task(id={self.id}, title={self.title!r}, "
                f"description={self.description!r}, status={self.status})")
