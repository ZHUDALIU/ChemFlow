"""Gaussian log parser — extracts structured data from output files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple


@dataclass
class LogEntry:
    """A single parsed section from a Gaussian log file."""

    section: str
    content: str
    line_start: int
    line_end: int


@dataclass
class EnergyPoint:
    """Energy value extracted from a log file."""

    cycle: int
    energy_hartree: float
    energy_kjmol: float = 0.0
    convergence: Dict[str, float] = field(default_factory=dict)


@dataclass
class ParsedLog:
    """Fully parsed Gaussian output log with structured data."""

    method: str = ""
    basis: str = ""
    molecule_name: str = ""
    final_energy: Optional[float] = None
    energies: List[EnergyPoint] = field(default_factory=list)
    scf_cycles: int = 0
    optimization_cycles: int = 0
    has_converged: bool = False
    error_messages: List[str] = field(default_factory=list)
    sections: List[LogEntry] = field(default_factory=list)
    raw_text: str = ""


class LogParser:
    """Multi-stage parser for Gaussian 16 output logs.

    Extraction stages:
    1. Header parsing — method, basis, molecule name
    2. Energy extraction — SCF energies per cycle
    3. Convergence tracking — RMS force, max displacement
    4. Error detection — pattern recognition for known errors
    """

    PATTERN_ENERGY = re.compile(r"SCF Done:\s+E\([\w]+\)\s*=\s*([-\d.]+)")
    PATTERN_METHOD = re.compile(r"#p?\s+(\w+)/")
    PATTERN_BASIS = re.compile(r"/([\w+\-()]+)")
    PATTERN_CONVERGENCE = re.compile(r"Convergence\s+failure", re.IGNORECASE)
    PATTERN_NORMAL = re.compile(r"Normal\s+termination", re.IGNORECASE)

    def parse(self, log_text: str) -> ParsedLog:
        """Parse a complete Gaussian log file."""
        result = ParsedLog(raw_text=log_text)
        lines = log_text.split("\n")

        # Extract method/basis
        for line in lines[:50]:
            m = self.PATTERN_METHOD.search(line)
            if m:
                result.method = m.group(1)
            b = self.PATTERN_BASIS.search(line)
            if b:
                result.basis = b.group(1)

        # Extract energies
        for i, line in enumerate(lines):
            m = self.PATTERN_ENERGY.search(line)
            if m:
                result.scf_cycles += 1
                energy = float(m.group(1))
                result.energies.append(
                    EnergyPoint(cycle=result.scf_cycles, energy_hartree=energy)
                )

        # Check convergence
        text_upper = log_text.upper()
        if self.PATTERN_NORMAL.search(text_upper):
            result.has_converged = True
        if self.PATTERN_CONVERGENCE.search(text_upper):
            result.error_messages.append("SCF convergence failure")

        if result.energies:
            result.final_energy = result.energies[-1].energy_hartree

        return result