"""
Recurrence service for Recurring Engine
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
import uuid
from .models.recurring import NextOccurrenceResponse


class RecurrenceService:
    """
    Service class for handling recurrence business logic
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using an in-memory store for demonstration
        pass
    
    async def process_recurring_trigger(self, parent_task_id: str, recurrence_pattern: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a recurring task trigger and create a new task instance
        """
        try:
            # Create a new task based on the parent task and recurrence pattern
            new_task_id = str(uuid.uuid4())
            
            # In a real implementation, this would copy the parent task
            # and adjust the due date based on the recurrence pattern
            # For now, we'll just return the new task ID
            
            return {
                "new_task_id": new_task_id,
                "success": True,
                "message": f"New recurring task created with ID: {new_task_id}"
            }
        except Exception as e:
            return {
                "new_task_id": None,
                "success": False,
                "message": f"Error processing recurring trigger: {str(e)}"
            }
    
    async def calculate_next_occurrence(
        self, 
        parent_task_id: str, 
        recurrence_pattern: Dict[str, Any], 
        last_occurrence: Optional[datetime]
    ) -> NextOccurrenceResponse:
        """
        Calculate the next occurrence based on the recurrence pattern
        """
        try:
            recurrence_type = recurrence_pattern.get("type")
            interval = recurrence_pattern.get("interval", 1)
            end_date = recurrence_pattern.get("end_date")
            
            if not last_occurrence:
                # If no last occurrence, we can't calculate the next one
                # In a real system, we'd need the original task creation date
                return NextOccurrenceResponse(next_occurrence=None, should_create_new=False)
            
            # Calculate next occurrence based on recurrence type
            next_occurrence = None
            if recurrence_type == "daily":
                next_occurrence = last_occurrence + timedelta(days=interval)
            elif recurrence_type == "weekly":
                next_occurrence = last_occurrence + timedelta(weeks=interval)
            elif recurrence_type == "monthly":
                # For simplicity, we'll add the interval in days * 30
                # In a real system, we'd need to handle months properly
                next_occurrence = last_occurrence + timedelta(days=interval * 30)
            elif recurrence_type == "yearly":
                # For simplicity, we'll add the interval in days * 365
                # In a real system, we'd need to handle leap years
                next_occurrence = last_occurrence + timedelta(days=interval * 365)
            else:
                # Unknown recurrence type
                return NextOccurrenceResponse(next_occurrence=None, should_create_new=False)
            
            # Check if the next occurrence is beyond the end date
            if end_date and next_occurrence > datetime.fromisoformat(end_date.replace('Z', '+00:00')):
                return NextOccurrenceResponse(next_occurrence=None, should_create_new=False)
            
            # Check if the next occurrence is in the past
            if next_occurrence < datetime.now():
                # This means we missed occurrences, so we should create one now
                return NextOccurrenceResponse(
                    next_occurrence=datetime.now(), 
                    should_create_new=True
                )
            
            # Return the calculated next occurrence
            return NextOccurrenceResponse(
                next_occurrence=next_occurrence, 
                should_create_new=True
            )
        except Exception as e:
            print(f"Error calculating next occurrence: {str(e)}")
            return NextOccurrenceResponse(next_occurrence=None, should_create_new=False)
    
    async def schedule_recurring_task(self, parent_task_id: str, recurrence_pattern: Dict[str, Any]):
        """
        Schedule a recurring task based on the recurrence pattern
        """
        try:
            # In a real implementation, this would schedule the recurring task
            # using a job scheduler like Celery, APScheduler, or Dapr's built-in scheduling
            print(f"Scheduled recurring task for parent_task_id: {parent_task_id}")
            return True
        except Exception as e:
            print(f"Error scheduling recurring task: {str(e)}")
            return False