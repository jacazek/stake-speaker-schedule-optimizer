from z3 import Or

from config import month_index
from .base import Constraint


class SpeakerSpacingConstraint(Constraint):
    """For each speaker, every pair of assignments must be at least `min_months` apart."""

    def add(self, ctx):
        for speaker in ctx.speakers:
            idx = ctx.speaker_indices[speaker]
            count = ctx.speaker_count[speaker]
            interval = ctx.speaker_interval[speaker]

            if count < 2:
                continue

            for i in range(ctx.num_unit_months):
                for j in range(i + 1, ctx.num_unit_months):
                    unit_i, month_i = ctx.unit_month_pairs[i]
                    unit_j, month_j = ctx.unit_month_pairs[j]
                    m1, m2 = month_index[month_i], month_index[month_j]
                    month_diff = abs(m2 - m1)

                    ctx.solver.add(Or(
                        ctx.speaker_vars[i] != idx,
                        ctx.speaker_vars[j] != idx,
                        month_diff >= interval
                    ))
