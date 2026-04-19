from z3 import Or

from config import month_index
from .base import Constraint


class SpeakerSpacingConstraint(Constraint):
    """For each speaker, every pair of assignments must be at least `min_months` apart."""

    def add(self, solver):
        for speaker in self.ctx.speakers:
            idx = self.ctx.speaker_indices[speaker]
            count = self.ctx.speaker_count[speaker]
            interval = self.ctx.speaker_interval[speaker]

            if count < 2:
                continue

            for i in range(self.ctx.num_unit_months):
                for j in range(i + 1, self.ctx.num_unit_months):
                    unit_i, month_i = self.ctx.unit_month_pairs[i]
                    unit_j, month_j = self.ctx.unit_month_pairs[j]
                    m1, m2 = month_index[month_i], month_index[month_j]
                    month_diff = abs(m2 - m1)

                    solver.add(Or(
                        self.ctx.speaker_vars[i] != idx,
                        self.ctx.speaker_vars[j] != idx,
                        month_diff >= interval
                    ))
