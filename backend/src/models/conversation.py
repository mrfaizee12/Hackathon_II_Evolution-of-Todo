from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING
import uuid

if TYPE_CHECKING:
    from .user import User
    from .message import AIMessage


class AIConversationBase(SQLModel):
    title: str = Field(max_length=200)
    user_id: uuid.UUID = Field(foreign_key="user.id")


class AIConversation(AIConversationBase, table=True):
    """
    Represents a session of interaction between user and AI assistant,
    including message history and context.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    is_active: bool = Field(default=True)

    # Relationship to user who owns this conversation
    user: "User" = Relationship(back_populates="conversations")

    # Relationship to messages in this conversation
    messages: list["AIMessage"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def __repr__(self):
        return f"<AIConversation(id={self.id}, title='{self.title}')>"