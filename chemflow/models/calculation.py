"""Calculation task models — representing computational chemistry jobs."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional


class CalculationType(Enum):
    SP = "SP"
    OPT = "Opt"
    FREQ = "Freq"
    OPT_FREQ = "Opt+Freq"
    TS = "Opt=(TS,Calcfc,NoEigenTest)"
    IRC = "IRC"
    NMR = "NMR"
    POLAR = "Polar"
    RAMAN = "Raman"
    VCD = "VCD"
    ECD = "ECD"
    SCAN = "Scan"
    STABILITY = "Stability"


class TheoryLevel(Enum):
    HF = "HF"
    DFT = "DFT"
    MP2 = "MP2"
    CCSD = "CCSD"
    CCSD_T = "CCSD(T)"
    CASSCF = "CASSCF"
    CASPT2 = "CASPT2"
    MRCI = "MRCI"
    CIS = "CIS"
    TDDFT = "TD-DFT"


class SolventModel(Enum):
    PCM = "PCM"
    SMD = "SMD"
    CPCM = "CPCM"
    IPCM = "IPCM"
    ONIOM = "ONIOM"


@dataclass
class SolventConfig:
    model: SolventModel = SolventModel.SMD
    solvent: str = "water"
    radii: str = "bondi"
    cavity: bool = True


@dataclass
class RouteConfig:
    method: str = "B3LYP"
    basis_set: str = "6-31+G(d,p)"
    calc_type: CalculationType = CalculationType.OPT
    solvent: Optional[SolventConfig] = None
    dispersion: Optional[str] = None
    empirical_dispersion: str = "GD3BJ"
    memory_mb: int = 16000
    nproc: int = 8
    extra_keywords: List[str] = field(default_factory=list)

    def build_route_line(self) -> str:
        parts = [f"#p {self.method}/{self.basis_set}"]
        if self.calc_type:
            parts.append(self.calc_type.value)
        if self.solvent:
            parts.append(f"scrf=({self.solvent.model.value},{self.solvent.solvent})")
        if self.dispersion:
            parts.append(f"empiricaldispersion={self.dispersion}")
        parts.extend(self.extra_keywords)
        return " ".join(parts)


@dataclass
class CalculationTask:
    """A single computational chemistry job."""

    molecule_name: str
    route: RouteConfig
    chk_name: str = ""
    title: str = ""
    priority: int = 5
    tags: Dict[str, str] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)


@dataclass
class BatchConfig:
    """Configuration for a batch of calculations."""

    tasks: List[CalculationTask] = field(default_factory=list)
    max_concurrent: int = 4
    retry_limit: int = 3
    checkpoint_interval: int = 300
    output_dir: str = "./output"