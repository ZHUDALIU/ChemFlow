"""Tests for InputMaster and GaussianInput."""

import pytest
from chemflow.input_master import InputMaster, GaussianInput


class TestInputMaster:
    """Test InputMaster.generate() with various molecules and parameters."""

    def setup_method(self) -> None:
        self.master = InputMaster()

    def test_generate_water_opt(self) -> None:
        result = self.master.generate("water", "B3LYP", "6-31G(d)", "Opt")
        assert "%chk=water.chk" in result
        assert "# Opt B3LYP/6-31G(d)" in result
        assert "0 1" in result
        assert "O" in result
        assert "H" in result

    def test_generate_aspirin_sp(self) -> None:
        result = self.master.generate("aspirin", "HF", "STO-3G", "SP")
        assert "%chk=aspirin.chk" in result
        assert "# SP HF/STO-3G" in result
        assert "Title: aspirin SP at HF/STO-3G" in result

    def test_generate_benzene_freq(self) -> None:
        result = self.master.generate("benzene", "B3LYP", "6-31G(d)", "Freq")
        assert "%chk=benzene.chk" in result
        assert "# Freq B3LYP/6-31G(d)" in result
        assert "C" in result
        assert "H" in result

    def test_generate_ethanol(self) -> None:
        result = self.master.generate("ethanol", "M06-2X", "def2TZVP", "Opt")
        assert "%chk=ethanol.chk" in result
        assert "# Opt M06-2X/def2TZVP" in result
        assert "O    1.300000" in result

    def test_generate_methane(self) -> None:
        result = self.master.generate("methane", "HF", "STO-3G", "SP")
        assert "%chk=methane.chk" in result
        assert "C    0.000000" in result

    def test_generate_unknown_molecule_raises(self) -> None:
        with pytest.raises(ValueError, match="Unknown molecule"):
            self.master.generate("fullerene", "B3LYP", "6-31G(d)", "Opt")

    def test_generate_case_insensitive(self) -> None:
        result = self.master.generate("Water", "B3LYP", "6-31G(d)", "SP")
        assert "%chk=water.chk" in result

    def test_empty_task(self) -> None:
        result = self.master.generate("water", "B3LYP", "6-31G(d)", "")
        assert "# B3LYP/6-31G(d)" in result


class TestGaussianInput:
    """Test GaussianInput dataclass and builder."""

    def test_build_gjf_basic(self) -> None:
        gjf = GaussianInput(
            route="Opt B3LYP/6-31G(d)",
            charge=0,
            multiplicity=1,
            coordinates="O    0.0    0.0    0.1\nH    0.0    0.8   -0.5",
            molecule="water",
        )
        output = gjf.build_gjf()
        assert "%chk=water.chk" in output
        assert "# Opt B3LYP/6-31G(d)" in output
        assert "0 1" in output
        assert output.endswith("\n")

    def test_build_gjf_includes_title(self) -> None:
        gjf = GaussianInput(
            route="SP HF/STO-3G",
            charge=0,
            multiplicity=1,
            coordinates="C    0.0    0.0    0.0",
            molecule="methane",
            method="HF",
            basis="STO-3G",
            task="SP",
        )
        output = gjf.build_gjf()
        assert "Title: methane SP at HF/STO-3G" in output