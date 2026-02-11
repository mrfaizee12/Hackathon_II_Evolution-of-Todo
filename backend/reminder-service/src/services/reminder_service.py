"""
Reminder service for Reminder Service
"""

from typing import Dict, Any, Optional
from datetime import datetime
import uuid
import asyncio
from .models.reminder import ScheduleReminderResponse, CancelReminderResponse, SendNotificationResponse


class ReminderService:
    """
    Service class for handling reminder business logic
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using an in-memory store for demonstration
        self.scheduled_reminders = {}
        self.notifications_sent = []
    
    async def schedule_reminder(
        self, 
        task_id: str, 
        user_id: str, 
        reminder_time: datetime, 
        notification_method: str
    ) -> Dict[str, Any]:
        """
        Schedule a reminder for a task
        """
        try:
            reminder_id = str(uuid.uuid4())
            
            reminder_data = {
                "id": reminder_id,
                "task_id": task_id,
                "user_id": user_id,
                "reminder_time": reminder_time,
                "notification_method": notification_method,
                "created_at": datetime.now(),
                "status": "scheduled"
            }
            
            # Store the reminder
            self.scheduled_reminders[reminder_id] = reminder_data
            
            # In a real implementation, we would schedule the actual reminder
            # using a job scheduler or Dapr's timer functionality
            # For now, we'll just return the scheduled reminder
            
            return {
                "reminder_id": reminder_id,
                "scheduled_time": reminder_time,
                "success": True,
                "message": f"Reminder scheduled with ID: {reminder_id}"
            }
        except Exception as e:
            return {
                "reminder_id": None,
                "scheduled_time": None,
                "success": False,
                "message": f"Error scheduling reminder: {str(e)}"
            }
    
    async def cancel_reminder(self, reminder_id: str) -> Dict[str, Any]:
        """
        Cancel a scheduled reminder
        """
        try:
            if reminder_id in self.scheduled_reminders:
                # Update the status to cancelled
                self.scheduled_reminders[reminder_id]["status"] = "cancelled"
                
                return {
                    "success": True,
                    "message": f"Reminder {reminder_id} has been cancelled"
                }
            else:
                return {
                    "success": False,
                    "message": f"Reminder {reminder_id} not found"
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Error cancelling reminder: {str(e)}"
            }
    
    async def send_notification(
        self, 
        user_id: str, 
        method: str, 
        title: str, 
        message: str, 
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Send a notification to a user
        """
        try:
            notification_id = str(uuid.uuid4())
            
            # In a real implementation, this would actually send the notification
            # via email, push notification, SMS, etc.
            # For now, we'll just simulate the sending
            
            notification_data = {
                "id": notification_id,
                "user_id": user_id,
                "method": method,
                "title": title,
                "message": message,
                "metadata": metadata or {},
                "sent_at": datetime.now(),
                "status": "sent"
            }
            
            # Store the notification
            self.notifications_sent.append(notification_data)
            
            # Simulate sending the notification
            print(f"Sending {method} notification to user {user_id}: {title}")
            print(f"Message: {message}")
            
            return {
                "notification_id": notification_id,
                "sent": True,
                "message": f"Notification sent successfully with ID: {notification_id}"
            }
        except Exception as e:
            return {
                "notification_id": None,
                "sent": False,
                "message": f"Error sending notification: {str(e)}"
            }
    
    async def process_due_reminders(self):
        """
        Process reminders that are due to be sent
        """
        try:
            now = datetime.now()
            due_reminders = []
            
            # Find all reminders that are due
            for reminder_id, reminder_data in self.scheduled_reminders.items():
                if (
                    reminder_data["status"] == "scheduled" and
                    reminder_data["reminder_time"] <= now
                ):
                    due_reminders.append(reminder_data)
            
            # Process each due reminder
            for reminder in due_reminders:
                # Send the notification
                await self.send_notification(
                    user_id=reminder["user_id"],
                    method=reminder["notification_method"],
                    title="Task Reminder",
                    message=f"Reminder: Your task '{reminder['task_id']}' is due.",
                    metadata={"task_id": reminder["task_id"]}
                )
                
                # Update the reminder status
                self.scheduled_reminders[reminder["id"]]["status"] = "sent"
            
            return {
                "processed_count": len(due_reminders),
                "message": f"Processed {len(due_reminders)} due reminders"
            }
        except Exception as e:
            return {
                "processed_count": 0,
                "message": f"Error processing due reminders: {str(e)}"
            }