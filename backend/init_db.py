import sys
import os
# Add the backend directory to the Python path to allow proper imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel
from src.database.config import settings
from src.database.database import engine

def create_db_and_tables():
    """
    Create database tables after resolving circular imports
    """
    # Import models to register them with SQLModel before creating tables
    # This resolves the circular import issue
    from src.models import user
    from src.models import todo

    print("Creating tables in database...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()