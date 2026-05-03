"""FSM transition definitions — workflow state transitions for Gaussian jobs."""

from __future__ import annotations

from chemflow.fsm.states import JobState, StateMachine, Transition


class WorkflowTransitionBuilder:
    """Builds a complete state machine with all valid transitions."""

    @staticmethod
    def build_calculation_fsm() -> StateMachine:
        """Construct the calculation lifecycle state machine."""
        sm = StateMachine(JobState.INITIALIZED)
        sm.add_transition(Transition(JobState.INITIALIZED, JobState.INPUT_GENERATED))
        sm.add_transition(Transition(JobState.INPUT_GENERATED, JobState.SUBMITTED))
        sm.add_transition(Transition(JobState.SUBMITTED, JobState.RUNNING))
        sm.add_transition(Transition(JobState.RUNNING, JobState.CONVERGED))
        sm.add_transition(Transition(JobState.RUNNING, JobState.SCF_FAILED))
        sm.add_transition(Transition(JobState.RUNNING, JobState.OSCILLATING))
        sm.add_transition(Transition(JobState.RUNNING, JobState.IMAG_FREQ))
        sm.add_transition(Transition(JobState.RUNNING, JobState.BASIS_ERROR))
        sm.add_transition(Transition(JobState.RUNNING, JobState.OUT_OF_MEMORY))
        sm.add_transition(Transition(JobState.SCF_FAILED, JobState.HEALING))
        sm.add_transition(Transition(JobState.OSCILLATING, JobState.HEALING))
        sm.add_transition(Transition(JobState.IMAG_FREQ, JobState.HEALING))
        sm.add_transition(Transition(JobState.HEALING, JobState.RESUBMITTED))
        sm.add_transition(Transition(JobState.RESUBMITTED, JobState.RUNNING))
        sm.add_transition(Transition(JobState.SCF_FAILED, JobState.MAX_RETRIES))
        sm.add_transition(Transition(JobState.OSCILLATING, JobState.MAX_RETRIES))
        sm.add_transition(Transition(JobState.MAX_RETRIES, JobState.ABORTED))
        return sm