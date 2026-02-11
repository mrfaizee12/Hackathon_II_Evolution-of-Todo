"""
Kafka adapter implementation for event bus
"""

from typing import Any, Dict, Callable
from .base_adapter import BaseEventBusAdapter


class KafkaEventBusAdapter(BaseEventBusAdapter):
    """
    Kafka implementation of the EventBus interface
    """
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the Kafka event bus adapter
        
        Args:
            config: Configuration dictionary for Kafka
        """
        super().__init__(config)
        self.bootstrap_servers = config.get('bootstrap_servers', 'localhost:9092')
        self.producer = None
        self.consumer = None
    
    async def connect(self):
        """
        Establish connection to Kafka
        """
        # Import kafka library when needed to avoid dependency issues
        try:
            from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
        except ImportError:
            raise ImportError("aiokafka is required for Kafka adapter. Install with: pip install aiokafka")
        
        # Initialize producer and consumer
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()
        
        self._connected = True
    
    async def disconnect(self):
        """
        Disconnect from Kafka
        """
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()
        
        self._connected = False
    
    async def publish(self, topic: str, event_data: Dict[str, Any]) -> bool:
        """
        Publish an event to the specified topic
        """
        if not self._connected:
            await self.connect()
        
        try:
            # Serialize the event data
            import json
            serialized_data = json.dumps(event_data).encode('utf-8')
            
            # Send the message
            await self.producer.send_and_wait(topic, serialized_data)
            return True
        except Exception as e:
            print(f"Error publishing to Kafka: {e}")
            return False
    
    async def subscribe(self, topic: str, handler_func: Callable):
        """
        Subscribe to events from the specified topic
        """
        if not self._connected:
            await self.connect()
        
        try:
            from aiokafka import AIOKafkaConsumer
            import json
            
            # Create a consumer for the topic
            consumer = AIOKafkaConsumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                value_deserializer=lambda x: json.loads(x.decode('utf-8'))
            )
            await consumer.start()
            
            # Consume messages
            async for msg in consumer:
                try:
                    await handler_func(msg.value)
                except Exception as e:
                    print(f"Error processing message: {e}")
                    
        except Exception as e:
            print(f"Error subscribing to Kafka: {e}")
            raise