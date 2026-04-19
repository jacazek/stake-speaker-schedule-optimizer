from z3 import And, Not, Or

from .base import Constraint


class OverlapPreventionConstraint(Constraint):
    """Prevent overlapping speakers from being scheduled in the same month."""

    # (speaker_a, speaker_b) pairs that must not overlap
    overlap_pairs = [('SS', 'SSP'), ('YM', 'YMP')]

    def add(self, ctx):
        months = set()
        for unit, months_list in ctx.units.items():
            months.update(months_list)

        for month in months:
            indices = [i for i, (_, m) in enumerate(ctx.unit_month_pairs) if m == month]
            if not indices:
                continue
            for speaker_a, speaker_b in self.overlap_pairs:
                idx_a = ctx.speaker_indices[speaker_a]
                idx_b = ctx.speaker_indices[speaker_b]
                A = Or([ctx.speaker_vars[i] == idx_a for i in indices])
                B = Or([ctx.speaker_vars[i] == idx_b for i in indices])
                ctx.solver.add(Not(And(A, B)))
