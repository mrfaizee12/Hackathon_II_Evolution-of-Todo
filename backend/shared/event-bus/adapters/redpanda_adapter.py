"""
Redpanda adapter implementation for event bus
"""

from typing import Any, Dict, Callable
from .kafka_adapter import KafkaEventBusAdapter


class RedpandaEventBusAdapter(KafkaEventBusAdapter):
    """
    Redpanda implementation of the EventBus interface
    Since Redpanda is Kafka-compatible, we can extend the Kafka adapter
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Redpanda event bus adapter
        
        Args:
            config: Configuration dictionary for Redpanda
        """
        # Redpanda uses the same protocol as Kafka, so we can use the same implementation
        super().__init__(config)