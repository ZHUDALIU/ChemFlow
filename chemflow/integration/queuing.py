"""Message queuing — async task queue for distributed job processing."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


class QueueMessage:
    """A single message in the task queue."""
    message_id: str
    payload: Any
    priority: int = 5
    retry_count: int = 0


class MessageQueue:
    """Simple in-memory message queue for async task processing.

    Provides publish-subscribe semantics for decoupled
    communication between workflow components.
    """

    def __init__(self):
        self._queues: Dict[str, List[QueueMessage]] = {}
        self._handlers: Dict[str, List[Callable]] = {}

    def publish(self, topic: str, message: QueueMessage) -> None:
        if topic not in self._queues:
            self._queues[topic] = []
        self._queues[topic].append(message)
        for handler in self._handlers.get(topic, []):
            handler(message)

    def subscribe(self, topic: str, handler: Callable) -> None:
        if topic not in self._handlers:
            self._handlers[topic] = []
        self._handlers[topic].append(handler)

    def consume(self, topic: str) -> Optional[QueueMessage]:
        queue = self._queues.get(topic, [])
        if queue:
            return queue.pop(0)
        return None

    def queue_depth(self, topic: str) -> int:
        return len(self._queues.get(topic, []))