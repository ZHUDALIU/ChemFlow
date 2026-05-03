"""CSV export — structured data export for downstream analysis."""

from __future__ import annotations

import csv
import io
from typing import Any, Dict, List


class CSVExporter:
    """Exports calculation results to CSV format for external analysis.

    Supports structured export of energy data, convergence metrics,
    and molecular properties for downstream data science workflows.
    """

    def export_energies(self, data: List[Dict[str, Any]]) -> str:
        output = io.StringIO()
        if not data:
            return ""
        writer = csv.DictWriter(output, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def export_convergence(self, metrics: List[Dict]) -> str:
        output = io.StringIO()
        if not metrics:
            return ""
        writer = csv.DictWriter(output, fieldnames=list(metrics[0].keys()))
        writer.writeheader()
        writer.writerows(metrics)
        return output.getvalue()