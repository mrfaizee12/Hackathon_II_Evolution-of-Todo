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
    """Add new columns and indexes to the todo table."""
    engine = create_engine(DATABASE_URL)

    # List of columns to add and their SQL definitions
    columns_to_add = [
        ("priority", "VARCHAR(20) DEFAULT 'medium'"),
        ("tags", "TEXT DEFAULT ''"),
        ("due_date", "TIMESTAMP WITH TIME ZONE"),
        ("completed_at", "TIMESTAMP WITH TIME ZONE"),
        ("recurrence_type", "VARCHAR(20) DEFAULT 'none'"),
        ("recurrence_interval", "INTEGER"),
        ("next_occurrence", "TIMESTAMP WITH TIME ZONE"),
        ("reminder_at", "TIMESTAMP WITH TIME ZONE"),
    ]

    for column_name, column_definition in columns_to_add:
        with engine.connect() as conn:
            try:
                conn.execute(text(f"ALTER TABLE todo ADD COLUMN {column_name} {column_definition};"))
                conn.commit()
                print(f"Added {column_name} column to todo table")
            except Exception as e:
                print(f"{column_name.capitalize()} column may already exist or an error occurred: {e}")
                conn.rollback() # Rollback the current transaction on error

    # List of indexes to add
    indexes_to_add = [
        ("ix_user_due_date", "CREATE INDEX ix_user_due_date ON todo (user_id, due_date);"),
        ("ix_user_reminder_at", "CREATE INDEX ix_user_reminder_at ON todo (user_id, reminder_at);"),
        ("ix_next_occurrence", "CREATE INDEX ix_next_occurrence ON todo (next_occurrence);"),
    ]

    for index_name, index_sql in indexes_to_add:
        with engine.connect() as conn:
            try:
                conn.execute(text(index_sql))
                conn.commit()
                print(f"Added index {index_name} to todo table")
            except Exception as e:
                print(f"Index {index_name} may already exist or an error occurred: {e}")
                conn.rollback() # Rollback the current transaction on error

    print("Migration attempt completed.")

if __name__ == "__main__":
    run_migrations()
