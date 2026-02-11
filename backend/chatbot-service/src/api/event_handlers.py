"""
Event handlers for Chatbot Service
"""

from typing import Dict, Any
import asyncio
from datetime import datetime
from .services.chatbot_service import ChatbotService


class ChatbotServiceEventHandler:
    """
    Event handler class for processing events in the Chatbot Service
    """
    
    def __init__(self):
        self.chatbot_service = ChatbotService()
    
    async def handle_task_created_event(self, event_data: Dict[str, Any]):
        """
        Handle task created events - update chatbot context
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            title = payload.get('title')
            user_id = payload.get('user_id')
            
            print(f"Chatbot Service received task created event for task {task_id} by user {user_id}")
            
            # Update chatbot context with the new task
            await self.chatbot_service.update_context_with_event({
                "type": "task_created",
                "payload": {
                    "task_id": task_id,
                    "title": title,
                    "user_id": user_id
                }
            })
            
            return {
                "handled": True,
                "event_type": "task_created",
                "task_id": task_id,
                "user_id": user_id,
                "context_updated": True
            }
        except Exception as e:
            print(f"Error handling task created event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_task_updated_event(self, event_data: Dict[str, Any]):
        """
        Handle task updated events - update chatbot context
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            updates = payload.get('updates', {})
            user_id = payload.get('user_id')
            
            print(f"Chatbot Service received task updated event for task {task_id} by user {user_id}")
            
            # Update chatbot context with the task update
            await self.chatbot_service.update_context_with_event({
                "type": "task_updated",
                "payload": {
                    "task_id": task_id,
                    "updates": updates,
                    "user_id": user_id
                }
            })
            
            return {
                "handled": True,
                "event_type": "task_updated",
                "task_id": task_id,
                "user_id": user_id,
                "context_updated": True
            }
        except Exception as e:
            print(f"Error handling task updated event: {str(e)}")
            return {"handled": False, "error": str(e)}
    
    async def handle_reminder_triggered_event(self, event_data: Dict[str, Any]):
        """
        Handle reminder triggered events - update chatbot context and potentially notify user
        """
        try:
            payload = event_data.get('payload', {})
            task_id = payload.get('task_id')
            user_id = payload.get('user_id')
            message = payload.get('message', '')
            
            print(f"Chatbot Service received reminder triggered event for task {task_id} for user {user_id}")
            
            # Update chatbot context with the reminder
            await self.chatbot_service.update_context_with_event({
                "type": "reminder_triggered",
                "payload": {
                    "task_id": task_id,
                    "message": message,
                    "user_id": user_id
                }
            })
            
            # Potentially send a proactive notification to the user through the chatbot
            # This would involve updating the user's session with a reminder message
            if user_id and task_id:
                # In a real implementation, we might add a message to the user's chat session
                # indicating that a reminder was triggered
                pass
            
            return {
                "handled": True,
                "event_type": "reminder_triggered",
                "task_id": task_id,
                "user_id": user_id,
                "context_updated": True
            }
        except Exception as e:
            print(f"Error handling reminder triggered event: {str(e)}")
            return {"handled": False, "error": str(e)}