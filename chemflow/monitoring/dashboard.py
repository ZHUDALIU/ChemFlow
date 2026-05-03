"""Dashboard — real-time visualization and monitoring dashboard."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class DashboardPanel:
    """A single dashboard panel widget."""
    title: str
    metric: str
    panel_type: str = "gauge"  # gauge, chart, table, log
    refresh_interval: int = 30


@dataclass
class DashboardConfig:
    """Full dashboard configuration."""
    panels: List[DashboardPanel] = field(default_factory=list)
    auto_refresh: bool = True
    theme: str = "dark"


class Dashboard:
    """Operational dashboard for pipeline monitoring.

    Provides real-time visibility into calculation progress,
    error rates, token consumption, and system health.
    """

    def __init__(self):
        self._panels: List[DashboardPanel] = []

    def add_panel(self, panel: DashboardPanel) -> None:
        self._panels.append(panel)

    def render_summary(self, metrics: Dict[str, Any]) -> str:
        lines = ["=" * 50, "ChemFlow Pipeline Dashboard", "=" * 50]
        for key, value in metrics.items():
            lines.append(f"  {key:30s}: {value}")
        return "\n".join(lines)