from z3 import And

from .base import Constraint


class VariableRangeConstraint(Constraint):
    """Each speaker variable must be in the range of speakers."""

    def add(self, solver):
        for var in self.ctx.speaker_vars:
            solver.add(And(0 <= var, var < self.ctx.num_speakers))
