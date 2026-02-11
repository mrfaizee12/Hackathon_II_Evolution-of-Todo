"""
Structured logging for Recurring Engine
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
            'service': 'recurring-engine',
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
    Set up structured logging for the Recurring Engine
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


def log_schedule_creation(schedule_id: str, task_id: str, pattern: Dict[str, Any], 
                        correlation_id: str = None):
    """
    Log a recurring schedule creation
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Recurring Schedule Created",
        extra={
            'correlation_id': correlation_id,
            'schedule_id': schedule_id,
            'task_id': task_id,
            'pattern': pattern
        }
    )


def log_schedule_execution(schedule_id: str, task_id: str, 
                         correlation_id: str = None):
    """
    Log a recurring schedule execution
    """
    logger = logging.getLogger(__name__)
    logger.info(
        "Recurring Schedule Executed",
        extra={
            'correlation_id': correlation_id,
            'schedule_id': schedule_id,
            'task_id': task_id
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