"""
API endpoints for Chatbot Service following OpenAPI contract
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import uuid
from datetime import datetime

# Handle imports based on PYTHONPATH in container
try:
    from models.chatbot import ProcessMessageRequest, ChatHistoryResponse
    from services.chatbot_service import ChatbotService
    from shared.event_bus import create_event_bus, get_default_config
except ImportError:
    # Fallback for when running in container with different PYTHONPATH
    from models.chatbot import ProcessMessageRequest, ChatHistoryResponse
    from services.chatbot_service import ChatbotService
    from shared.event_bus import create_event_bus, get_default_config

router = APIRouter(prefix="/api/v1/chat", tags=["chatbot"])

# Initialize event bus
event_bus_config = get_default_config()
event_bus = create_event_bus(event_bus_config)

# Initialize chatbot service
chatbot_service = ChatbotService()


@router.post("/process", response_model=dict)
async def process_chat_message(request: ProcessMessageRequest, background_tasks: BackgroundTasks):
    """
    Process a chat message and return a response
    """
    try:
        result = await chatbot_service.process_message(
            request.user_id,
            request.message,
            request.session_id
        )
        
        # Publish chatbot event
        event_payload = {
            "user_id": request.user_id,
            "session_id": request.session_id,
            "input_message": request.message,
            "output_reply": result["reply"],
            "actions": result.get("actions", []),
            "timestamp": datetime.now().isoformat(),
            "intent": result.get("intent", ""),
            "entities": result.get("entities", {})
        }
        
        background_tasks.add_task(
            event_bus.publish, 
            "todo.chatbot.event", 
            event_payload
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")


@router.get("/history/{session_id}", response_model=ChatHistoryResponse)
async def get_chat_history(session_id: str):
    """
    Get chat history for a session
    """
    try:
        history = await chatbot_service.get_chat_history(session_id)
        return ChatHistoryResponse(messages=history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving chat history: {str(e)}")