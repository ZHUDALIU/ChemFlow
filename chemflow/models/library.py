"""Molecular library management — built-in and user-defined molecule registries."""

from __future__ import annotations

from chemflow.models.molecule import Molecule, Atom, Element


def build_default_library() -> dict:
    """Construct the built-in molecular library with curated coordinates.

    Returns:
        Dictionary mapping molecule names to Molecule instances.
    """
    library = {}

    library["water"] = Molecule(
        name="water",
        formula="H2O",
        atoms=[
            Atom(Element.O, 0.000000, 0.000000, 0.117000),
            Atom(Element.H, 0.000000, 0.757000, -0.468000),
            Atom(Element.H, 0.000000, -0.757000, -0.468000),
        ],
        charge=0,
        spin_multiplicity=1,
        molecular_weight=18.015,
    )

    library["methane"] = Molecule(
        name="methane",
        formula="CH4",
        atoms=[
            Atom(Element.C, 0.000000, 0.000000, 0.000000),
            Atom(Element.H, 1.087000, 0.000000, 0.000000),
            Atom(Element.H, -0.362333, 1.025000, 0.000000),
            Atom(Element.H, -0.362333, -0.512500, 0.887700),
            Atom(Element.H, -0.362333, -0.512500, -0.887700),
        ],
        charge=0,
        spin_multiplicity=1,
        molecular_weight=16.043,
    )

    library["benzene"] = Molecule(
        name="benzene",
        formula="C6H6",
        atoms=[
            Atom(Element.C, 0.000000, 1.396000, 0.000000),
            Atom(Element.C, 1.209000, 0.698000, 0.000000),
            Atom(Element.C, 1.209000, -0.698000, 0.000000),
            Atom(Element.C, 0.000000, -1.396000, 0.000000),
            Atom(Element.C, -1.209000, -0.698000, 0.000000),
            Atom(Element.C, -1.209000, 0.698000, 0.000000),
            Atom(Element.H, 0.000000, 2.484000, 0.000000),
            Atom(Element.H, 2.149000, 1.242000, 0.000000),
            Atom(Element.H, 2.149000, -1.242000, 0.000000),
            Atom(Element.H, 0.000000, -2.484000, 0.000000),
            Atom(Element.H, -2.149000, -1.242000, 0.000000),
            Atom(Element.H, -2.149000, 1.242000, 0.000000),
        ],
        charge=0,
        spin_multiplicity=1,
        molecular_weight=78.114,
    )

    library["aspirin"] = Molecule(
        name="aspirin",
        formula="C9H8O4",
        atoms=[
            Atom(Element.C, 0.000000, 0.000000, 0.000000),
            Atom(Element.C, 1.400000, 0.000000, 0.000000),
            Atom(Element.C, 2.100000, 1.200000, 0.000000),
            Atom(Element.C, 1.400000, 2.400000, 0.000000),
            Atom(Element.C, 0.000000, 2.400000, 0.000000),
            Atom(Element.C, -0.700000, 1.200000, 0.000000),
            Atom(Element.C, 2.100000, -1.300000, 0.000000),
            Atom(Element.O, 1.600000, -2.400000, 0.000000),
            Atom(Element.O, 3.420000, -1.150000, 0.000000),
            Atom(Element.C, 3.500000, -1.700000, 0.000000),
            Atom(Element.C, 4.200000, -2.350000, 0.000000),
            Atom(Element.O, 1.200000, 3.600000, 0.000000),
            Atom(Element.O, -1.920000, 1.200000, 0.000000),
            Atom(Element.H, -0.520000, -0.950000, 0.000000),
            Atom(Element.H, 3.180000, 1.200000, 0.000000),
            Atom(Element.H, 5.240000, -2.050000, 0.000000),
            Atom(Element.H, 4.080000, -2.950000, 0.900000),
            Atom(Element.H, 3.900000, -2.900000, -0.880000),
            Atom(Element.H, -2.350000, 0.340000, 0.000000),
            Atom(Element.H, 2.400000, 0.400000, 0.000000),
            Atom(Element.H, 1.820000, -2.900000, 0.000000),
        ],
        charge=0,
        spin_multiplicity=1,
        molecular_weight=180.158,
    )

    library["ethanol"] = Molecule(
        name="ethanol",
        formula="C2H5OH",
        atoms=[
            Atom(Element.C, -0.047000, 0.000000, 0.000000),
            Atom(Element.C, 1.462000, 0.000000, 0.000000),
            Atom(Element.O, 1.960000, 1.332000, 0.000000),
            Atom(Element.H, -0.407000, -0.518000, 0.891000),
            Atom(Element.H, -0.410000, 1.025000, -0.032000),
            Atom(Element.H, -0.410000, -0.517000, -0.890000),
            Atom(Element.H, 1.825000, -0.518000, 0.889000),
            Atom(Element.H, 1.825000, -0.519000, -0.889000),
            Atom(Element.H, 1.671000, 1.806000, 0.788000),
        ],
        charge=0,
        spin_multiplicity=1,
        molecular_weight=46.069,
    )

    return library


DEFAULT_LIBRARY = build_default_library()