from z3 import If, Sum

from .base import Constraint


class AssignmentCountsConstraint(Constraint):
    """Each speaker must have exactly their permitted number of assignments."""

    def add(self, ctx):
        for speaker in ctx.speakers:
            idx = ctx.speaker_indices[speaker]
            count = ctx.speaker_count[speaker]
            total = Sum([If(var == idx, 1, 0) for var in ctx.speaker_vars])
            ctx.solver.add(total == count)
