"""Molecular dynamics parameters — classical MD simulation configurations."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class ForceField(Enum):
    AMBER = "AMBER"
    CHARMM = "CHARMM"
    OPLS = "OPLS-AA"
    GAFF = "GAFF"
    UFF = "UFF"


class Thermostat(Enum):
    NOSE_HOOVER = "nose-hoover"
    ANDERSEN = "andersen"
    LANGEVIN = "langevin"
    BERENDSEN = "berendsen"


@dataclass
class MDParams:
    """Molecular dynamics simulation parameters.

    Covers thermostats, barostats, integration time steps,
    and ensemble specification for NVT/NPT simulations.
    """
    force_field: ForceField = ForceField.GAFF
    ensemble: str = "NVT"  # NVE, NVT, NPT
    temperature_k: float = 298.15
    pressure_bar: Optional[float] = None
    time_step_fs: float = 1.0
    total_time_ns: float = 10.0
    thermostat: Thermostat = Thermostat.LANGEVIN
    cutoff_angstrom: float = 10.0
    shake_constraints: bool = True
    periodic_boundary: bool = True
    trajectory_interval: int = 1000

    @property
    def nsteps(self) -> int:
        return int(self.total_time_ns * 1000 / self.time_step_fs)