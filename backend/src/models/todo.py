from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class TodoBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    """
    Todo entity representing a task item with content, completion status, and user association.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")

class TodoCreate(TodoBase):
    """
    Schema for creating a new todo.
    """
    title: str = Field(min_length=1, max_length=255)

class TodoRead(TodoBase):
    """
    Schema for reading todo data.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    """
    Schema for updating todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TodoPatchStatus(SQLModel):
    """
    Schema for updating todo completion status.
    """
    completed: bool