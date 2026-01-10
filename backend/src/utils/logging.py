import logging
from datetime import datetime
from typing import Any, Dict

# Configure the root logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()  # Output to console
    ]
)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the specified name.
    """
    return logging.getLogger(name)

def log_api_call(
    endpoint: str,
    method: str,
    user_id: str = None,
    status_code: int = None,
    response_time: float = None
) -> None:
    """
    Log API call information.
    """
    logger = get_logger("api")
    message = f"API Call: {method} {endpoint}"
    if user_id:
        message += f" by user {user_id}"
    if status_code:
        message += f" - Status: {status_code}"
    if response_time:
        message += f" - Response time: {response_time:.2f}ms"

    logger.info(message)

def log_error(error: Exception, context: str = "") -> None:
    """
    Log error information with context.
    """
    logger = get_logger("error")
    logger.error(f"Error in {context}: {str(error)}", exc_info=True)

def log_user_action(action: str, user_id: str, details: Dict[str, Any] = None) -> None:
    """
    Log user action for audit trail.
    """
    logger = get_logger("user_action")
    message = f"User {user_id} performed action: {action}"
    if details:
        message += f" with details: {details}"

    logger.info(message)