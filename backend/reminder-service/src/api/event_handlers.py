"""
Event handlers for Reminder Service
"""

from typing import Dict, Any
import asyncio
from datetime import datetime
from .services.reminder_service import ReminderService


class ReminderServiceEventHandler:
    """
    Event handler class for processing events in the Reminder Service
    """
    
    def __init__(self):
        self.reminder_service = ReminderService()
    
    async def handle_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle task created events - schedule reminders if needed
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            reminder_settings = payload.get('reminder_settings')
            user_id = payload.get('user_id')
            
            print(f"Reminder Service received task created event for task {task_id}")
            
            # Check if the created task has reminder settings
            if reminder_settings and reminder_settings.get('enabled', False):
                reminder_time = reminder_settings.get('minutes_before')
                if reminder_time:
                    # Calculate the actual reminder time based on due date and minutes before
                    due_date_str = payload.get('due_date')
                    if due_date_str:
                        from datetime import datetime, timedelta
                        due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                        reminder_time_obj = due_date - timedelta(minutes=reminder_settings['minutes_before'])
                        
                        notification_method = reminder_settings.get('method', 'email')
                        
                        result = await self.reminder_service.schedule_reminder(
                            task_id,
                            user_id,
                            reminder_time_obj,
                            notification_method
                        )
                        
                        return {
                            "handled": True,
                            "event_type": "task_created",
                            "task_id": task_id,
                            "reminder_scheduled": result["success"]
                        }
            
            return {
                "handled": True,
                "event_type": "task_created",
                "task_id": task_id,
                "reminder_scheduled": bool(reminder_settings and reminder_settings.get('enabled', False))
            }
        except Exception as e:
            print(f"Error handling task created event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle task updated events - reschedule reminders if needed
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            updates = payload.get('updates', {})
            user_id = payload.get('user_id')
            
            print(f"Reminder Service received task updated event for task {task_id}")
            
            # Check if reminder settings were updated
            if 'reminder_settings' in updates:
                new_reminder_settings = updates['reminder_settings']
                
                # Cancel existing reminders for this task
                # In a real implementation, we'd have a way to identify and cancel specific reminders
                # For now, we'll just log that we need to reschedule
                
                if new_reminder_settings and new_reminder_settings.get('enabled', False):
                    reminder_time = new_reminder_settings.get('minutes_before')
                    if reminder_time:
                        # Calculate the actual reminder time based on due date and minutes before
                        due_date_str = updates.get('due_date') or payload.get('due_date')
                        if due_date_str:
                            from datetime import datetime, timedelta
                            due_date = datetime.fromisoformat(due_date_str.replace('Z', '+00:00'))
                            reminder_time_obj = due_date - timedelta(minutes=new_reminder_settings['minutes_before'])
                            
                            notification_method = new_reminder_settings.get('method', 'email')
                            
                            result = await self.reminder_service.schedule_reminder(
                                task_id,
                                user_id,
                                reminder_time_obj,
                                notification_method
                            )
                            
                            return {
                                "handled": True,
                                "event_type": "task_updated",
                                "task_id": task_id,
                                "reminder_rescheduled": result["success"]
                            }
            
            return {
                "handled": True,
                "event_type": "task_updated",
                "task_id": task_id,
                "reminder_rescheduled": False
            }
        except Exception as e:
            print(f"Error handling task updated event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_recurring_triggered_event(self, event_data: Dict[str, Any]):
        """
        Handle recurring triggered events - create reminders for new recurring tasks
        """
        try:
            payload = event_data.get('payload', {})
            parent_task_id = payload.get('parent_task_id')
            new_task_id = payload.get('new_task_id')
            user_id = payload.get('user_id')
            
            print(f"Reminder Service received recurring triggered event - parent: {parent_task_id}, new: {new_task_id}")
            
            # In a real implementation, we would need to get the original task's reminder settings
            # and apply them to the newly created recurring task
            # For now, we'll just log the event
            
            return {
                "handled": True,
                "event_type": "recurring_triggered",
                "parent_task_id": parent_task_id,
                "new_task_id": new_task_id
            }
        except Exception as e:
            print(f"Error handling recurring triggered event: {str(e)}")
            return {"handled": False, "error": str(e)}