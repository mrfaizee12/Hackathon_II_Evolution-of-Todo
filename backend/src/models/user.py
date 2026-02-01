from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
from datetime import datetime
import uuid

# Handle circular import for relationship
if TYPE_CHECKING:
    from .todo import Todo
    from .conversation import AIConversation

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False, max_length=255)
    name: str = Field(nullable=False, max_length=255)

class User(UserBase, table=True):
    """
    User entity representing an authenticated user with credentials.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    password_hash: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: List["Todo"] = Relationship(back_populates="user")

    # Relationship to conversations
    conversations: List["AIConversation"] = Relationship(back_populates="user")

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    """
    password: str = Field(min_length=8)

class UserRead(UserBase):
    """
    Schema for reading user data (without sensitive information).
    """
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    """
    Schema for updating user information.
    """
    email: Optional[str] = None
    name: Optional[str] = None

class UserLogin(SQLModel):
    """
    Schema for user login credentials.
    """
    email: str
    password: str