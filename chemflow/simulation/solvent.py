"""Solvent model configurations — implicit solvation for QM calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

SOLVENT_PROPERTIES: Dict[str, Dict] = {
    "water": {"epsilon": 78.36, "radius": 1.38},
    "ethanol": {"epsilon": 24.85, "radius": 2.18},
    "methanol": {"epsilon": 32.61, "radius": 1.93},
    "acetonitrile": {"epsilon": 35.69, "radius": 2.19},
    "dichloromethane": {"epsilon": 8.93, "radius": 2.27},
    "chloroform": {"epsilon": 4.71, "radius": 2.44},
    "toluene": {"epsilon": 2.38, "radius": 2.76},
    "thf": {"epsilon": 7.43, "radius": 2.58},
    "dmso": {"epsilon": 46.83, "radius": 2.46},
    "benzene": {"epsilon": 2.27, "radius": 2.68},
}


@dataclass
class SolventConfig:
    """Implicit solvent model parameters."""
    solvent: str = "water"
    model: str = "SMD"  # PCM, CPCM, SMD, IPCM
    radii: str = "bondi"
    cavity: bool = True
    nonelectrostatic: bool = True

    @property
    def dielectric(self) -> float:
        info = SOLVENT_PROPERTIES.get(self.solvent.lower(), {})
        return info.get("epsilon", 78.36)

    def build_scrf_keyword(self) -> str:
        parts = [f"scrf=({self.model},{self.solvent})"]
        return " ".join(parts)


class SolventDatabase:
    """Solvent property database with dielectric constants and radii."""

    @classmethod
    def list_solvents(cls) -> list:
        return sorted(SOLVENT_PROPERTIES.keys())

    @classmethod
    def get_properties(cls, solvent: str) -> Optional[dict]:
        return SOLVENT_PROPERTIES.get(solvent.lower())