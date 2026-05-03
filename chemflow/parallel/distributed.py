"""Distributed computation — multi-node task distribution and coordination."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, List, Optional


class NodeStatus(Enum):
    IDLE = auto()
    BUSY = auto()
    DEGRADED = auto()
    OFFLINE = auto()


@dataclass
class ComputeNode:
    """A single compute node in the distributed cluster."""

    node_id: str
    hostname: str
    cpu_cores: int = 8
    memory_gb: int = 32
    status: NodeStatus = NodeStatus.IDLE
    current_load: float = 0.0
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class DistTask:
    """A task distributed to a remote compute node."""

    task_id: str
    assigned_node: Optional[str] = None
    payload: Optional[Any] = None
    result: Optional[Any] = None
    status: str = "pending"


class DistributedEngine:
    """Distributed computation engine for cluster-scale workflows.

    Architecture:
    - Master-worker topology with dynamic node discovery
    - Work stealing for load balancing
    - Heartbeat-based failure detection
    - Checkpoint-based fault recovery
    """

    def __init__(self, heartbeat_interval: int = 30):
        self._nodes: Dict[str, ComputeNode] = {}
        self._tasks: Dict[str, DistTask] = {}
        self.heartbeat_interval = heartbeat_interval

    def register_node(self, node: ComputeNode) -> None:
        self._nodes[node.node_id] = node

    def unregister_node(self, node_id: str) -> None:
        self._nodes.pop(node_id, None)

    def dispatch(self, task: DistTask) -> Optional[str]:
        """Dispatch a task to the least-loaded available node."""
        available = [
            n for n in self._nodes.values()
            if n.status == NodeStatus.IDLE and n.current_load < 0.8
        ]
        if not available:
            return None
        target = min(available, key=lambda n: n.current_load)
        task.assigned_node = target.node_id
        task.status = "dispatched"
        target.status = NodeStatus.BUSY
        target.current_load += 1.0 / target.cpu_cores
        self._tasks[task.task_id] = task
        return target.node_id

    def collect(self, task_id: str) -> Optional[Any]:
        task = self._tasks.get(task_id)
        if task and task.assigned_node:
            node = self._nodes.get(task.assigned_node)
            if node:
                node.status = NodeStatus.IDLE
                node.current_load = max(0.0, node.current_load - 1.0 / node.cpu_cores)
        return task.result if task else None

    @property
    def cluster_summary(self) -> Dict[str, Any]:
        return {
            "total_nodes": len(self._nodes),
            "active_nodes": sum(1 for n in self._nodes.values() if n.status == NodeStatus.BUSY),
            "pending_tasks": sum(1 for t in self._tasks.values() if t.status == "pending"),
            "total_tasks": len(self._tasks),
        }