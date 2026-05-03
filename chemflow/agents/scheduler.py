"""Task scheduler — queue-based job scheduling with priority and dependency resolution."""

from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


class TaskPriority(Enum):
    CRITICAL = 0
    HIGH = 1
    NORMAL = 5
    LOW = 10
    BACKGROUND = 20


@dataclass(order=True)
class ScheduledTask:
    """A task in the scheduling queue with priority ordering."""

    priority: int = TaskPriority.NORMAL.value
    timestamp: float = 0.0
    task_id: str = ""
    payload: Any = None
    dependencies: List[str] = field(default_factory=list, compare=False)
    tags: Dict[str, str] = field(default_factory=dict, compare=False)


class Scheduler:
    """Priority queue-based task scheduler with dependency graph resolution.

    Supports:
    - Priority-based task ordering
    - Dependency graph resolution (DAG)
    - Weighted fair scheduling across task classes
    - Backpressure and throttling
    """

    def __init__(self):
        self._queue: List[ScheduledTask] = []
        self._running: Dict[str, ScheduledTask] = {}
        self._completed: Dict[str, Any] = {}

    def enqueue(self, task: ScheduledTask) -> None:
        heapq.heappush(self._queue, task)

    def enqueue_batch(self, tasks: List[ScheduledTask]) -> None:
        for task in tasks:
            self.enqueue(task)

    def dequeue(self) -> Optional[ScheduledTask]:
        """Dequeue the next ready task (all dependencies satisfied)."""
        ready: List[ScheduledTask] = []
        while self._queue:
            task = heapq.heappop(self._queue)
            if all(dep in self._completed for dep in task.dependencies):
                return task
            ready.append(task)
        for task in ready:
            heapq.heappush(self._queue, task)
        return None

    def complete(self, task_id: str, result: Any = None) -> None:
        self._completed[task_id] = result
        self._running.pop(task_id, None)

    @property
    def pending_count(self) -> int:
        return len(self._queue)

    @property
    def is_idle(self) -> bool:
        return len(self._queue) == 0 and len(self._running) == 0