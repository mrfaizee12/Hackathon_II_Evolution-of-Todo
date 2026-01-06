"""
Database migration script to add new fields to the todo table for Phase II Intermediate features.
"""
from sqlmodel import SQLModel, create_engine
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL", "")

def run_migrations():
    """Add new columns to the todo table."""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Add priority column
        try:
            conn.execute(text("ALTER TABLE todo ADD COLUMN priority VARCHAR(20) DEFAULT 'medium';"))
            print("Added priority column to todo table")
        except Exception as e:
            print(f"Priority column may already exist: {e}")

        # Add tags column
        try:
            conn.execute(text("ALTER TABLE todo ADD COLUMN tags TEXT DEFAULT '';"))
            print("Added tags column to todo table")
        except Exception as e:
            print(f"Tags column may already exist: {e}")

        # Add due_date column
        try:
            conn.execute(text("ALTER TABLE todo ADD COLUMN due_date TIMESTAMP WITH TIME ZONE;"))
            print("Added due_date column to todo table")
        except Exception as e:
            print(f"Due date column may already exist: {e}")

        # Add completed_at column
        try:
            conn.execute(text("ALTER TABLE todo ADD COLUMN completed_at TIMESTAMP WITH TIME ZONE;"))
            print("Added completed_at column to todo table")
        except Exception as e:
            print(f"Completed at column may already exist: {e}")

        conn.commit()
        print("Migration completed successfully!")

if __name__ == "__main__":
    run_migrations()
