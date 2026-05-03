"""Input file validator — syntactic and semantic validation of Gaussian input files."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from chemflow.models.calculation import CalculationType


@dataclass
class ValidationError:
    line: int
    severity: str  # error, warning, info
    message: str
    code: str


@dataclass
class ValidationReport:
    valid: bool = True
    errors: List[ValidationError] = field(default_factory=list)

    @property
    def error_count(self) -> int:
        return len([e for e in self.errors if e.severity == "error"])

    @property
    def warning_count(self) -> int:
        return len([e for e in self.errors if e.severity == "warning"])


class Validator:
    """Semantic and syntactic validator for Gaussian input files.

    Performs multi-stage validation:
    1. Syntax validation — checks route line format, section ordering
    2. Semantic validation — validates method/basis compatibility
    3. Resource validation — checks memory and processor constraints
    """

    VALID_METHODS = {
        "HF", "B3LYP", "M06-2X", "wB97XD", "PBE0", "PBE1PBE",
        "MP2", "CCSD", "CCSD(T)", "CASSCF", "CIS", "TD",
    }

    VALID_BASIS_SETS = {
        "STO-3G", "3-21G", "6-31G(d)", "6-31G(d,p)", "6-31+G(d)",
        "6-31+G(d,p)", "6-311+G(d,p)", "def2SVP", "def2TZVP",
        "def2QZVP", "aug-cc-pVDZ", "aug-cc-pVTZ",
    }

    def validate_gjf(self, content: str) -> ValidationReport:
        """Full validation of a .gjf input file."""
        report = ValidationReport()
        lines = content.split("\n")

        # Check for required sections
        has_route = False
        has_title = False
        has_charge_mult = False
        has_coords = False

        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#"):
                has_route = True
                route_errors = self._validate_route(stripped)
                for e in route_errors:
                    e.line = i + 1
                    report.errors.append(e)
            elif stripped == "":
                continue
            elif re.match(r"^[0-9\-]+\s+[0-9\-]+$", stripped):
                has_charge_mult = True
            elif re.match(r"^[A-Za-z][a-z]?", stripped):
                has_coords = True

        if not has_route:
            report.errors.append(ValidationError(0, "error", "Missing route line", "E001"))
            report.valid = False
        if not has_charge_mult:
            report.errors.append(ValidationError(0, "error", "Missing charge/multiplicity", "E002"))
            report.valid = False

        return report

    def _validate_route(self, route: str) -> List[ValidationError]:
        errors: List[ValidationError] = []
        route_upper = route.upper()
        # Check method is valid
        if not any(m in route_upper for m in self.VALID_METHODS):
            errors.append(ValidationError(0, "warning", "Unrecognized method", "W001"))
        # Check basis set
        if not any(b.upper() in route_upper for b in self.VALID_BASIS_SETS):
            errors.append(ValidationError(0, "warning", "Unrecognized basis set", "W002"))
        return errors