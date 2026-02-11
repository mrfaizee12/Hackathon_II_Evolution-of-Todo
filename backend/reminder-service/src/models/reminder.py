"""
Models for Reminder Service
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class ScheduleReminderRequest(BaseModel):
    """
    Request model for scheduling a reminder
    """
    task_id: str
    user_id: str
    reminder_time: datetime
    notification_method: str  # email, push, sms


class SendNotificationRequest(BaseModel):
    """
    Request model for sending a notification
    """
    user_id: str
    method: str  # email, push, sms
    title: str
    message: str
    metadata: Optional[Dict[str, Any]] = {}


class ScheduleReminderResponse(BaseModel):
    """
    Response model for scheduling a reminder
    """
    reminder_id: str
    scheduled_time: datetime
    success: bool
    message: Optional[str] = None


class CancelReminderResponse(BaseModel):
    """
    Response model for canceling a reminder
    """
    success: bool
    message: Optional[str] = None


class SendNotificationResponse(BaseModel):
    """
    Response model for sending a notification
    """
    notification_id: str
    sent: bool
    message: Optional[str] = None