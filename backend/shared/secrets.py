"""
Secrets management for services
"""

import os
from typing import Optional
from pydantic import BaseSettings


class SecretsManager:
    """
    Manager for handling secrets and sensitive configuration
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a secrets store
        # For now, we'll use environment variables as the source
        pass
    
    def get_secret(self, secret_name: str) -> Optional[str]:
        """
        Retrieve a secret by name
        
        Args:
            secret_name: Name of the secret to retrieve
            
        Returns:
            The secret value or None if not found
        """
        # In a real implementation, this would fetch from a secure store
        # like HashiCorp Vault, AWS Secrets Manager, etc.
        # For now, we'll get it from environment variables
        return os.getenv(secret_name)
    
    def get_database_url(self) -> str:
        """
        Get the database URL from secrets
        
        Returns:
            Database URL string
        """
        db_url = self.get_secret("DB_URL")
        if not db_url:
            # Fallback to the default from the .env file
            db_url = os.getenv("DATABASE_URL", "")
        return db_url
    
    def get_openrouter_api_key(self) -> str:
        """
        Get the OpenRouter API key from secrets
        
        Returns:
            OpenRouter API key string
        """
        api_key = self.get_secret("OPENROUTER_API_KEY")
        if not api_key:
            # Fallback to the default from the .env file
            api_key = os.getenv("OPENROUTER_API_KEY", "")
        return api_key
    
    def get_secret_key(self) -> str:
        """
        Get the secret key for JWT signing
        
        Returns:
            Secret key string
        """
        secret_key = self.get_secret("SECRET_KEY")
        if not secret_key:
            # Fallback to the default from the .env file
            secret_key = os.getenv("SECRET_KEY", "a5fc2776eecd3988b703c53fa959331099a9fc24d7190b0d62a244b5f4b09c54")
        return secret_key


# Global instance
secrets_manager = SecretsManager()