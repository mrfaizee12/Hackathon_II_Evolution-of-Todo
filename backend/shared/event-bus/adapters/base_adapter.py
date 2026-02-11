"""
Base adapter implementation for event bus
"""

import asyncio
from typing import Any, Dict, Callable
from ..interface import EventBus, EventPublisher, EventSubscriber


class BaseEventBusAdapter(EventBus):
    """
    Base implementation of the EventBus interface
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the event bus adapter with configuration
        
        Args:
            config: Configuration dictionary for the event bus
        """
        self.config = config
        self._connected = False
    
    async def connect(self):
        """
        Establish connection to the event bus
        """
        self._connected = True
    
    async def disconnect(self):
        """
        Disconnect from the event bus
        """
        self._connected = False
    
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic
        """
        if not self._connected:
            raise RuntimeError("EventBus not connected")
        
        # This method should be overridden by specific implementations
        raise NotImplementedError("publish method must be implemented by subclasses")
    
    async def subscribe(self, topic: str, handler_func: Callable):
        """
        Subscribe to events from the specified topic
        """
        if not self._connected:
            raise RuntimeError("EventBus not connected")
        
        # This method should be overridden by specific implementations
        raise NotImplementedError("subscribe method must be implemented by subclasses")


class MockEventBusAdapter(BaseEventBusAdapter):
    """
    Mock implementation of the EventBus for testing purposes
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__(config or {})
        self.events = []
        self.subscribers = {}
    
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic
        """
        if not self._connected:
            await self.connect()
        
        event = {
            'topic': topic,
            'data': event_data,
            'timestamp': asyncio.get_event_loop().time()
        }
        
        self.events.append(event)
        
        # Notify subscribers
        if topic in self.subscribers:
            for handler in self.subscribers[topic]:
                await handler(event_data)
        
        return True
    
    async def subscribe(self, topic: str, handler_func: Callable):
        """
        Subscribe to events from the specified topic
        """
        if not self._connected:
            await self.connect()
        
        if topic not in self.subscribers:
            self.subscribers[topic] = []
        
        self.subscribers[topic].append(handler_func)