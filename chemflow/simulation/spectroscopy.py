"""Spectroscopy prediction — NMR, IR, Raman, UV-Vis, VCD, ECD."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class NMRPeak:
    """A single NMR chemical shift prediction."""
    atom_index: int
    isotope: str = "13C"
    chemical_shift_ppm: float = 0.0
    multiplicity: str = "s"


@dataclass
class IRBand:
    """IR absorption band."""
    frequency_cm1: float
    intensity: float
    mode: int = 0


@dataclass
class Spectrum:
    """Generic spectrum container."""
    type: str = ""  # NMR, IR, Raman, UV-Vis
    data: Dict = field(default_factory=dict)
    metadata: Dict[str, str] = field(default_factory=dict)


class NMREngine:
    """NMR chemical shift prediction via GIAO method configuration."""

    def configure(self, nucleus: str = "13C", method: str = "B3LYP") -> Dict:
        configs = {
            "13C": {"route": "#p B3LYP/6-311+G(2d,p) NMR GIAO", "reference": 184.2},
            "1H": {"route": "#p B3LYP/6-311+G(2d,p) NMR GIAO", "reference": 31.9},
            "15N": {"route": "#p B3LYP/6-311+G(2d,p) NMR GIAO", "reference": 243.7},
        }
        return configs.get(nucleus, configs["13C"])


class SpectroscopyEngine:
    """Spectroscopy calculation router — selects appropriate method."""

    ROUTE_TEMPLATES = {
        "nmr": "#p {method}/{basis} NMR GIAO",
        "ir": "#p {method}/{basis} Freq",
        "raman": "#p {method}/{basis} Freq=RAMAN",
        "vcd": "#p {method}/{basis} Freq VCD",
        "ecd": "#p {method}/{basis} TD=(NStates=20,Root=1)",
        "uvvis": "#p {method}/{basis} TD=(NStates=20,Singlets)",
    }

    def suggest_route(self, spec_type: str, method: str = "B3LYP",
                      basis: str = "6-31+G(d,p)") -> str:
        template = self.ROUTE_TEMPLATES.get(spec_type.lower())
        if not template:
            raise ValueError(f"Unsupported spectroscopy type: {spec_type}")
        return template.format(method=method, basis=basis)