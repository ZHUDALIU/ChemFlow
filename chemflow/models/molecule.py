"""Molecular data models — core domain abstractions for computational chemistry."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Dict, List, Optional, Tuple


class Element(Enum):
    H = "H"
    He = "He"
    Li = "Li"
    Be = "Be"
    B = "B"
    C = "C"
    N = "N"
    O = "O"
    F = "F"
    Ne = "Ne"
    Na = "Na"
    Mg = "Mg"
    Al = "Al"
    Si = "Si"
    P = "P"
    S = "S"
    Cl = "Cl"
    Ar = "Ar"
    K = "K"
    Ca = "Ca"
    Fe = "Fe"
    Cu = "Cu"
    Zn = "Zn"
    Br = "Br"
    I = "I"


@dataclass
class Atom:
    """A single atom with Cartesian or internal coordinates."""

    element: Element
    x: float = 0.0
    y: float = 0.0
    z: float = 0.0
    explicit_hydrogens: int = 0


@dataclass
class Bond:
    """Chemical bond between two atoms."""

    atom1_index: int
    atom2_index: int
    order: int = 1  # 1=single, 2=double, 3=triple


@dataclass
class DihedralAngle:
    """Dihedral angle constraint for coordinate scans."""

    atom_indices: Tuple[int, int, int, int]
    angle_degrees: float


class PointGroup(Enum):
    C1 = auto()
    Cs = auto()
    Ci = auto()
    C2 = auto()
    C2v = auto()
    C2h = auto()
    D2h = auto()
    D6h = auto()
    Td = auto()
    Oh = auto()


@dataclass
class Molecule:
    """Complete molecular description with topology and properties."""

    name: str
    formula: str
    atoms: List[Atom] = field(default_factory=list)
    bonds: List[Bond] = field(default_factory=list)
    charge: int = 0
    spin_multiplicity: int = 1
    point_group: Optional[PointGroup] = None
    smiles: Optional[str] = None
    inchi: Optional[str] = None
    molecular_weight: Optional[float] = None
    dihedral_constraints: List[DihedralAngle] = field(default_factory=list)

    @property
    def num_atoms(self) -> int:
        return len(self.atoms)

    @property
    def electron_count(self) -> int:
        atomic_numbers = {
            "H": 1, "He": 2, "Li": 3, "Be": 4, "B": 5, "C": 6, "N": 7, "O": 8,
            "F": 9, "Ne": 10, "Na": 11, "Mg": 12, "Al": 13, "Si": 14, "P": 15,
            "S": 16, "Cl": 17, "Ar": 18, "K": 19, "Ca": 20, "Fe": 26, "Cu": 29,
            "Zn": 30, "Br": 35, "I": 53,
        }
        total = sum(atomic_numbers.get(a.element.value, 0) for a in self.atoms)
        return total - self.charge

    def to_xyz(self) -> str:
        lines = [str(self.num_atoms), self.name]
        for a in self.atoms:
            lines.append(f"{a.element.value:2s}  {a.x:12.6f}  {a.y:12.6f}  {a.z:12.6f}")
        return "\n".join(lines)


@dataclass
class MolecularLibrary:
    """Repository of molecule definitions with search and registration."""

    entries: Dict[str, Molecule] = field(default_factory=dict)

    def register(self, mol: Molecule) -> None:
        self.entries[mol.name.lower()] = mol

    def get(self, name: str) -> Optional[Molecule]:
        return self.entries.get(name.lower())