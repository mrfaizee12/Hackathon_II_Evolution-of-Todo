"""
Configuration-based switching mechanism for event bus
"""

from enum import Enum
from typing import Dict, Any
from .adapters.base_adapter import MockEventBusAdapter
from ..interface import EventBus


class EventBusType(Enum):
    """
    Supported event bus types
    """
    MOCK = "mock"
    KAFKA = "kafka"
    REDPANDA = "redpanda"
    NATS = "nats"


def create_event_bus(config: Dict[str, Any]) -> EventBus:
    """
    Factory function to create an event bus instance based on configuration
    
    Args:
        config: Configuration dictionary containing 'type' and other parameters
        
    Returns:
        An instance of the appropriate event bus implementation
    """
    event_bus_type = config.get('type', 'mock').lower()
    
    if event_bus_type == EventBusType.MOCK.value:
        return MockEventBusAdapter(config)
    elif event_bus_type == EventBusType.KAFKA.value:
        # Import Kafka adapter when needed to avoid dependency issues
        from .adapters.kafka_adapter import KafkaEventBusAdapter
        return KafkaEventBusAdapter(config)
    elif event_bus_type == EventBusType.REDPANDA.value:
        # Import Redpanda adapter when needed to avoid dependency issues
        from .adapters.redpanda_adapter import RedpandaEventBusAdapter
        return RedpandaEventBusAdapter(config)
    elif event_bus_type == EventBusType.NATS.value:
        # Import NATS adapter when needed to avoid dependency issues
        from .adapters.nats_adapter import NATSEventBusAdapter
        return NATSEventBusAdapter(config)
    else:
        raise ValueError(f"Unsupported event bus type: {event_bus_type}")


def get_default_config() -> Dict[str, Any]:
    """
    Get default configuration for event bus
    
    Returns:
        Default configuration dictionary
    """
    return {
        'type': 'mock',
        'connection_string': 'mock://localhost:9092',
        'topics': {
            'task_created': 'todo.task.created',
            'task_updated': 'todo.task.updated',
            'task_deleted': 'todo.task.deleted',
            'recurring_triggered': 'todo.recurring.triggered',
            'reminder_triggered': 'todo.reminder.triggered',
            'chatbot_event': 'todo.chatbot.event'
        }
    }