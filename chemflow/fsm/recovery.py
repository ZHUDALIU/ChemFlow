"""Failure recovery strategies — automated recovery actions for failed calculations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional

from chemflow.fsm.states import JobState


@dataclass
class RecoveryAction:
    """A single recovery action with description."""
    target_state: JobState
    route_modification: str
    description: str
    priority: int = 5


class RecoveryStrategy:
    """Strategy-based recovery engine with escalating intervention levels."""

    RECOVERY_MAP: Dict[JobState, List[RecoveryAction]] = {
        JobState.SCF_FAILED: [
            RecoveryAction(JobState.HEALING, "scf=xqc", "Extrapolated SCF (XQC)", 1),
            RecoveryAction(JobState.HEALING, "scf=xqc int=ultrafine", "XQC + fine grid", 2),
            RecoveryAction(JobState.HEALING, "scf=qc int=ultrafine scf=novaracc",
                           "Quadratic convergence", 3),
        ],
        JobState.OSCILLATING: [
            RecoveryAction(JobState.HEALING, "scf=qc", "Quadratic convergence SCF", 1),
            RecoveryAction(JobState.HEALING, "opt=(maxstep=5,calcfc)", "Reduced step + calc FC", 2),
        ],
        JobState.IMAG_FREQ: [
            RecoveryAction(JobState.HEALING, "opt=(readfc,ts,noeigentest)",
                           "TS optimization from checkpoint", 1),
        ],
    }

    def get_recovery_plan(self, state: JobState) -> List[RecoveryAction]:
        return self.RECOVERY_MAP.get(state, [])

    def escalate(self, state: JobState, retry_count: int) -> Optional[RecoveryAction]:
        plan = self.get_recovery_plan(state)
        if retry_count < len(plan):
            return plan[retry_count]
        return None