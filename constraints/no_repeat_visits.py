from z3 import If, Sum

from .base import Constraint


class NoRepeatVisitsConstraint(Constraint):
    """No speaker can speak at the same unit more than once."""

    def add(self, solver):
        unit_to_indices = {}
        for i, (unit, month) in enumerate(self.ctx.unit_month_pairs):
            if unit not in unit_to_indices:
                unit_to_indices[unit] = []
            unit_to_indices[unit].append(i)
        for unit, indices in unit_to_indices.items():
            for speaker_idx in range(self.ctx.num_speakers):
                total = Sum([If(self.ctx.speaker_vars[i] == speaker_idx, 1, 0) for i in indices])
                solver.add(total <= 1)
