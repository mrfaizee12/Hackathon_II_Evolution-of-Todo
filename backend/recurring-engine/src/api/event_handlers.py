"""
Event handlers for Recurring Engine
"""

from typing import Dict, Any
import asyncio
from datetime import datetime
from .models.recurring import NextOccurrenceResponse
from .services.recurrence_service import RecurrenceService


class RecurringEngineEventHandler:
    """
    Event handler class for processing events in the Recurring Engine
    """
    
    def __init__(self):
        self.recurrence_service = RecurrenceService()
    
    async def handle_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle task created events - check if the task has a recurrence pattern
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            recurrence_pattern = payload.get('recurrence_pattern')
            user_id = payload.get('user_id')
            
            print(f"Recurring Engine received task created event for task {task_id}")
            
            # Check if the created task has a recurrence pattern
            if recurrence_pattern:
                print(f"Scheduling recurring task for task {task_id} with pattern: {recurrence_pattern}")
                
                # Schedule the recurring task
                scheduled = await self.recurrence_service.schedule_recurring_task(task_id, recurrence_pattern)
                
                if scheduled:
                    return {
                        "handled": True, 
                        "event_type": "task_created", 
                        "task_id": task_id,
                        "scheduled_recurrence": True
                    }
            
            return {
                "handled": True, 
                "event_type": "task_created", 
                "task_id": task_id,
                "scheduled_recurrence": bool(recurrence_pattern)
            }
        except Exception as e:
            print(f"Error handling task created event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_recurring_triggered_event(self, event_data: Dict[str, Any]):
        """
        Handle recurring triggered events - this might be for chained recurrences
        """
        try:
            payload = event_data.get('payload', {})
            parent_task_id = payload.get('parent_task_id')
            new_task_id = payload.get('new_task_id')
            recurrence_pattern = payload.get('recurrence_pattern')
            user_id = payload.get('user_id')
            
            print(f"Recurring Engine received recurring triggered event - parent: {parent_task_id}, new: {new_task_id}")
            
            # If this is a chained recurrence, we might need to schedule the next occurrence
            if recurrence_pattern and parent_task_id:
                # Calculate the next occurrence based on the pattern
                next_occurrence_result = await self.recurrence_service.calculate_next_occurrence(
                    parent_task_id,
                    recurrence_pattern,
                    datetime.now()
                )
                
                if next_occurrence_result.should_create_new and next_occurrence_result.next_occurrence:
                    # Process the next recurring trigger
                    result = await self.recurrence_service.process_recurring_trigger(
                        parent_task_id,
                        recurrence_pattern
                    )
                    
                    return {
                        "handled": True,
                        "event_type": "recurring_triggered",
                        "parent_task_id": parent_task_id,
                        "new_task_id": result.get("new_task_id"),
                        "next_scheduled": True
                    }
            
            return {
                "handled": True,
                "event_type": "recurring_triggered",
                "parent_task_id": parent_task_id,
                "new_task_id": new_task_id
            }
        except Exception as e:
            print(f"Error handling recurring triggered event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle task updated events - check if recurrence pattern changed
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            updates = payload.get('updates', {})
            user_id = payload.get('user_id')
            
            print(f"Recurring Engine received task updated event for task {task_id}")
            
            # Check if the recurrence pattern was updated
            if 'recurrence_pattern' in updates:
                new_pattern = updates['recurrence_pattern']
                
                # Cancel any existing scheduled recurrences for this task
                # Then schedule new ones based on the updated pattern
                print(f"Recurrence pattern updated for task {task_id}, rescheduling...")
                
                scheduled = await self.recurrence_service.schedule_recurring_task(task_id, new_pattern)
                
                return {
                    "handled": True,
                    "event_type": "task_updated",
                    "task_id": task_id,
                    "rescheduled": scheduled
                }
            
            return {
                "handled": True,
                "event_type": "task_updated",
                "task_id": task_id,
                "rescheduled": False
            }
        except Exception as e:
            print(f"Error handling task updated event: {str(e)}")
            return {"handled": False, "error": str(e)}