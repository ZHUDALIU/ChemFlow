"""Solvent database — comprehensive solvent property reference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class SolventRecord:
    """Complete solvent properties for implicit solvation."""
    name: str
    dielectric_constant: float
    refractive_index: float = 1.0
    surface_tension_dyncm: Optional[float] = None
    acidity: float = 0.0
    basicity: float = 0.0
    aromaticity: bool = False
    halogen: bool = False


class SolventDatabase:
    """Comprehensive solvent property database."""

    RECORDS: Dict[str, SolventRecord] = {
        "water": SolventRecord("Water", 78.36, 1.333, 71.99, 0.82, 0.35),
        "methanol": SolventRecord("Methanol", 32.61, 1.328, 22.12, 0.98, 0.66),
        "ethanol": SolventRecord("Ethanol", 24.85, 1.361, 21.97, 0.86, 0.75),
        "acetonitrile": SolventRecord("Acetonitrile", 35.69, 1.344, 28.66, 0.19, 0.40),
        "dichloromethane": SolventRecord("DCM", 8.93, 1.424, 27.20, 0.10, 0.05, halogen=True),
        "chloroform": SolventRecord("Chloroform", 4.71, 1.446, 26.67, 0.15, 0.02, halogen=True),
        "toluene": SolventRecord("Toluene", 2.38, 1.496, 27.92, 0.00, 0.11, aromaticity=True),
        "thf": SolventRecord("THF", 7.43, 1.405, 26.40, 0.00, 0.59),
        "dmso": SolventRecord("DMSO", 46.83, 1.479, 42.92, 0.00, 0.88),
        "benzene": SolventRecord("Benzene", 2.27, 1.501, 28.22, 0.00, 0.12, aromaticity=True),
    }

    def get(self, name: str) -> Optional[SolventRecord]:
        return self.RECORDS.get(name.lower())

    def list_solvents(self) -> List[str]:
        return list(self.RECORDS.keys())