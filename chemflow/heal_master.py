"""HealMaster — Gaussian calculation error diagnosis and input healing."""

from enum import Enum
from typing import Callable, Dict


class Status(Enum):
    """Computational job status indicators for Gaussian calculations."""

    RUNNING = "running"
    CONVERGED = "converged"
    SCF_FAILED = "scf_failed"
    OSCILLATING = "oscillating"
    IMAG_FREQ = "imag_freq"


class HealMaster:
    """Diagnoses Gaussian calculation errors and produces healed input files.

    Uses keyword-based pattern matching on output logs to identify common
    failure modes, then modifies the input file route section accordingly.

    Example::

        healer = HealMaster()
        status = healer.diagnose(log_text)
        healed = healer.heal(original_gjf, status)
        print(healed)
    """

    def __init__(self) -> None:
        self._patches: Dict[Status, Callable[[str], str]] = {
            Status.SCF_FAILED: self._patch_scf_failed,
            Status.OSCILLATING: self._patch_oscillating,
        }

    def diagnose(self, log_text: str) -> Status:
        """Analyze a Gaussian output log and determine calculation status.

        Uses simple substring matching against known error/failure markers.

        Args:
            log_text: The content of a Gaussian output/log file as a string.

        Returns:
            A Status enum value indicating the calculation state.
        """
        if "Convergence failure" in log_text:
            return Status.SCF_FAILED
        if "Oscillating" in log_text or "oscillating" in log_text:
            return Status.OSCILLATING
        if "imaginary frequency" in log_text or "imaginary frequencies" in log_text:
            return Status.IMAG_FREQ
        if "Normal termination" in log_text or "Have a nice day" in log_text:
            return Status.CONVERGED
        return Status.RUNNING

    @staticmethod
    def _patch_scf_failed(route: str) -> str:
        """Add SCF convergence aids for SCF failure."""
        if "scf=xqc" not in route:
            route += " scf=xqc"
        if "int=ultrafine" not in route:
            route += " int=ultrafine"
        return route

    @staticmethod
    def _patch_oscillating(route: str) -> str:
        """Add damping via quadratically-convergent SCF for oscillation."""
        if "scf=qc" not in route:
            route += " scf=qc"
        return route

    def heal(self, original_input: str, status: Status) -> str:
        """Generate a modified input file to fix a failed calculation.

        Modifies the route line of the .gjf input to add convergence
        aids appropriate to the diagnosed failure mode.

        Args:
            original_input: The original .gjf input file content.
            status: The diagnosed Status of the previous calculation.

        Returns:
            A modified .gjf input string with route-level fixes applied.

        Raises:
            ValueError: If the status is IMAG_FREQ (requires geometry
                adjustment, not a simple route patch).
        """
        if status in (Status.CONVERGED, Status.RUNNING):
            return original_input

        if status == Status.IMAG_FREQ:
            raise ValueError(
                "Imaginary frequencies detected. Consider adjusting "
                "the initial geometry or using a different method."
            )

        patcher = self._patches.get(status)
        if patcher is None:
            return original_input

        lines = original_input.split("\n")
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("#") and not stripped.startswith("#!"):
                route_part = stripped.lstrip("#")
                leading_ws = route_part[: len(route_part) - len(route_part.lstrip())]
                route = route_part.strip()
                new_route = patcher(route)
                indent = line[: len(line) - len(line.lstrip())]
                lines[i] = f"{indent}#{leading_ws}{new_route}"
                break

        return "\n".join(lines)