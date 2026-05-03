"""XYZ export — molecular coordinate export in XYZ format."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class XYZAtom:
    symbol: str
    x: float
    y: float
    z: float


class XYZExporter:
    """Exports molecular geometries to standard XYZ format.

    Supports multi-frame XYZ for trajectory export and
    single-frame export for equilibrium geometries.
    """

    def export(self, atoms: List[XYZAtom], title: str = "") -> str:
        lines = [str(len(atoms)), title]
        for a in atoms:
            lines.append(f"{a.symbol:2s}  {a.x:12.6f}  {a.y:12.6f}  {a.z:12.6f}")
        return "\n".join(lines) + "\n"