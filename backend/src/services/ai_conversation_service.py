"""
Service for managing AI conversations and messages.
Handles creating, retrieving, and updating conversation data.
"""

from typing import List, Optional
from sqlmodel import Session, select
from datetime import datetime
from uuid import UUID
import uuid
from ..models.conversation import AIConversation, AIConversationBase
from ..models.message import AIMessage, AIMessageBase, MessageSenderType, MessageType


class AIConversationService:
    def __init__(self, session: Session):
        self.session = session

    def create_conversation(self, user_id: UUID, title: str = "New AI Conversation", commit: bool = True) -> AIConversation:
        """
        Create a new AI conversation for a user.

        Args:
            user_id: ID of the user creating the conversation
            title: Title for the conversation
            commit: Whether to commit the transaction immediately (default True)

        Returns:
            The created AIConversation object
        """
        conversation = AIConversation(
            id=uuid.uuid4(),
            title=title,
            user_id=user_id,
            is_active=True
        )
        self.session.add(conversation)
        if commit:
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: UUID) -> Optional[AIConversation]:
        """
        Get a conversation by its ID.

        Args:
            conversation_id: ID of the conversation to retrieve

        Returns:
            The AIConversation object or None if not found
        """
        statement = select(AIConversation).where(AIConversation.id == conversation_id)
        return self.session.exec(statement).first()

    def get_conversations_by_user(self, user_id: UUID, limit: int = 10, offset: int = 0) -> List[AIConversation]:
        """
        Get all conversations for a specific user.

        Args:
            user_id: ID of the user
            limit: Maximum number of conversations to return
            offset: Number of conversations to skip

        Returns:
            List of AIConversation objects
        """
        statement = select(AIConversation)\
            .where(AIConversation.user_id == user_id)\
            .order_by(AIConversation.updated_at.desc())\
            .offset(offset)\
            .limit(limit)
        return self.session.exec(statement).all()

    def update_conversation_title(self, conversation_id: UUID, new_title: str) -> Optional[AIConversation]:
        """
        Update the title of a conversation.

        Args:
            conversation_id: ID of the conversation to update
            new_title: New title for the conversation

        Returns:
            Updated AIConversation object or None if not found
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.title = new_title
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            self.session.refresh(conversation)
        return conversation

    def deactivate_conversation(self, conversation_id: UUID) -> bool:
        """
        Deactivate a conversation (soft delete).

        Args:
            conversation_id: ID of the conversation to deactivate

        Returns:
            True if successfully deactivated, False otherwise
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.is_active = False
            conversation.updated_at = datetime.utcnow()
            self.session.add(conversation)
            self.session.commit()
            return True
        return False

    def add_message_to_conversation(
        self,
        conversation_id: UUID,
        sender_type: str,
        content: str,
        message_type: str = MessageType.TEXT,
        metadata: Optional[dict] = None,
        commit: bool = True
    ) -> Optional['AIMessage']:
        """
        Add a message to a conversation.

        Args:
            conversation_id: ID of the conversation to add message to
            sender_type: Type of sender (USER or ASSISTANT)
            content: Content of the message
            message_type: Type of message (TEXT, ACTION_REQUEST, etc.)
            metadata: Additional metadata for the message
            commit: Whether to commit the transaction immediately (default True)

        Returns:
            Created AIMessage object or None if conversation not found
        """
        # Verify conversation exists
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        message = AIMessage(
            id=uuid.uuid4(),
            conversation_id=conversation_id,
            sender_type=sender_type,
            content=content,
            message_type=message_type,
            extra_metadata=metadata
        )
        self.session.add(message)
        # Update conversation's last activity time
        conversation.updated_at = datetime.utcnow()
        self.session.add(conversation)
        if commit:
            self.session.commit()
            self.session.refresh(message)
        return message

    def get_messages_by_conversation(
        self,
        conversation_id: UUID,
        limit: int = 50,
        offset: int = 0
    ) -> List['AIMessage']:
        """
        Get messages from a specific conversation.

        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of AIMessage objects
        """
        statement = select(AIMessage)\
            .where(AIMessage.conversation_id == conversation_id)\
            .order_by(AIMessage.created_at.asc())\
            .offset(offset)\
            .limit(limit)
        return self.session.exec(statement).all()

    def get_latest_message_in_conversation(self, conversation_id: UUID) -> Optional['AIMessage']:
        """
        Get the latest message in a conversation.

        Args:
            conversation_id: ID of the conversation

        Returns:
            Latest AIMessage object or None if no messages exist
        """
        statement = select(AIMessage)\
            .where(AIMessage.conversation_id == conversation_id)\
            .order_by(AIMessage.created_at.desc())\
            .limit(1)
        return self.session.exec(statement).first()

    def get_conversation_summary(self, conversation_id: UUID) -> Optional[dict]:
        """
        Get a summary of a conversation including message count and participants.

        Args:
            conversation_id: ID of the conversation

        Returns:
            Dictionary with conversation summary or None if not found
        """
        conversation = self.get_conversation_by_id(conversation_id)
        if not conversation:
            return None

        # Count messages
        message_statement = select(AIMessage).where(AIMessage.conversation_id == conversation_id)
        messages = self.session.exec(message_statement).all()
        message_count = len(messages)

        # Count messages by sender type
        user_msg_count = sum(1 for msg in messages if msg.sender_type == MessageSenderType.USER)
        assistant_msg_count = sum(1 for msg in messages if msg.sender_type == MessageSenderType.ASSISTANT)

        return {
            "id": str(conversation.id),
            "title": conversation.title,
            "created_at": conversation.created_at.isoformat(),
            "updated_at": conversation.updated_at.isoformat(),
            "is_active": conversation.is_active,
            "message_count": message_count,
            "user_message_count": user_msg_count,
            "assistant_message_count": assistant_msg_count
        }