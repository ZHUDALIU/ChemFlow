"""Computational methods knowledge base — method recommendations and compatibility."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class MethodInfo:
    """Metadata for a computational chemistry method."""
    name: str
    family: str  # HF, DFT, MP, CC, MCSCF, SemiEmpirical
    description: str = ""
    scaling: str = ""  # e.g., O(N^4), O(N^5), O(N^7)
    recommended_for: List[str] = None


class MethodsDatabase:
    """Knowledge base of computational methods with recommendations."""

    ENTRIES = {
        "HF": MethodInfo("HF", "HF", "Hartree-Fock", "O(N^4)", ["large systems", "initial guess"]),
        "B3LYP": MethodInfo("B3LYP", "DFT", "Becke 3-parameter + LYP correlation", "O(N^3)",
                            ["general purpose", "thermochemistry", "geometry optimization"]),
        "M06-2X": MethodInfo("M06-2X", "DFT", "Minnesota 2006 double exchange", "O(N^3)",
                             ["main-group thermochemistry", "non-covalent interactions"]),
        "wB97XD": MethodInfo("wB97XD", "DFT", "Long-range corrected with dispersion", "O(N^3)",
                             ["dispersion-dominated systems", "charge transfer"]),
        "MP2": MethodInfo("MP2", "MP", "Møller-Plesset 2nd order", "O(N^5)",
                          ["correlation energy", "thermochemistry"]),
        "CCSD(T)": MethodInfo("CCSD(T)", "CC", "Coupled cluster with triples", "O(N^7)",
                              ["gold standard", "high-accuracy thermochemistry"]),
    }

    def lookup(self, name: str) -> Optional[MethodInfo]:
        return self.ENTRIES.get(name)

    def recommend(self, property_type: str) -> List[str]:
        recommendations = {
            "geometry": ["B3LYP", "PBE0", "M06-2X"],
            "energy": ["CCSD(T)", "MP2", "wB97XD"],
            "nmr": ["B3LYP", "PBE0"],
            "uvvis": ["TD-B3LYP", "TD-CAM-B3LYP"],
            "thermochemistry": ["B3LYP", "M06-2X", "G4"],
        }
        return recommendations.get(property_type, ["B3LYP"])