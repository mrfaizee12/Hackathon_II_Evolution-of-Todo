"""
Structured logging for Chatbot Service
"""

from __future__ import absolute_import
import logging
import sys
from datetime import datetime
from typing import Dict, Any
import json
import traceback
from logging.handlers import RotatingFileHandler


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in a structured JSON format
    """
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'service': 'chatbot-service',
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
            'message': record.getMessage(),
        }
        
        # Add exception info if present
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        # Add any extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'getMessage', 'exc_info', 
                          'exc_text', 'stack_info']:
                log_entry[key] = value
        
        return json.dumps(log_entry)


def setup_logging(level=logging.INFO):
    """
    Set up structured logging for the Chatbot Service
    """
    logger = logging.getLogger()
    logger.setLevel(level)
    
    # Create console handler with structured formatter
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter())
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Add console handler
    logger.addHandler(console_handler)
    
    return logger


def add_correlation_id(correlation_id: str = None):
    """
    Add a correlation ID to the logging context
    """
    # In a real implementation, this would use a context variable
    # For now, we'll just return the correlation ID
    return correlation_id or f"corr_{int(datetime.now().timestamp())}"


def log_message_processed(user_id: str, session_id: str, message: str, 
                       reply: str, correlation_id: str = None):
    """
    Log a chat message being processed
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Message Processed",
        extra={
            'correlation_id': correlation_id,
            'user_id': user_id,
            'session_id': session_id,
            'input_message': message,
            'output_reply': reply
        }
    )


def log_intent_detected(user_id: str, intent: str, entities: Dict[str, Any], 
                      correlation_id: str = None):
    """
    Log an intent being detected
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Intent Detected",
        extra={
            'correlation_id': correlation_id,
            'user_id': user_id,
            'intent': intent,
            'entities': entities
        }
    )


def log_action_performed(action_type: str, params: Dict[str, Any], 
                       correlation_id: str = None):
    """
    Log an action being performed
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Action Performed",
        extra={
            'correlation_id': correlation_id,
            'action_type': action_type,
            'params': params
        }
    )


def log_context_updated(user_id: str, context_changes: Dict[str, Any], 
                      correlation_id: str = None):
    """
    Log the chatbot context being updated
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Context Updated",
        extra={
            'correlation_id': correlation_id,
            'user_id': user_id,
            'context_changes': context_changes
        }
    )


def log_error(error: Exception, correlation_id: str = None, context: Dict[str, Any] = None):
    """
    Log an error with structured format
    """
    logger = logging.getLogger(__name__)
    logger.error(
        str(error),
        extra={
            'correlation_id': correlation_id,
            'error_type': type(error).__name__,
            'context': context or {}
        },
        exc_info=True
    )


def log_event_consumed(event_type: str, event_id: str, correlation_id: str = None):
    """
    Log an event consumption
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Event Consumed",
        extra={
            'correlation_id': correlation_id,
            'event_type': event_type,
            'event_id': event_id
        }
    )


def log_event_published(event_type: str, event_id: str, correlation_id: str = None):
    """
    Log an event publication
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Event Published",
        extra={
            'correlation_id': correlation_id,
            'event_type': event_type,
            'event_id': event_id
        }
    )


# Initialize the logger
logger = setup_logging()