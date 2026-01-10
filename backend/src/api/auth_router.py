from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta

from ..models.user import User, UserCreate, UserLogin, UserRead
from ..database.database import get_session
from ..middleware.auth import get_current_active_user
from ..services.auth_service import (
    authenticate_user,
    create_user,
    create_access_token
)
from ..database.config import settings

auth_router = APIRouter()

@auth_router.post("/auth/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup(
    user_create: UserCreate,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.
    """
    try:
        user = create_user(session, user_create)
        return UserRead(
            id=user.id,
            email=user.email,
            name=user.name,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    except HTTPException:
        # Re-raise the HTTPException from create_user
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user"
        )


@auth_router.post("/auth/signin")
def signin(
    user_login: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate existing user and return token.
    """
    user = authenticate_user(session, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    return {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        },
        "token": access_token
    }


@auth_router.post("/auth/signout", status_code=status.HTTP_200_OK)
def signout():
    """
    Invalidate user session/token.
    """
    return {"message": "Successfully signed out"}


@auth_router.get("/auth/me", response_model=UserRead)
def read_users_me(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get information about the currently authenticated user.
    This endpoint requires authentication.
    """
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at
    )