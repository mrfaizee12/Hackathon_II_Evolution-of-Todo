"""
Models for Chatbot Service
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime


class ProcessMessageRequest(BaseModel):
    """
    Request model for processing a chat message
    """
    user_id: str
    message: str
    session_id: str


class ChatAction(BaseModel):
    """
    Model for actions that the chatbot can take
    """
    type: str  # create_task, update_task, get_tasks, etc.
    params: Dict[str, Any]


class ProcessMessageResponse(BaseModel):
    """
    Response model for processing a chat message
    """
    reply: str
    actions: List[ChatAction]
    intent: Optional[str] = None
    entities: Optional[Dict[str, Any]] = None


class ChatMessage(BaseModel):
    """
    Model for a chat message
    """
    id: str
    sender: str  # user or bot
    message: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    """
    Response model for chat history
    """
    messages: List[ChatMessage]