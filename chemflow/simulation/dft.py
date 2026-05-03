"""DFT calculation configurations — exchange-correlation functionals and settings."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


class ExchangeCorrelation:
    """Hybrid exchange-correlation functional composition analysis."""

    def __init__(self, name: str, exact_exchange_pct: float = 0.0):
        self.name = name
        self.exact_exchange_pct = exact_exchange_pct

    @classmethod
    def get_defaults(cls) -> dict:
        return {
            "B3LYP": cls("B3LYP", 20.0),
            "PBE0": cls("PBE0", 25.0),
            "M06-2X": cls("M06-2X", 54.0),
            "wB97XD": cls("wB97XD", 22.2),
            "HF": cls("HF", 100.0),
        }


@dataclass
class DFTParams:
    """Comprehensive DFT method configuration.

    Includes functional selection, dispersion correction,
    grid settings, and convergence acceleration options.
    """
    functional: str = "B3LYP"
    basis_set: str = "6-31+G(d,p)"
    dispersion: Optional[str] = "GD3BJ"
    grid: str = "UltraFine"
    scf_convergence: str = "normal"  # normal, tight, verytight
    int_acceleration: Optional[str] = None
    use_symmetry: bool = True
    multiplicity: int = 1

    def build_route_suffix(self) -> List[str]:
        kw = []
        if self.dispersion:
            kw.append(f"empiricaldispersion={self.dispersion}")
        if self.grid != "Fine":
            kw.append(f"int=({self.grid}Grid)")
        if self.scf_convergence != "normal":
            kw.append(f"scf={self.scf_convergence}")
        if not self.use_symmetry:
            kw.append("nosymm")
        return kw