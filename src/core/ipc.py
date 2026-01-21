#!/usr/bin/env python3
"""
SAGCO OS Event Bus - IPC/Message Passing System
Enables inter-process communication and event-driven architecture
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Set
from datetime import datetime
from enum import Enum, auto
import queue
import threading
from collections import defaultdict


class EventPriority(Enum):
    """Event priority levels"""
    LOW = 1
    NORMAL = 2
    HIGH = 3
    CRITICAL = 4


@dataclass
class Event:
    """System event"""
    event_type: str
    data: Any
    source: str
    priority: EventPriority = EventPriority.NORMAL
    timestamp: datetime = field(default_factory=datetime.now)
    event_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __lt__(self, other: 'Event') -> bool:
        """For priority queue ordering"""
        if self.priority.value != other.priority.value:
            return self.priority.value > other.priority.value  # Higher priority first
        return self.timestamp < other.timestamp


EventHandler = Callable[[Event], None]


class EventBus:
    """
    Central event bus for SAGCO OS
    Implements publish-subscribe pattern for IPC
    """
    
    def __init__(self):
        self.subscribers: Dict[str, List[EventHandler]] = defaultdict(list)
        self.event_queue: queue.PriorityQueue = queue.PriorityQueue()
        self.running = False
        self.worker_thread: Optional[threading.Thread] = None
        self.event_history: List[Event] = []
        self.max_history = 1000
        self.lock = threading.RLock()
        self.stats = {
            "published": 0,
            "processed": 0,
            "errors": 0
        }
    
    def subscribe(self, event_type: str, handler: EventHandler) -> None:
        """Subscribe to event type"""
        with self.lock:
            if handler not in self.subscribers[event_type]:
                self.subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: EventHandler) -> None:
        """Unsubscribe from event type"""
        with self.lock:
            if handler in self.subscribers[event_type]:
                self.subscribers[event_type].remove(handler)
    
    def publish(
        self,
        event_type: str,
        data: Any,
        source: str = "system",
        priority: EventPriority = EventPriority.NORMAL,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Event:
        """Publish event to bus"""
        event = Event(
            event_type=event_type,
            data=data,
            source=source,
            priority=priority,
            event_id=f"evt-{datetime.now().timestamp()}",
            metadata=metadata or {}
        )
        
        with self.lock:
            self.event_queue.put(event)
            self.stats["published"] += 1
        
        return event
    
    def _process_event(self, event: Event) -> None:
        """Process single event"""
        from src.core.logger import get_logger
        logger = get_logger("event_bus")
        
        with self.lock:
            handlers = self.subscribers.get(event.event_type, []).copy()
            # Also notify wildcard subscribers
            handlers.extend(self.subscribers.get("*", []))
        
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                self.stats["errors"] += 1
                logger.error(f"Handler failed for {event.event_type}", 
                           exception=e, event_id=event.event_id)
        
        with self.lock:
            self.stats["processed"] += 1
            self.event_history.append(event)
            if len(self.event_history) > self.max_history:
                self.event_history.pop(0)
    
    def _worker_loop(self) -> None:
        """Background worker for processing events"""
        from src.core.logger import get_logger
        logger = get_logger("event_bus.worker")
        
        while self.running:
            try:
                event = self.event_queue.get(timeout=0.1)
                self._process_event(event)
                self.event_queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logger.error("Worker loop error", exception=e)
    
    def start(self) -> None:
        """Start event bus worker"""
        if self.running:
            return
        
        self.running = True
        self.worker_thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.worker_thread.start()
    
    def stop(self) -> None:
        """Stop event bus worker"""
        self.running = False
        if self.worker_thread:
            self.worker_thread.join(timeout=1.0)
    
    def wait_for_events(self, timeout: Optional[float] = None) -> None:
        """Wait for all queued events to be processed"""
        self.event_queue.join()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get event bus statistics"""
        with self.lock:
            return {
                "stats": self.stats.copy(),
                "queue_size": self.event_queue.qsize(),
                "subscriber_count": sum(len(handlers) for handlers in self.subscribers.values()),
                "event_types": list(self.subscribers.keys()),
                "running": self.running
            }
    
    def get_recent_events(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent event history"""
        with self.lock:
            events = self.event_history[-limit:]
            return [
                {
                    "event_type": e.event_type,
                    "source": e.source,
                    "priority": e.priority.name,
                    "timestamp": e.timestamp.isoformat(),
                    "event_id": e.event_id
                }
                for e in events
            ]


# Message Queue for async task processing
class MessageQueue:
    """Simple message queue for task distribution"""
    
    def __init__(self, name: str = "default"):
        self.name = name
        self.queue: queue.Queue = queue.Queue()
        self.processed = 0
        self.failed = 0
    
    def enqueue(self, message: Any) -> None:
        """Add message to queue"""
        self.queue.put(message)
    
    def dequeue(self, timeout: Optional[float] = None) -> Any:
        """Get message from queue"""
        try:
            return self.queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def size(self) -> int:
        """Get queue size"""
        return self.queue.qsize()
    
    def mark_processed(self) -> None:
        """Mark message as processed"""
        self.processed += 1
        self.queue.task_done()
    
    def mark_failed(self) -> None:
        """Mark message as failed"""
        self.failed += 1
        self.queue.task_done()


class IPCManager:
    """Inter-Process Communication manager"""
    
    def __init__(self):
        self.event_bus = EventBus()
        self.queues: Dict[str, MessageQueue] = {}
        self.channels: Dict[str, Set[str]] = defaultdict(set)  # channel -> subscribers
    
    def start(self) -> None:
        """Start IPC system"""
        self.event_bus.start()
    
    def stop(self) -> None:
        """Stop IPC system"""
        self.event_bus.stop()
    
    def create_queue(self, name: str) -> MessageQueue:
        """Create named message queue"""
        if name not in self.queues:
            self.queues[name] = MessageQueue(name)
        return self.queues[name]
    
    def get_queue(self, name: str) -> Optional[MessageQueue]:
        """Get existing queue"""
        return self.queues.get(name)
    
    def join_channel(self, channel: str, subscriber_id: str) -> None:
        """Join communication channel"""
        self.channels[channel].add(subscriber_id)
    
    def leave_channel(self, channel: str, subscriber_id: str) -> None:
        """Leave communication channel"""
        if subscriber_id in self.channels[channel]:
            self.channels[channel].remove(subscriber_id)
    
    def broadcast_to_channel(
        self,
        channel: str,
        message: Any,
        source: str = "system"
    ) -> None:
        """Broadcast message to all channel subscribers"""
        self.event_bus.publish(
            event_type=f"channel.{channel}",
            data=message,
            source=source
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Get IPC system status"""
        return {
            "event_bus": self.event_bus.get_stats(),
            "queues": {
                name: {
                    "size": q.size(),
                    "processed": q.processed,
                    "failed": q.failed
                }
                for name, q in self.queues.items()
            },
            "channels": {
                name: list(subscribers)
                for name, subscribers in self.channels.items()
            }
        }


def get_event_bus() -> EventBus:
    """Get singleton event bus instance"""
    if not hasattr(get_event_bus, '_instance'):
        get_event_bus._instance = EventBus()
        get_event_bus._instance.start()
    return get_event_bus._instance


def get_ipc_manager() -> IPCManager:
    """Get singleton IPC manager instance"""
    if not hasattr(get_ipc_manager, '_instance'):
        get_ipc_manager._instance = IPCManager()
        get_ipc_manager._instance.start()
    return get_ipc_manager._instance
