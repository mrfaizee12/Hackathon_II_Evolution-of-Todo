"""
Task model for Todo Service
"""

from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import uuid


class Task(BaseModel):
    """
    Task model representing a user's todo item
    """
    id: str
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"  # low, medium, high, urgent
    tags: List[str] = []
    status: str = "pending"  # pending, in-progress, completed, cancelled
    created_at: datetime
    updated_at: datetime
    recurrence_pattern: Optional[Dict[str, Any]] = None  # Defines recurrence rules if task repeats
    reminder_settings: Optional[Dict[str, Any]] = None  # Defines when and how to send reminders
    user_id: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class TaskCreateRequest(BaseModel):
    """
    Request model for creating a new task
    """
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"
    tags: List[str] = []
    recurrence_pattern: Optional[Dict[str, Any]] = None
    reminder_settings: Optional[Dict[str, Any]] = None
    user_id: str


class TaskUpdateRequest(BaseModel):
    """
    Request model for updating an existing task
    """
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    status: Optional[str] = None
    recurrence_pattern: Optional[Dict[str, Any]] = None
    reminder_settings: Optional[Dict[str, Any]] = None