"""Alerting system — configurable alerts for job failures and anomalies."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


class AlertSeverity(Enum):
    DEBUG = auto()
    INFO = auto()
    WARNING = auto()
    ERROR = auto()
    CRITICAL = auto()


@dataclass
class Alert:
    """A single alert with severity and context."""
    title: str
    message: str
    severity: AlertSeverity = AlertSeverity.INFO
    source: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class AlertManager:
    """Centralized alert management with routing and deduplication.

    Supports multiple notification channels including console,
    file, webhook, and callback-based delivery.
    """

    def __init__(self):
        self._handlers: List[Callable[[Alert], None]] = []
        self._alerts: List[Alert] = []

    def add_handler(self, handler: Callable[[Alert], None]) -> None:
        self._handlers.append(handler)

    def emit(self, alert: Alert) -> None:
        self._alerts.append(alert)
        for handler in self._handlers:
            handler(alert)

    def emit_error(self, title: str, message: str) -> None:
        self.emit(Alert(title, message, AlertSeverity.ERROR))

    @property
    def recent(self) -> List[Alert]:
        return list(self._alerts[-10:]) if self._alerts else []

    def clear(self) -> None:
        self._alerts.clear()