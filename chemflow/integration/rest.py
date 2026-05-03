"""REST API — HTTP interface for remote workflow management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class APIRequest:
    """Incoming API request."""
    method: str = "GET"
    path: str = "/"
    params: Dict[str, str] = field(default_factory=dict)
    body: Optional[Dict] = None


@dataclass
class APIResponse:
    """Outgoing API response."""
    status_code: int = 200
    body: Dict = field(default_factory=dict)
    headers: Dict[str, str] = field(default_factory=dict)


class RESTAPI:
    """RESTful API server for remote pipeline management.

    Endpoints:
    - POST /pipeline — submit a new pipeline
    - GET /pipeline/{id} — get pipeline status
    - POST /generate — generate input file
    - POST /diagnose — diagnose log file
    - POST /heal — heal input file
    - GET /metrics — get usage metrics
    """

    def __init__(self):
        self._routes: Dict[str, Any] = {}

    def handle(self, request: APIRequest) -> APIResponse:
        handler = self._routes.get((request.method, request.path))
        if not handler:
            return APIResponse(404, {"error": "not found"})
        return handler(request)

    def route(self, method: str, path: str, handler: Any) -> None:
        self._routes[(method.upper(), path)] = handler