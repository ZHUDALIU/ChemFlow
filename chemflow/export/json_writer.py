"""JSON export — structured data serialization in JSON format."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Any, Dict, List, Optional


class JSONExporter:
    """Exports calculation data to structured JSON format.

    Handles serialization of nested dataclass objects and
    provides schema-constrained output for API integration.
    """

    def export(self, data: Any, indent: int = 2) -> str:
        if hasattr(data, "__dataclass_fields__"):
            return json.dumps(asdict(data), indent=indent, ensure_ascii=False)
        return json.dumps(data, indent=indent, ensure_ascii=False)

    def export_batch(self, records: List[Dict], indent: int = 2) -> str:
        return json.dumps(records, indent=indent, ensure_ascii=False)