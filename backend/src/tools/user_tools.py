"""
MCP (Model Context Protocol) Tools for User Identity Access
These tools allow the AI agent to access user information.
"""

from typing import Optional
from pydantic import BaseModel
from sqlmodel import Session, select
from ..models.user import User


class GetUserIdentityInput(BaseModel):
    """Input for getting user identity information."""
    pass  # No parameters needed, user info comes from authentication context


def get_user_identity(user_id: str, db_session: Session) -> dict:
    """
    Get user identity information.

    Args:
        user_id: ID of the user (passed from authentication context)
        db_session: Database session

    Returns:
        Dictionary with user identity information
    """
    try:
        # Query for the user
        statement = select(User).where(User.id == user_id)
        user = db_session.exec(statement).first()

        if not user:
            return {
                "success": False,
                "message": "User not found"
            }

        # Return user identity information
        return {
            "success": True,
            "user_info": {
                "id": str(user.id),
                "email": user.email,
                "name": user.name,
                "full_name": user.name
            }
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to retrieve user information: {str(e)}"
        }