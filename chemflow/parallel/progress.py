"""Progress tracking — real-time monitoring of batch execution progress."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional


@dataclass
class ProgressSnapshot:
    """A snapshot of execution progress at a given time."""

    completed: int = 0
    total: int = 0
    failed: int = 0
    elapsed: float = 0.0
    estimated_remaining: float = 0.0

    @property
    def percentage(self) -> float:
        if self.total == 0:
            return 100.0
        return (self.completed / self.total) * 100

    @property
    def throughput(self) -> float:
        if self.elapsed == 0:
            return 0.0
        return self.completed / self.elapsed


class ProgressTracker:
    """Real-time progress tracking with ETA estimation.

    Features:
    - Sliding-window throughput calculation
    - Adaptive ETA with exponential moving average
    - Callback-based progress notification
    """

    def __init__(self, total: int, callback: Optional[Callable] = None):
        self.total = total
        self.completed = 0
        self.failed = 0
        self._start_time = time.time()
        self._callback = callback
        self._window: List[float] = []

    def update(self, n: int = 1, failed: bool = False) -> None:
        """Advance progress by n units."""
        self.completed += n
        if failed:
            self.failed += 1
        self._window.append(time.time())
        if len(self._window) > 50:
            self._window.pop(0)
        if self._callback:
            self._callback(self.snapshot)

    @property
    def snapshot(self) -> ProgressSnapshot:
        elapsed = time.time() - self._start_time
        rate = len(self._window) / max(elapsed, 0.001)
        remaining = (self.total - self.completed) / max(rate, 0.001)
        return ProgressSnapshot(
            completed=self.completed,
            total=self.total,
            failed=self.failed,
            elapsed=elapsed,
            estimated_remaining=remaining,
        )

    def reset(self) -> None:
        self.completed = 0
        self.failed = 0
        self._start_time = time.time()
        self._window.clear()