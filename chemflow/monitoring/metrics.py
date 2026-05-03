"""Metrics collection — performance monitoring and usage tracking."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class MetricPoint:
    """A single metric data point with timestamp."""
    name: str
    value: float
    timestamp: float = 0.0
    tags: Dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """Collects and aggregates performance metrics.

    Tracks token consumption, API call latencies, error rates,
    and throughput for operational monitoring and cost analysis.
    """

    def __init__(self):
        self._metrics: List[MetricPoint] = []

    def record(self, name: str, value: float, tags: Optional[Dict[str, str]] = None) -> None:
        self._metrics.append(MetricPoint(
            name=name, value=value, timestamp=time.time(), tags=tags or {}
        ))

    def aggregate(self, name: str) -> Dict[str, float]:
        values = [m.value for m in self._metrics if m.name == name]
        if not values:
            return {"count": 0, "mean": 0.0, "sum": 0.0}
        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "sum": sum(values),
            "min": min(values),
            "max": max(values),
        }

    def token_summary(self) -> Dict[str, float]:
        return {
            "total_tokens": self.aggregate("token_usage")["sum"],
            "total_calls": self.aggregate("api_call")["count"],
        }

    def clear(self) -> None:
        self._metrics.clear()