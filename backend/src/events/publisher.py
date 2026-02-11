from abc import ABC, abstractmethod
from typing import Any, List, Dict

class EventPublisher(ABC):
    """
    Abstract base class for event publishers.
    Defines the interface for publishing events to an event bus or message queue.
    """
    @abstractmethod
    def publish(self, event_name: str, event_data: Any) -> None:
        """
        Publishes an event.

        Args:
            event_name: The name or type of the event.
            event_data: The data payload of the event.
        """
        pass

class InMemoryEventPublisher(EventPublisher):
    """
    An in-memory implementation of EventPublisher for testing and development.
    """
    def __init__(self):
        self.events = []

    def publish(self, event_name: str, event_data: Any) -> None:
        """
        Publishes an event by storing it in memory.
        """
        self.events.append({"event_name": event_name, "event_data": event_data})
        print(f"Published event (in-memory): {event_name} - {event_data}")

    def get_published_events(self) -> List[Dict[str, Any]]:
        """
        Returns all events published to this in-memory publisher.
        """
        return self.events

    def clear_events(self) -> None:
        """
        Clears all published events from memory.
        """
        self.events = []
