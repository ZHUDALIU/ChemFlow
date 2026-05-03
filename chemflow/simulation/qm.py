"""Quantum mechanics parameters — ab initio and DFT method configurations."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class QMParams:
    """Quantum mechanics calculation parameters.

    Encapsulates all tunable parameters for QM calculations
    including convergence thresholds, integration grids, and
    SCF control parameters.
    """
    method: str = "B3LYP"
    basis_set: str = "6-31+G(d,p)"
    scf_algorithm: str = "DIIS"
    scf_max_cycles: int = 128
    convergence_tight: bool = False
    integral_grid: str = "UltraFine"
    dispersion_correction: Optional[str] = "GD3BJ"

    def to_route_keywords(self) -> List[str]:
        kw = [f"{self.method}/{self.basis_set}"]
        if self.convergence_tight:
            kw.append("scf=tight")
        if self.dispersion_correction:
            kw.append(f"empiricaldispersion={self.dispersion_correction}")
        return kw


@dataclass
class FunctionalParams:
    """DFT functional-specific parameters."""
    functional: str = "B3LYP"
    exact_exchange: float = 0.20
    correlation_part: str = "LYP"
    range_separated: bool = False
    omega: Optional[float] = None


@dataclass
class BasisSetParams:
    """Basis set configuration with optional augmentation."""
    basis: str = "6-31G(d)"
    polarization: bool = True
    diffuse: bool = False
    ecp: Optional[str] = None  # Effective core potential


class DFTEngine:
    """DFT calculation parameter engine — method/basis selection and validation."""

    FUNCTIONAL_MAP = {
        "b3lyp": "B3LYP",
        "m062x": "M06-2X",
        "wb97xd": "wB97XD",
        "pbe0": "PBE0",
        "pbe1pbe": "PBE1PBE",
        "b3pw91": "B3PW91",
    }

    BASIS_MAP = {
        "sto-3g": "STO-3G", "3-21g": "3-21G", "6-31g(d)": "6-31G(d)",
        "6-31g(d,p)": "6-31G(d,p)", "6-31+g(d)": "6-31+G(d)",
        "6-31+g(d,p)": "6-31+G(d,p)", "def2svp": "def2SVP",
        "def2tzvp": "def2TZVP", "def2qzvp": "def2QZVP",
    }

    def resolve(self, method: str, basis: str) -> tuple:
        return (
            self.FUNCTIONAL_MAP.get(method.lower(), method),
            self.BASIS_MAP.get(basis.lower(), basis),
        )