from z3 import If

from .base import Constraint


class SpecialUnitLimitsConstraint(Constraint):
    """Each speaker must have at most 2 assignments in special units unless they are SS or YM."""

    def add(self, ctx):
        special_units = ['Durham 5th', 'Roxboro', 'FSLG-CH1']
        unit_to_indices = {}
        for i, (unit, month) in enumerate(ctx.unit_month_pairs):
            if unit not in unit_to_indices:
                unit_to_indices[unit] = []
            unit_to_indices[unit].append(i)

        for speaker_idx in range(ctx.num_speakers):
            total = 0
            speaker = ctx.speakers[speaker_idx]

            for unit in special_units:
                if unit in unit_to_indices:
                    for i in unit_to_indices[unit]:
                        total += If(ctx.speaker_vars[i] == speaker_idx, 1, 0)
            if speaker == 'SS' or speaker == 'YM':
                ctx.solver.add(total <= 1)
            else:
                ctx.solver.add(total <= 2)
