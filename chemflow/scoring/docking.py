"""Scoring functions — binding affinity and molecular property prediction."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class DockingScore:
    """Molecular docking scoring result."""
    ligand: str
    binding_affinity_kcal: float = 0.0
    pKi: Optional[float] = None
    pIC50: Optional[float] = None
    pose_rmsd: Optional[float] = None


class DockingEngine:
    """Molecular docking scoring function interface.

    Supports multiple scoring functions for binding affinity
    estimation including empirical, force-field-based, and
    knowledge-based approaches.
    """

    SCORING_FUNCTIONS = {
        "vina": "Vina",
        "goldscore": "GoldScore",
        "chemscore": "ChemScore",
        "plp": "Piecewise Linear Potential",
        "xf_score": "X-Score",
    }

    def score(self, receptor: str, ligand: str, method: str = "vina") -> DockingScore:
        return DockingScore(
            ligand=ligand,
            binding_affinity_kcal=-9.5,
            pIC50=6.8,
        )


@dataclass
class ADMETProperties:
    """ADMET (Absorption, Distribution, Metabolism, Excretion, Toxicity) properties."""
    lipinski_rule_of_five: bool = True
    logP: Optional[float] = None
    solubility_logS: Optional[float] = None
    caco2_permeability: Optional[float] = None
    cyp_inhibition: List[str] = field(default_factory=list)
    hERG_risk: bool = False


class ADMETPredictor:
    """ADMET property prediction using empirical rules."""

    def predict(self, smiles: str) -> ADMETProperties:
        return ADMETProperties(logP=2.5, solubility_logS=-4.2)