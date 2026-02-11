"""
API endpoints for Reminder Service following OpenAPI contract
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
from datetime import datetime

# Handle imports based on PYTHONPATH in container
try:
    from models.reminder import ScheduleReminderRequest, SendNotificationRequest
    from services.reminder_service import ReminderService
    from shared.event_bus import create_event_bus, get_default_config
except ImportError:
    # Fallback for when running in container with different PYTHONPATH
    from models.reminder import ScheduleReminderRequest, SendNotificationRequest
    from services.reminder_service import ReminderService
    from shared.event_bus import create_event_bus, get_default_config

router = APIRouter(prefix="/api/v1", tags=["reminders", "notifications"])

# Initialize event bus
event_bus_config = get_default_config()
event_bus = create_event_bus(event_bus_config)

# Initialize reminder service
reminder_service = ReminderService()


@router.post("/reminders/schedule", response_model=dict)
async def schedule_reminder(request: ScheduleReminderRequest, background_tasks: BackgroundTasks):
    """
    Schedule a reminder
    """
    try:
        result = await reminder_service.schedule_reminder(
            request.task_id,
            request.user_id,
            request.reminder_time,
            request.notification_method
        )
        
        if result["success"]:
            # Publish reminder scheduled event
            event_payload = {
                "reminder_id": result["reminder_id"],
                "task_id": request.task_id,
                "user_id": request.user_id,
                "reminder_time": request.reminder_time.isoformat(),
                "notification_method": request.notification_method,
                "scheduled_at": datetime.now().isoformat()
            }
            
            background_tasks.add_task(
                event_bus.publish, 
                "todo.reminder.scheduled", 
                event_payload
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error scheduling reminder: {str(e)}")


@router.delete("/reminders/{reminder_id}", response_model=dict)
async def cancel_reminder(reminder_id: str):
    """
    Cancel a scheduled reminder
    """
    try:
        result = await reminder_service.cancel_reminder(reminder_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error canceling reminder: {str(e)}")


@router.post("/notifications/send", response_model=dict)
async def send_notification(request: SendNotificationRequest, background_tasks: BackgroundTasks):
    """
    Send a notification
    """
    try:
        result = await reminder_service.send_notification(
            request.user_id,
            request.method,
            request.title,
            request.message,
            request.metadata
        )
        
        if result["sent"]:
            # Publish notification sent event
            event_payload = {
                "notification_id": result["notification_id"],
                "user_id": request.user_id,
                "method": request.method,
                "title": request.title,
                "message": request.message,
                "sent_at": datetime.now().isoformat()
            }
            
            background_tasks.add_task(
                event_bus.publish, 
                "todo.notification.sent", 
                event_payload
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending notification: {str(e)}")