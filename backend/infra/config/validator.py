"""
Configuration validation mechanisms
"""

import os
from typing import Dict, Any, List
from pydantic import BaseModel, ValidationError, validator
import yaml


class ServiceConfig(BaseModel):
    """
    Base configuration model for services
    """
    service_name: str
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    
    # Database configuration
    db_url: str  # Required field - no default to ensure it's provided
    db_pool_size: int = 5
    
    # Event bus configuration
    event_bus_type: str = "redpanda"  # Default to redpanda for event-driven architecture
    event_bus_config: Dict[str, Any] = {}
    
    # Dapr configuration
    dapr_enabled: bool = True
    dapr_port: int = 3500
    dapr_grpc_port: int = 50001
    
    # Security and API keys
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    openrouter_api_key: str
    
    class Config:
        env_file = ".env"
        extra = "allow"


def validate_config(config_data: Dict[str, Any]) -> ServiceConfig:
    """
    Validate configuration data against the ServiceConfig model
    
    Args:
        config_data: Dictionary containing configuration values
        
    Returns:
        Validated ServiceConfig object
        
    Raises:
        ValidationError: If configuration is invalid
    """
    try:
        config = ServiceConfig(**config_data)
        return config
    except ValidationError as e:
        raise ValidationError(f"Invalid configuration: {e}")


def load_config_from_env() -> ServiceConfig:
    """
    Load configuration from environment variables
    
    Returns:
        Validated ServiceConfig object
    """
    config_dict = {}
    
    # Load common environment variables
    env_vars = [
        'SERVICE_NAME', 'DEBUG', 'HOST', 'PORT', 'ENVIRONMENT',
        'DB_URL', 'DB_POOL_SIZE', 'EVENT_BUS_TYPE', 'DAPR_ENABLED',
        'DAPR_PORT', 'DAPR_GRPC_PORT'
    ]
    
    for var in env_vars:
        value = os.getenv(var)
        if value is not None:
            # Convert string values to appropriate types
            if var in ['DEBUG', 'DAPR_ENABLED']:
                config_dict[var.lower()] = value.lower() in ('true', '1', 'yes', 'on')
            elif var in ['PORT', 'DB_POOL_SIZE', 'DAPR_PORT', 'DAPR_GRPC_PORT']:
                config_dict[var.lower()] = int(value)
            else:
                config_dict[var.lower()] = value
    
    # Load event bus config from environment
    event_bus_config_str = os.getenv('EVENT_BUS_CONFIG', '{}')
    import json
    try:
        config_dict['event_bus_config'] = json.loads(event_bus_config_str)
    except json.JSONDecodeError:
        config_dict['event_bus_config'] = {}
    
    return validate_config(config_dict)


def load_config_from_file(file_path: str) -> ServiceConfig:
    """
    Load configuration from a YAML file
    
    Args:
        file_path: Path to the configuration file
        
    Returns:
        Validated ServiceConfig object
    """
    with open(file_path, 'r') as f:
        config_data = yaml.safe_load(f)
    
    return validate_config(config_data)


def validate_required_vars(required_vars: List[str]) -> bool:
    """
    Validate that required environment variables are set
    
    Args:
        required_vars: List of required environment variable names
        
    Returns:
        True if all required variables are set, False otherwise
    """
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"Missing required environment variables: {', '.join(missing_vars)}")
        return False
    
    return True