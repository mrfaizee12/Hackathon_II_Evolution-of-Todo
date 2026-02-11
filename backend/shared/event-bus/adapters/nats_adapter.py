"""
NATS adapter implementation for event bus
"""

from typing import Any, Dict, Callable
from .base_adapter import BaseEventBusAdapter


class NATSEventBusAdapter(BaseEventBusAdapter):
    """
    NATS implementation of the EventBus interface
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the NATS event bus adapter
        
        Args:
            config: Configuration dictionary for NATS
        """
        super().__init__(config)
        self.servers = config.get('servers', ['nats://localhost:4222'])
        self.nc = None
        self.js = None
    
    async def connect(self):
        """
        Establish connection to NATS
        """
        try:
            import nats
        except ImportError:
            raise ImportError("nats-py is required for NATS adapter. Install with: pip install nats-py")
        
        # Connect to NATS
        self.nc = await nats.connect(servers=self.servers)
        self.js = self.nc.jetstream()
        
        self._connected = True
    
    async def disconnect(self):
        """
        Disconnect from NATS
        """
        if self.nc:
            await self.nc.close()
        
        self._connected = False
    
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified subject (NATS term for topic)
        """
        if not self._connected:
            await self.connect()
        
        try:
            import json
            serialized_data = json.dumps(event_data).encode('utf-8')
            
            # Publish to NATS subject
            await self.js.publish(topic, serialized_data)
            return True
        except Exception as e:
            print(f"Error publishing to NATS: {e}")
            return False
    
    async def subscribe(self, topic: str, handler_func: Callable):
        """
        Subscribe to events from the specified subject
        """
        if not self._connected:
            await self.connect()
        
        try:
            import json
            
            # Subscribe to NATS subject
            async def message_handler(msg):
                try:
                    data = json.loads(msg.data.decode())
                    await handler_func(data)
                except Exception as e:
                    print(f"Error processing message: {e}")
            
            # Create subscription
            await self.js.subscribe(topic, cb=message_handler)
            
        except Exception as e:
            print(f"Error subscribing to NATS: {e}")
            raise