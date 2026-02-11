"""
Chatbot service for Chatbot Service
"""

from typing import Dict, Any, List
from datetime import datetime
import uuid
from .models.chatbot import ChatMessage, ChatAction


class ChatbotService:
    """
    Service class for handling chatbot business logic
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using an in-memory store for demonstration
        self.sessions = {}
        self.context = {}  # Store conversation context per user/session
    
    async def process_message(self, user_id: str, message: str, session_id: str) -> Dict[str, Any]:
        """
        Process a chat message and return a response
        """
        try:
            # Initialize session if it doesn't exist
            if session_id not in self.sessions:
                self.sessions[session_id] = []
            
            # Add user message to session
            user_msg = ChatMessage(
                id=str(uuid.uuid4()),
                sender="user",
                message=message,
                timestamp=datetime.now()
            )
            self.sessions[session_id].append(user_msg)
            
            # Simple NLP processing to identify intent and entities
            intent, entities, actions = self._parse_intent_and_entities(message)
            
            # Generate response based on intent
            reply = self._generate_response(intent, entities, user_id)
            
            # Add bot response to session
            bot_msg = ChatMessage(
                id=str(uuid.uuid4()),
                sender="bot",
                message=reply,
                timestamp=datetime.now()
            )
            self.sessions[session_id].append(bot_msg)
            
            # Update context
            if user_id not in self.context:
                self.context[user_id] = {}
            self.context[user_id]["last_intent"] = intent
            self.context[user_id]["last_entities"] = entities
            
            return {
                "reply": reply,
                "actions": [action.dict() for action in actions],
                "intent": intent,
                "entities": entities
            }
        except Exception as e:
            return {
                "reply": "Sorry, I encountered an error processing your message.",
                "actions": [],
                "intent": "error",
                "entities": {}
            }
    
    def _parse_intent_and_entities(self, message: str) -> tuple:
        """
        Simple intent and entity recognition
        In a real implementation, this would use NLP models
        """
        message_lower = message.lower()
        
        # Identify intent
        intent = "unknown"
        if any(word in message_lower for word in ["create", "add", "new", "make"]):
            intent = "create_task"
        elif any(word in message_lower for word in ["update", "change", "modify", "edit"]):
            intent = "update_task"
        elif any(word in message_lower for word in ["delete", "remove", "cancel"]):
            intent = "delete_task"
        elif any(word in message_lower for word in ["list", "show", "view", "get", "see"]):
            intent = "get_tasks"
        elif any(word in message_lower for word in ["hello", "hi", "hey", "greetings"]):
            intent = "greet"
        elif any(word in message_lower for word in ["help", "assist"]):
            intent = "help"
        
        # Extract entities (simple keyword matching)
        entities = {}
        if "today" in message_lower or "now" in message_lower:
            entities["due_date"] = datetime.now().strftime("%Y-%m-%d")
        elif "tomorrow" in message_lower:
            tomorrow = datetime.now().replace(day=datetime.now().day + 1)
            entities["due_date"] = tomorrow.strftime("%Y-%m-%d")
        
        # Extract title (everything after "to" or "called")
        if "to" in message:
            entities["title"] = message.split("to", 1)[1].strip()
        elif "called" in message:
            entities["title"] = message.split("called", 1)[1].strip()
        
        # Create actions based on intent
        actions = []
        if intent == "create_task":
            actions.append(ChatAction(
                type="create_task",
                params={
                    "title": entities.get("title", "Untitled task"),
                    "due_date": entities.get("due_date")
                }
            ))
        elif intent == "get_tasks":
            actions.append(ChatAction(
                type="get_tasks",
                params={}
            ))
        
        return intent, entities, actions
    
    def _generate_response(self, intent: str, entities: Dict[str, Any], user_id: str) -> str:
        """
        Generate a response based on intent and entities
        """
        if intent == "greet":
            return "Hello! How can I help you with your tasks today?"
        elif intent == "help":
            return "I can help you create, update, delete, and list tasks. Try saying 'Create a task to buy groceries'"
        elif intent == "create_task":
            title = entities.get("title", "a new task")
            return f"I've created the task '{title}' for you."
        elif intent == "get_tasks":
            return "Here are your tasks..."
        elif intent == "unknown":
            return "I'm not sure what you mean. Could you rephrase that? You can say 'help' for assistance."
        else:
            return "I've processed your request."
    
    async def get_chat_history(self, session_id: str) -> List[ChatMessage]:
        """
        Get chat history for a session
        """
        if session_id in self.sessions:
            return self.sessions[session_id]
        else:
            return []
    
    async def update_context_with_event(self, event_data: Dict[str, Any]):
        """
        Update chatbot context based on incoming events
        """
        user_id = event_data.get("user_id")
        if not user_id:
            return
        
        if user_id not in self.context:
            self.context[user_id] = {}
        
        # Update context based on event type
        event_type = event_data.get("type", "")
        if event_type == "task_created":
            task_title = event_data.get("payload", {}).get("title", "a task")
            if "recent_tasks" not in self.context[user_id]:
                self.context[user_id]["recent_tasks"] = []
            self.context[user_id]["recent_tasks"].append({
                "title": task_title,
                "timestamp": datetime.now().isoformat()
            })
        elif event_type == "task_updated":
            # Update context with task update information
            pass
        elif event_type == "reminder_triggered":
            # Update context with reminder information
            reminder_message = event_data.get("payload", {}).get("message", "")
            if "recent_reminders" not in self.context[user_id]:
                self.context[user_id]["recent_reminders"] = []
            self.context[user_id]["recent_reminders"].append({
                "message": reminder_message,
                "timestamp": datetime.now().isoformat()
            })