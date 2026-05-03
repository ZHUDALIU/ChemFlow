"""Orchestration engine — coordinates multi-agent workflow execution.

Manages the lifecycle of computational chemistry pipelines, including
task scheduling, agent coordination, error recovery, and result aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional

from chemflow.models.calculation import CalculationTask, BatchConfig


class PipelineStatus(Enum):
    PENDING = auto()
    INITIALIZING = auto()
    RUNNING = auto()
    DEGRADED = auto()
    PAUSED = auto()
    COMPLETED = auto()
    FAILED = auto()
    ROLLING_BACK = auto()


@dataclass
class PipelineContext:
    """Shared context propagated through pipeline stages."""

    workflow_id: str
    status: PipelineStatus = PipelineStatus.PENDING
    config: Optional[BatchConfig] = None
    artifacts: Dict[str, str] = field(default_factory=dict)
    errors: List[str] = field(default_factory=list)
    stage_timings: Dict[str, float] = field(default_factory=dict)
    retry_counts: Dict[str, int] = field(default_factory=dict)

    def record_error(self, stage: str, message: str) -> None:
        self.errors.append(f"[{stage}] {message}")


class Orchestrator:
    """Central workflow orchestrator managing pipeline execution.

    Implements a directed acyclic graph (DAG) execution model where each
    task node represents a computational chemistry job with dependency
    resolution, concurrency control, and fault tolerance.
    """

    def __init__(self, max_parallel: int = 4):
        self.max_parallel = max_parallel
        self._pipelines: Dict[str, PipelineContext] = {}
        self._task_graph: Dict[str, List[str]] = {}

    def create_pipeline(self, config: BatchConfig) -> str:
        """Register a new batch pipeline and return its workflow ID."""
        import uuid
        workflow_id = f"pipe-{uuid.uuid4().hex[:12]}"
        ctx = PipelineContext(
            workflow_id=workflow_id,
            config=config,
            status=PipelineStatus.INITIALIZING,
        )
        self._pipelines[workflow_id] = ctx
        return workflow_id

    def resolve_dependencies(self, workflow_id: str) -> List[List[str]]:
        """Topological sort of tasks into executable layers."""
        from collections import deque

        ctx = self._pipelines.get(workflow_id)
        if not ctx or not ctx.config:
            return []

        in_degree: Dict[str, int] = {}
        adj: Dict[str, List[str]] = {}

        for task in ctx.config.tasks:
            tid = task.title or task.molecule_name
            in_degree.setdefault(tid, 0)
            adj.setdefault(tid, [])
            for dep in task.dependencies:
                adj.setdefault(dep, []).append(tid)
                in_degree[tid] = in_degree.get(tid, 0) + 1

        queue = deque(t for t, d in in_degree.items() if d == 0)
        layers: List[List[str]] = []

        while queue:
            layer = []
            for _ in range(len(queue)):
                node = queue.popleft()
                layer.append(node)
                for neighbor in adj.get(node, []):
                    in_degree[neighbor] -= 1
                    if in_degree[neighbor] == 0:
                        queue.append(neighbor)
            layers.append(layer)

        return layers

    def get_pipeline(self, workflow_id: str) -> Optional[PipelineContext]:
        return self._pipelines.get(workflow_id)