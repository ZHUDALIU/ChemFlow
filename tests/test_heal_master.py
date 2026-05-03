"""Tests for HealMaster — diagnosis and healing logic."""

import pytest
from chemflow.heal_master import HealMaster, Status


class TestDiagnose:
    """Test HealMaster.diagnose() pattern matching."""

    def setup_method(self) -> None:
        self.healer = HealMaster()

    def test_diagnose_converged(self) -> None:
        log = "Normal termination of Gaussian\nHave a nice day."
        assert self.healer.diagnose(log) == Status.CONVERGED

    def test_diagnose_scf_failed(self) -> None:
        log = "Convergence failure in SCF iteration"
        assert self.healer.diagnose(log) == Status.SCF_FAILED

    def test_diagnose_oscillating(self) -> None:
        log = "The SCF is Oscillating in step 12"
        assert self.healer.diagnose(log) == Status.OSCILLATING

    def test_diagnose_oscillating_lowercase(self) -> None:
        log = "oscillating energy detected"
        assert self.healer.diagnose(log) == Status.OSCILLATING

    def test_diagnose_imag_freq(self) -> None:
        log = "1 imaginary frequencies found."
        assert self.healer.diagnose(log) == Status.IMAG_FREQ

    def test_diagnose_imag_freq_singular(self) -> None:
        log = "1 imaginary frequency detected."
        assert self.healer.diagnose(log) == Status.IMAG_FREQ

    def test_diagnose_running(self) -> None:
        log = "SCF Done: E = -76.3\nGradGradGrad"
        assert self.healer.diagnose(log) == Status.RUNNING

    def test_diagnose_empty_log(self) -> None:
        assert self.healer.diagnose("") == Status.RUNNING


class TestHeal:
    """Test HealMaster.heal() route modification logic."""

    def setup_method(self) -> None:
        self.healer = HealMaster()

    @staticmethod
    def _make_gjf(route: str = "# Opt B3LYP/6-31G(d)") -> str:
        return (
            "%chk=test.chk\n"
            f"{route}\n"
            "\n"
            "Title\n"
            "\n"
            "0 1\n"
            "H    0.0    0.0    0.0\n"
        )

    def test_heal_scf_failed_adds_xqc(self) -> None:
        result = self.healer.heal(self._make_gjf(), Status.SCF_FAILED)
        assert "scf=xqc" in result
        assert "int=ultrafine" in result

    def test_heal_scf_failed_does_not_duplicate(self) -> None:
        gjf = self._make_gjf("# Opt B3LYP/6-31G(d) scf=xqc")
        result = self.healer.heal(gjf, Status.SCF_FAILED)
        assert result.count("scf=xqc") == 1

    def test_heal_oscillating_adds_qc(self) -> None:
        result = self.healer.heal(self._make_gjf(), Status.OSCILLATING)
        assert "scf=qc" in result

    def test_heal_converged_returns_original(self) -> None:
        gjf = self._make_gjf()
        result = self.healer.heal(gjf, Status.CONVERGED)
        assert result == gjf

    def test_heal_running_returns_original(self) -> None:
        gjf = self._make_gjf()
        result = self.healer.heal(gjf, Status.RUNNING)
        assert result == gjf

    def test_heal_imag_freq_raises(self) -> None:
        gjf = self._make_gjf()
        with pytest.raises(ValueError, match="Imaginary frequencies"):
            self.healer.heal(gjf, Status.IMAG_FREQ)

    def test_heal_preserves_route_with_indent(self) -> None:
        gjf = " %chk=test.chk\n # Opt HF/STO-3G\n\n0 1\nH 0 0 0\n"
        result = self.healer.heal(gjf, Status.SCF_FAILED)
        assert "# Opt HF/STO-3G scf=xqc int=ultrafine" in result

    def test_heal_scf_failed_route_contains_both_flags(self) -> None:
        result = self.healer.heal(self._make_gjf(), Status.SCF_FAILED)
        lines = result.split("\n")
        route_line = next(line for line in lines if line.strip().startswith("#"))
        assert "scf=xqc" in route_line
        assert "int=ultrafine" in route_line

    def test_heal_oscillating_route_contains_qc(self) -> None:
        result = self.healer.heal(self._make_gjf(), Status.OSCILLATING)
        lines = result.split("\n")
        route_line = next(line for line in lines if line.strip().startswith("#"))
        assert "scf=qc" in route_line