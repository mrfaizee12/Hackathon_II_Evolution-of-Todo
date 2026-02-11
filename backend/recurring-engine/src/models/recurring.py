"""
Models for Recurring Engine
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class RecurringTaskRequest(BaseModel):
    """
    Request model for triggering a recurring task
    """
    parent_task_id: str
    recurrence_pattern: Dict[str, Any]  # Contains type, interval, end_date, etc.


class NextOccurrenceRequest(BaseModel):
    """
    Request model for getting the next occurrence of a recurring task
    """
    parent_task_id: str
    recurrence_pattern: Dict[str, Any]  # Contains type, interval, end_date, etc.
    last_occurrence: Optional[datetime] = None


class RecurringTaskResponse(BaseModel):
    """
    Response model for recurring task operations
    """
    new_task_id: str
    success: bool
    message: Optional[str] = None


class NextOccurrenceResponse(BaseModel):
    """
    Response model for next occurrence calculation
    """
    next_occurrence: Optional[datetime] = None
    should_create_new: bool