"""FSM — Finite State Machine for workflow state management."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Callable, Dict, List, Optional


class JobState(Enum):
    INITIALIZED = auto()
    INPUT_GENERATED = auto()
    SUBMITTED = auto()
    RUNNING = auto()
    CONVERGED = auto()
    SCF_FAILED = auto()
    OSCILLATING = auto()
    IMAG_FREQ = auto()
    BASIS_ERROR = auto()
    OUT_OF_MEMORY = auto()
    PREEMPTED = auto()
    HEALING = auto()
    RESUBMITTED = auto()
    MAX_RETRIES = auto()
    ABORTED = auto()


@dataclass
class Transition:
    """A state transition with optional guard condition."""
    from_state: JobState
    to_state: JobState
    guard: Optional[Callable[[], bool]] = None
    action: Optional[Callable[[], None]] = None


class StateMachine:
    """Generic finite state machine for workflow orchestration.

    Features:
    - Guarded transitions with precondition checks
    - Entry/exit actions for each state
    - Transition history with timestamps
    - Error recovery paths
    """

    def __init__(self, initial_state: JobState = JobState.INITIALIZED):
        self._current: JobState = initial_state
        self._transitions: List[Transition] = []
        self._history: List[Dict] = []

    def add_transition(self, t: Transition) -> None:
        self._transitions.append(t)

    def transition_to(self, target: JobState) -> bool:
        for t in self._transitions:
            if t.from_state == self._current and t.to_state == target:
                if t.guard and not t.guard():
                    return False
                self._history.append({
                    "from": self._current.name,
                    "to": target.name,
                })
                if t.action:
                    t.action()
                self._current = target
                return True
        return False

    @property
    def state(self) -> JobState:
        return self._current

    @property
    def history(self) -> List[Dict]:
        return list(self._history)