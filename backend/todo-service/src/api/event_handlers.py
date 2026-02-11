"""
Event handlers for Todo Service
"""

from typing import Dict, Any
import asyncio
from datetime import datetime
from .models.todo import Task
from .services.task_service import TaskService


class TodoEventHandler:
    """
    Event handler class for processing events in the Todo Service
    """
    
    def __init__(self):
        self.task_service = TaskService()
    
    async def handle_reminder_triggered_event(self, event_data: Dict[str, Any]):
        """
        Handle reminder triggered events
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            user_id = payload.get('user_id')
            
            print(f"Todo Service received reminder triggered event for task {task_id}")
            
            # Update task status if needed
            if task_id:
                task = await self.task_service.get_task_by_id(task_id)
                if task:
                    # Maybe update a 'last_reminded' field or similar
                    updated_data = {
                        "updated_at": datetime.now().isoformat()
                    }
                    await self.task_service.update_task(task_id, updated_data)
            
            return {"handled": True, "event_type": "reminder_triggered", "task_id": task_id}
        except Exception as e:
            print(f"Error handling reminder triggered event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_chatbot_event(self, event_data: Dict[str, Any]):
        """
        Handle chatbot events
        """
        try:
            payload = event_data.get('payload', {})
            user_id = payload.get('user_id')
            intent = payload.get('intent')
            entities = payload.get('entities', {})
            
            print(f"Todo Service received chatbot event for user {user_id}, intent: {intent}")
            
            # Process any task-related actions from the chatbot
            if intent == "create_task" and entities:
                # Create a task based on entities from the chatbot
                task_data = {
                    "title": entities.get("title", "Untitled task"),
                    "description": entities.get("description", ""),
                    "user_id": user_id,
                    "priority": entities.get("priority", "medium"),
                    "due_date": entities.get("due_date")
                }
                
                task = await self.task_service.create_task(task_data)
                return {"handled": True, "event_type": "chatbot_event", "created_task": task.id}
            
            return {"handled": True, "event_type": "chatbot_event", "user_id": user_id}
        except Exception as e:
            print(f"Error handling chatbot event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_recurring_triggered_event(self, event_data: Dict[str, Any]):
        """
        Handle recurring task triggered events
        """
        try:
            payload = event_data.get('payload', {})
            parent_task_id = payload.get('parent_task_id')
            new_task_id = payload.get('new_task_id')
            user_id = payload.get('user_id')
            
            print(f"Todo Service received recurring triggered event - parent: {parent_task_id}, new: {new_task_id}")
            
            # The recurring engine should have already created the new task,
            # but we can update the parent task to track its recurring instances
            if parent_task_id:
                task = await self.task_service.get_task_by_id(parent_task_id)
                if task:
                    # Update the parent task to track the new recurring instance
                    updated_data = {
                        "updated_at": datetime.now().isoformat()
                    }
                    await self.task_service.update_task(parent_task_id, updated_data)
            
            return {
                "handled": True, 
                "event_type": "recurring_triggered", 
                "parent_task_id": parent_task_id,
                "new_task_id": new_task_id
            }
        except Exception as e:
            print(f"Error handling recurring triggered event: {str(e)}")
            return {"handled": False, "error": str(e)}