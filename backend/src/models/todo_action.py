from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class ActionType:
    ADD = "ADD"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    COMPLETE = "COMPLETE"
    LIST = "LIST"


class ActionStatus:
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class TodoActionBase(SQLModel):
    conversation_id: uuid.UUID = Field(foreign_key="aiconversation.id")
    message_id: uuid.UUID = Field(foreign_key="aimessage.id")
    action_type: str = Field(max_length=20)  # ADD, UPDATE, DELETE, COMPLETE, LIST
    todo_details: Optional[Dict[str, Any]] = Field(default=None, nullable=True)  # details about the todo being acted upon
    status: str = Field(max_length=20, default="PENDING")  # PENDING, PROCESSING, COMPLETED, FAILED
    result: Optional[str] = Field(default=None, max_length=1000)  # result of the action, if applicable


class TodoAction(TodoActionBase, table=True):
    """
    Represents actions performed on todo items through AI commands.
    """
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    # Relationships
    # conversation: "AIConversation" = Relationship(back_populates="todo_actions")
    # message: "AIMessage" = Relationship(back_populates="todo_actions")

    def __repr__(self):
        return f"<TodoAction(id={self.id}, type={self.action_type}, status={self.status})>"