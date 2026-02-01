from sqlmodel import create_engine, Session
from sqlalchemy import text
from typing import Generator
from .config import settings

# Create the database engine
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,  # Set to True for SQL query logging
    pool_pre_ping=True,     # Verify connections before use
    pool_recycle=300,      # Recycle connections after 5 minutes
)

def get_session() -> Generator[Session, None, None]:
    """
    Get a database session for dependency injection.
    """
    with Session(engine) as session:
        yield session

def init_db():
    """
    Initialize the database by creating all tables.
    This should be called once at application startup.
    """
    from ..models.user import User  # Import here to avoid circular imports
    from ..models.todo import Todo  # Import here to avoid circular imports
    from ..models.conversation import AIConversation  # Import to ensure relationships are registered
    from ..models.message import AIMessage  # Import to ensure relationships are registered

    from sqlmodel import SQLModel
    # Create all tables, including updating existing ones with new columns
    SQLModel.metadata.create_all(engine)