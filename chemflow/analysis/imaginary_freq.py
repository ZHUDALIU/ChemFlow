"""Imaginary frequency analysis — detection and remediation of transition states."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class VibrationalMode:
    """A single vibrational mode from frequency calculation."""

    mode_number: int
    frequency_cm1: float
    ir_intensity: Optional[float] = None
    symmetry: str = ""

    @property
    def is_imaginary(self) -> bool:
        return self.frequency_cm1 < 0

    @property
    def is_low_frequency(self) -> bool:
        return abs(self.frequency_cm1) < 100


@dataclass
class FrequencyReport:
    """Full frequency analysis report."""

    total_modes: int = 0
    imaginary_modes: List[VibrationalMode] = field(default_factory=list)
    low_frequency_modes: List[VibrationalMode] = field(default_factory=list)
    thermochemistry: dict = field(default_factory=dict)
    is_transition_state: bool = False
    has_negative_eigenvalues: bool = False


class ImaginaryFrequencyAnalyzer:
    """Analyzes vibrational frequency output for imaginary modes.

    Capabilities:
    - Identifies imaginary frequencies from frequency calculations
    - Classifies stationary points (minimum vs transition state)
    - Suggests geometry modifications for TS refinement
    """

    def analyze(self, frequencies: List[float]) -> FrequencyReport:
        """Analyze a list of frequencies (in cm^-1) for imaginary modes."""
        report = FrequencyReport()
        report.total_modes = len(frequencies)

        for i, freq in enumerate(frequencies):
            mode = VibrationalMode(mode_number=i + 1, frequency_cm1=freq)
            if mode.is_imaginary:
                report.imaginary_modes.append(mode)
            if mode.is_low_frequency:
                report.low_frequency_modes.append(mode)

        n_imag = len(report.imaginary_modes)
        report.has_negative_eigenvalues = n_imag > 0

        if n_imag == 0:
            pass  # minimum
        elif n_imag == 1:
            report.is_transition_state = True  # true TS
        else:
            report.is_transition_state = False  # higher-order saddle point

        return report

    def suggest_remediation(self, report: FrequencyReport) -> List[str]:
        """Suggest remediation strategies based on imaginary frequency analysis."""
        suggestions = []
        if report.is_transition_state:
            suggestions.append("Transition state confirmed — proceed with IRC calculation")
        if len(report.imaginary_modes) > 1:
            suggestions.append("Higher-order saddle point — symmetry constraints may be too high")
        if report.low_frequency_modes:
            suggestions.append("Low-frequency modes detected — consider tighter optimization")
        return suggestions