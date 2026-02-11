from pydantic import BaseModel
from datetime import datetime
import uuid

class TaskCreatedEvent(BaseModel):
    task_id: uuid.UUID
    user_id: uuid.UUID
    title: str
    created_at: datetime

class TaskCompletedEvent(BaseModel):
    task_id: uuid.UUID
    user_id: uuid.UUID
    completed_at: datetime
    recurrence_type: str # Add recurrence type to event for recurrence engine

class ReminderTriggeredEvent(BaseModel):
    task_id: uuid.UUID
    user_id: uuid.UUID
    reminder_time: datetime
    message: str # Message to be sent as reminder
