"""Basis set knowledge base — reference data for Gaussian basis sets."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class BasisSetInfo:
    """Metadata for a Gaussian basis set."""
    name: str
    family: str  # Pople, Dunning, Ahlrichs
    polarization: bool = False
    diffuse: bool = False
    ecp: bool = False
    min_ang_mom: str = "S"
    max_ang_mom: str = "D"
    recommended_methods: List[str] = None


class BasisSetDatabase:
    """Curated database of Gaussian basis sets with compatibility info."""

    ENTRIES = {
        "STO-3G": BasisSetInfo("STO-3G", "Pople", False, False, min_ang_mom="S", max_ang_mom="P"),
        "3-21G": BasisSetInfo("3-21G", "Pople", False, False, min_ang_mom="S", max_ang_mom="P"),
        "6-31G(d)": BasisSetInfo("6-31G(d)", "Pople", True, False, min_ang_mom="S", max_ang_mom="D"),
        "6-31+G(d,p)": BasisSetInfo("6-31+G(d,p)", "Pople", True, True, min_ang_mom="S", max_ang_mom="P"),
        "def2SVP": BasisSetInfo("def2SVP", "Ahlrichs", True, False),
        "def2TZVP": BasisSetInfo("def2TZVP", "Ahlrichs", True, False),
        "aug-cc-pVDZ": BasisSetInfo("aug-cc-pVDZ", "Dunning", True, True),
        "aug-cc-pVTZ": BasisSetInfo("aug-cc-pVTZ", "Dunning", True, True),
    }

    def lookup(self, name: str) -> Optional[BasisSetInfo]:
        return self.ENTRIES.get(name)

    def recommend_for_method(self, method: str) -> List[str]:
        if method in ("HF", "B3LYP", "PBE0", "M06-2X"):
            return ["6-31G(d)", "6-31+G(d,p)", "def2SVP", "def2TZVP"]
        elif method in ("MP2", "CCSD", "CCSD(T)"):
            return ["aug-cc-pVDZ", "aug-cc-pVTZ"]
        return ["6-31G(d)"]