"""
Abstract interfaces for event publishing/subscribing
"""

from abc import ABC, abstractmethod
from typing import Any, Dict


class EventPublisher(ABC):
    """
    Abstract interface for publishing events to the event bus
    """
    
    @abstractmethod
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic
        
        Args:
            topic: The topic to publish the event to
            event_data: The event data to publish
            
        Returns:
            True if the event was published successfully, False otherwise
        """
        pass


class EventSubscriber(ABC):
    """
    Abstract interface for subscribing to events from the event bus
    """
    
    @abstractmethod
    async def subscribe(self, topic: str, handler_func):
        """
        Subscribe to events from the specified topic
        
        Args:
            topic: The topic to subscribe to
            handler_func: The function to handle incoming events
        """
        pass


class EventBus(ABC):
    """
    Combined interface for both publishing and subscribing
    """
    
    @abstractmethod
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic
        """
        pass
    
    @abstractmethod
    async def subscribe(self, topic: str, handler_func):
        """
        Subscribe to events from the specified topic
        """
        pass