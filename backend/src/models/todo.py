from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
import uuid
from pydantic import field_validator, field_serializer

# Handle circular import for relationship
if TYPE_CHECKING:
    from .user import User

class TodoBase(SQLModel):
    title: str = Field(nullable=False, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)
    priority: str = Field(default="medium", nullable=False)  # enum: low, medium, high
    tags: str = Field(default="", nullable=False)  # comma-separated tags
    due_date: Optional[datetime] = Field(default=None)
    # AI Integration Fields
    ai_generated: bool = Field(default=False)  # indicates if todo was created via AI
    ai_context: Optional[str] = Field(default=None, max_length=500)  # context from AI conversation

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
    priority: Optional[str] = Field(default="medium", max_length=20)  # enum: low, medium, high
    tags: Optional[str] = Field(default="", max_length=500)  # comma-separated tags
    ai_generated: bool = Field(default=False)  # indicates if todo was created via AI
    ai_context: Optional[str] = Field(default=None, max_length=500)  # context from AI conversation

    @field_validator('priority')
    def validate_priority(cls, value):
        if value and value not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be one of: low, medium, high')
        return value

    @field_validator('tags')
    def validate_tags(cls, value):
        if value:
            tags_list = [tag.strip() for tag in value.split(',') if tag.strip()]
            if len(tags_list) > 10:
                raise ValueError('Maximum 10 tags allowed per todo')
            for tag in tags_list:
                if len(tag) > 50:
                    raise ValueError('Each tag must be 50 characters or less')
        return value

class TodoRead(TodoBase):
    """
    Schema for reading todo data.
    """
    id: uuid.UUID
    user_id: uuid.UUID
    priority: str
    tags: str
    due_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    @field_serializer('priority')
    def serialize_priority(self, value: Optional[str]) -> str:
        # If priority is None, return default "medium"
        if value is None:
            return "medium"
        return value

class TodoUpdate(SQLModel):
    """
    Schema for updating todo information.
    """
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    priority: Optional[str] = None
    tags: Optional[str] = None
    due_date: Optional[datetime] = None
    ai_generated: Optional[bool] = None
    ai_context: Optional[str] = None

    @field_validator('priority')
    def validate_priority(cls, value):
        if value and value not in ['low', 'medium', 'high']:
            raise ValueError('Priority must be one of: low, medium, high')
        return value

    @field_validator('tags')
    def validate_tags(cls, value):
        if value:
            tags_list = [tag.strip() for tag in value.split(',') if tag.strip()]
            if len(tags_list) > 10:
                raise ValueError('Maximum 10 tags allowed per todo')
            for tag in tags_list:
                if len(tag) > 50:
                    raise ValueError('Each tag must be 50 characters or less')
        return value

class TodoPatchStatus(SQLModel):
    """
    Schema for updating todo completion status.
    """
    completed: bool