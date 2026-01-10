from sqlmodel import SQLModel
from src.database.config import settings
from src.database.database import engine

def create_db_and_tables():
    """
    Create database tables after resolving circular imports
    """
    # Import models to register them with SQLModel before creating tables
    # This resolves the circular import issue
    import src.models.user
    import src.models.todo

    print("Creating tables in database...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_db_and_tables()