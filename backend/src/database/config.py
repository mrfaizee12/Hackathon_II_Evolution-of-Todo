from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    database_url: str = "postgresql://username:password@localhost:5432/todo_app"
    db_echo: bool = False  # Set to True for SQL query logging
    secret_key: str = "your-secret-key-here"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openrouter_api_key: str

    model_config = {"env_file": ".env"}

settings = Settings()