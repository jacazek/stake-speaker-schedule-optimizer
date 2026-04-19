from z3 import If, Sum

from .base import Constraint


class AssignmentCountsConstraint(Constraint):
    """Each speaker must have exactly their permitted number of assignments."""

    def add(self, solver):
        for speaker in self.ctx.speakers:
            idx = self.ctx.speaker_indices[speaker]
            count = self.ctx.speaker_count[speaker]
            total = Sum([If(var == idx, 1, 0) for var in self.ctx.speaker_vars])
            solver.add(total == count)
