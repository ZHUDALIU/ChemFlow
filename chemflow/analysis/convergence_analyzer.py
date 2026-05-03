"""Convergence analysis — monitors SCF and geometry convergence trajectories."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class ConvergenceMetrics:
    """Convergence metrics for a single optimization step."""

    step: int
    rms_force: Optional[float] = None
    max_force: Optional[float] = None
    rms_displacement: Optional[float] = None
    max_displacement: Optional[float] = None
    energy_change: Optional[float] = None

    @property
    def is_converged(self) -> bool:
        thresholds = {"rms_force": 0.00045, "max_force": 0.00030}
        if self.rms_force is not None and self.rms_force > thresholds["rms_force"]:
            return False
        if self.max_force is not None and self.max_force > thresholds["max_force"]:
            return False
        return True


@dataclass
class ConvergenceReport:
    """Complete convergence analysis report."""

    scf_converged: bool = False
    geometry_converged: bool = False
    total_cycles: int = 0
    metrics: List[ConvergenceMetrics] = field(default_factory=list)
    oscillating: bool = False
    diagnosis: str = ""


class ConvergenceAnalyzer:
    """Analyzes SCF and geometry convergence from log data.

    Detection capabilities:
    - SCF oscillation detection via energy pattern analysis
    - Geometry convergence rate tracking
    - Early warning for divergence trends
    """

    OSCILLATION_THRESHOLD = 3

    def analyze_scf(self, energies: List[float]) -> ConvergenceReport:
        """Detect SCF convergence patterns and oscillation."""
        report = ConvergenceReport()
        report.total_cycles = len(energies)

        if len(energies) < 2:
            report.diagnosis = "Insufficient SCF cycles"
            return report

        # Check oscillation: alternating energy increases
        oscillation_count = 0
        for i in range(2, len(energies)):
            if (energies[i] > energies[i - 1] and energies[i - 1] < energies[i - 2]) or \
               (energies[i] < energies[i - 1] and energies[i - 1] > energies[i - 2]):
                oscillation_count += 1

        report.oscillating = oscillation_count >= self.OSCILLATION_THRESHOLD
        if report.oscillating:
            report.diagnosis = "SCF oscillation detected — consider damping or level shifting"
        else:
            report.scf_converged = True
            report.diagnosis = "SCF convergence normal"

        return report

    def analyze_geometry(self, metrics: List[ConvergenceMetrics]) -> ConvergenceReport:
        """Analyze geometry optimization convergence trajectory."""
        report = ConvergenceReport()
        report.metrics = metrics
        report.total_cycles = len(metrics)

        if not metrics:
            return report

        recent = metrics[-3:] if len(metrics) >= 3 else metrics
        report.geometry_converged = all(m.is_converged for m in recent)

        if not report.geometry_converged:
            rates = [abs(m.energy_change or 0) for m in recent if m.energy_change]
            if rates and len(rates) > 1 and rates[-1] > rates[0]:
                report.diagnosis = "Geometry divergence detected — check initial structure"
            else:
                report.diagnosis = "Geometry convergence in progress"
        else:
            report.diagnosis = "Geometry converged within thresholds"

        return report