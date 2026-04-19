from z3 import And, Not, Or

from .base import Constraint


class OverlapPreventionConstraint(Constraint):
    """Prevent overlapping speakers from being scheduled in the same month."""

    # (speaker_a, speaker_b) pairs that must not overlap
    overlap_pairs = [('SS', 'SSP'), ('YM', 'YMP')]

    def add(self, solver):
        months = set()
        for unit, months_list in self.ctx.units.items():
            months.update(months_list)

        for month in months:
            indices = [i for i, (_, m) in enumerate(self.ctx.unit_month_pairs) if m == month]
            if not indices:
                continue
            for speaker_a, speaker_b in self.overlap_pairs:
                idx_a = self.ctx.speaker_indices[speaker_a]
                idx_b = self.ctx.speaker_indices[speaker_b]
                A = Or([self.ctx.speaker_vars[i] == idx_a for i in indices])
                B = Or([self.ctx.speaker_vars[i] == idx_b for i in indices])
                solver.add(Not(And(A, B)))
