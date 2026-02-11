"""
API endpoints for Recurring Engine following OpenAPI contract
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
from datetime import datetime, timedelta

# Handle imports based on PYTHONPATH in container
try:
    from models.recurring import RecurringTaskRequest, NextOccurrenceRequest
    from services.recurrence_service import RecurrenceService
    from shared.event_bus import create_event_bus, get_default_config
except ImportError:
    # Fallback for when running in container with different PYTHONPATH
    from models.recurring import RecurringTaskRequest, NextOccurrenceRequest
    from services.recurrence_service import RecurrenceService
    from shared.event_bus import create_event_bus, get_default_config

router = APIRouter(prefix="/api/v1/recurring", tags=["recurring"])

# Initialize event bus
event_bus_config = get_default_config()
event_bus = create_event_bus(event_bus_config)

# Initialize recurrence service
recurrence_service = RecurrenceService()


@router.post("/trigger", response_model=dict)
async def trigger_recurring_task(request: RecurringTaskRequest, background_tasks: BackgroundTasks):
    """
    Trigger a recurring task
    """
    try:
        # Process the recurring task trigger
        result = await recurrence_service.process_recurring_trigger(
            request.parent_task_id, 
            request.recurrence_pattern
        )
        
        if result["success"]:
            # Publish recurring-task-triggered event
            event_payload = {
                "parent_task_id": request.parent_task_id,
                "new_task_id": result["new_task_id"],
                "recurrence_pattern": request.recurrence_pattern,
                "user_id": result.get("user_id", ""),
                "triggered_at": datetime.now().isoformat()
            }
            
            background_tasks.add_task(
                event_bus.publish, 
                "todo.recurring.triggered", 
                event_payload
            )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error triggering recurring task: {str(e)}")


@router.post("/next-occurrence", response_model=dict)
async def get_next_occurrence(request: NextOccurrenceRequest):
    """
    Get the next occurrence of a recurring task
    """
    try:
        next_occurrence = await recurrence_service.calculate_next_occurrence(
            request.parent_task_id,
            request.recurrence_pattern,
            request.last_occurrence
        )
        
        return next_occurrence
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating next occurrence: {str(e)}")