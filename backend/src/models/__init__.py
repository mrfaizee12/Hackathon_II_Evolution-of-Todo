"""
Model registration module to ensure all SQLModel models are properly registered
before relationships are resolved.
"""

# Import all models to ensure they're registered with SQLModel
from .user import User
from .todo import Todo
from .conversation import AIConversation
from .message import AIMessage

__all__ = ["User", "Todo", "AIConversation", "AIMessage"]