from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
from sqlalchemy import Column, JSON


class MessageSenderType:
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class MessageType:
    TEXT = "TEXT"
    ACTION_REQUEST = "ACTION_REQUEST"
    ACTION_RESULT = "ACTION_RESULT"
    SYSTEM = "SYSTEM"


class AIMessageBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="aiconversation.id")
    sender_type: str = Field(max_length=20)  # USER or ASSISTANT
    content: str = Field(sa_column_kwargs={"server_default": ""})
    message_type: str = Field(max_length=30, default="TEXT")  # TEXT, ACTION_REQUEST, etc.
    extra_metadata: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))


class AIMessage(AIMessageBase, table=True):
    """
    Represents individual messages exchanged between user and AI assistant.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationship to the conversation this message belongs to
    conversation: "AIConversation" = Relationship(back_populates="messages")

    def __repr__(self):
        return f"<AIMessage(id={self.id}, sender={self.sender_type}, type={self.message_type})>"