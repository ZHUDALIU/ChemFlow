"""InputMaster — Gaussian input file generation via Builder pattern."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class GaussianInput:
    """Represents a complete Gaussian input file configuration.

    Attributes:
        route: Route section content (e.g., "Opt B3LYP/6-31G(d)").
        charge: Molecular charge.
        multiplicity: Spin multiplicity.
        coordinates: Atomic coordinate block.
        molecule: Molecule name.
        method: Computational method.
        basis: Basis set.
        task: Job type (Opt, Freq, SP, etc.).
    """

    route: str
    charge: int
    multiplicity: int
    coordinates: str
    molecule: str = ""
    method: str = ""
    basis: str = ""
    task: str = ""

    def build_gjf(self) -> str:
        """Build and return the complete .gjf file content as a string."""
        return "\n".join([
            f"%chk={self.molecule.lower()}.chk",
            f"# {self.route}",
            "",
            f"Title: {self.molecule} {self.task} at {self.method}/{self.basis}",
            "",
            f"{self.charge} {self.multiplicity}",
            self.coordinates.strip(),
            "",
        ])


# Built-in molecular coordinate library (Cartesian, Angstrom)
MOLECULES: Dict[str, List[str]] = {
    "water": [
        "O    0.000000    0.000000    0.117000",
        "H    0.000000    0.757000   -0.468000",
        "H    0.000000   -0.757000   -0.468000",
    ],
    "methane": [
        "C    0.000000    0.000000    0.000000",
        "H    1.087000    0.000000    0.000000",
        "H   -0.362333    1.025000    0.000000",
        "H   -0.362333   -0.512500    0.887700",
        "H   -0.362333   -0.512500   -0.887700",
    ],
    "benzene": [
        "C    0.000000    1.396000    0.000000",
        "C    1.209000    0.698000    0.000000",
        "C    1.209000   -0.698000    0.000000",
        "C    0.000000   -1.396000    0.000000",
        "C   -1.209000   -0.698000    0.000000",
        "C   -1.209000    0.698000    0.000000",
        "H    0.000000    2.484000    0.000000",
        "H    2.149000    1.242000    0.000000",
        "H    2.149000   -1.242000    0.000000",
        "H    0.000000   -2.484000    0.000000",
        "H   -2.149000   -1.242000    0.000000",
        "H   -2.149000    1.242000    0.000000",
    ],
    "aspirin": [
        "C    0.000000    0.000000    0.000000",
        "C    1.400000    0.000000    0.000000",
        "C    2.100000    1.200000    0.000000",
        "C    1.400000    2.400000    0.000000",
        "C    0.000000    2.400000    0.000000",
        "C   -0.700000    1.200000    0.000000",
        "C    2.100000   -1.300000    0.000000",
        "O    1.600000   -2.400000    0.000000",
        "O    3.420000   -1.150000    0.000000",
        "C    3.500000   -1.700000    0.000000",
        "C    4.200000   -2.350000    0.000000",
        "O    1.200000    3.600000    0.000000",
        "O   -1.920000    1.200000    0.000000",
        "H   -0.520000   -0.950000    0.000000",
        "H    3.180000    1.200000    0.000000",
        "H    5.240000   -2.050000    0.000000",
        "H    4.080000   -2.950000    0.900000",
        "H    3.900000   -2.900000   -0.880000",
        "H   -2.350000    0.340000    0.000000",
        "H    2.400000    0.400000    0.000000",
        "H    1.820000   -2.900000    0.000000",
    ],
    "ethanol": [
        "C    0.000000    0.000000    0.000000",
        "C    0.000000    0.000000    1.520000",
        "O    1.300000    0.000000    2.080000",
        "H   -0.540000    0.890000   -0.420000",
        "H   -0.540000   -0.890000   -0.420000",
        "H    1.040000    0.000000   -0.420000",
        "H   -0.540000    0.890000    1.940000",
        "H   -0.540000   -0.890000    1.940000",
        "H    1.820000    0.720000    1.700000",
    ],
}


class InputMaster:
    """Builder for Gaussian input files (.gjf).

    Uses a Builder pattern to construct valid Gaussian input files with
    proper route sections, charge/multiplicity, and Cartesian coordinates.

    Example::

        master = InputMaster()
        gjf = master.generate("water", "B3LYP", "6-31G(d)", "Opt")
        print(gjf)
    """

    def __init__(self) -> None:
        self._molecules = {k: list(v) for k, v in MOLECULES.items()}

    def generate(self, molecule: str, method: str, basis: str, task: str) -> str:
        """Generate a complete Gaussian input file (.gjf) content.

        Args:
            molecule: Name of the molecule (e.g., 'water', 'aspirin').
            method: Computational method (e.g., 'B3LYP', 'HF').
            basis: Basis set (e.g., '6-31+G(d,p)', 'STO-3G').
            task: Job type (e.g., 'Opt', 'Freq', 'SP').

        Returns:
            A string containing the full .gjf input file content.

        Raises:
            ValueError: If the molecule name is not recognized.
        """
        key = molecule.lower()
        if key not in self._molecules:
            raise ValueError(
                f"Unknown molecule '{molecule}'. "
                f"Available: {list(self._molecules.keys())}"
            )

        route = f"{task} {method}/{basis}" if task else f"{method}/{basis}"
        coords = "\n".join(self._molecules[key])

        gjf = GaussianInput(
            route=route,
            charge=0,
            multiplicity=1,
            coordinates=coords,
            molecule=molecule,
            method=method,
            basis=basis,
            task=task,
        )
        return gjf.build_gjf()