"""
Transactional outbox pattern implementation for Todo Service
"""

from typing import Dict, Any, List
import asyncio
import json
from datetime import datetime, timedelta
from enum import Enum


class EventType(Enum):
    """
    Types of events that can be stored in the outbox
    """
    TASK_CREATED = "task-created"
    TASK_UPDATED = "task-updated"
    TASK_DELETED = "task-deleted"


class OutboxEntry:
    """
    Represents an entry in the transactional outbox
    """
    def __init__(self, event_type: EventType, payload: Dict[str, Any], 
                 correlation_id: str = None, partition_key: str = None):
        self.id = f"outbox_{int(datetime.now().timestamp())}_{hash(str(payload)) % 10000}"
        self.event_type = event_type
        self.payload = payload
        self.created_at = datetime.now()
        self.published = False
        self.published_at = None
        self.correlation_id = correlation_id or f"corr_{self.id}"
        self.partition_key = partition_key or self.id


class TransactionalOutbox:
    """
    Implements the transactional outbox pattern to ensure
    events are published consistently with database transactions
    """
    
    def __init__(self):
        # In a real implementation, this would connect to a database
        # For now, using an in-memory store for demonstration
        self.outbox_entries: List[OutboxEntry] = []
        self.published_entries: List[OutboxEntry] = []
    
    async def save_event(self, event_type: EventType, payload: Dict[str, Any], 
                         correlation_id: str = None, partition_key: str = None):
        """
        Save an event to the outbox as part of a database transaction
        """
        entry = OutboxEntry(event_type, payload, correlation_id, partition_key)
        self.outbox_entries.append(entry)
        return entry.id
    
    async def publish_pending_events(self, event_publisher):
        """
        Publish all pending events in the outbox
        """
        pending_entries = [entry for entry in self.outbox_entries if not entry.published]
        published_count = 0
        
        for entry in pending_entries:
            try:
                # Publish the event using the provided publisher
                success = await event_publisher.publish(
                    f"todo.{entry.event_type.value}",
                    {
                        "id": entry.id,
                        "type": entry.event_type.value,
                        "payload": entry.payload,
                        "timestamp": entry.created_at.isoformat(),
                        "correlation_id": entry.correlation_id,
                        "partition_key": entry.partition_key
                    }
                )
                
                if success:
                    entry.published = True
                    entry.published_at = datetime.now()
                    self.published_entries.append(entry)
                    # Remove from pending entries
                    self.outbox_entries.remove(entry)
                    published_count += 1
                else:
                    print(f"Failed to publish outbox entry {entry.id}")
                    
            except Exception as e:
                print(f"Error publishing outbox entry {entry.id}: {str(e)}")
        
        return published_count
    
    async def get_unpublished_events(self) -> List[OutboxEntry]:
        """
        Get all unpublished events from the outbox
        """
        return [entry for entry in self.outbox_entries if not entry.published]
    
    async def cleanup_processed_events(self, retention_hours: int = 24):
        """
        Clean up processed events after a retention period
        """
        cutoff_time = datetime.now() - timedelta(hours=retention_hours)
        expired_entries = [
            entry for entry in self.published_entries 
            if entry.published_at and entry.published_at < cutoff_time
        ]
        
        for entry in expired_entries:
            self.published_entries.remove(entry)
        
        return len(expired_entries)


# Global instance
outbox = TransactionalOutbox()