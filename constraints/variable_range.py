from z3 import And

from .base import Constraint


class VariableRangeConstraint(Constraint):
    """Each speaker variable must be in the range of speakers."""

    def add(self, ctx):
        for var in ctx.speaker_vars:
            ctx.solver.add(And(0 <= var, var < ctx.num_speakers))
