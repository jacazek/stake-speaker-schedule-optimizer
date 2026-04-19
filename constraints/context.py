class ConstraintContext:
    """Holds all shared data needed by constraints."""

    def __init__(
        self,
        speakers,
        speaker_count,
        speaker_interval,
        units,
        unit_month_pairs,
        quarter_map,
        speaker_indices,
        num_speakers,
        num_unit_months,
        speaker_vars,
        solver,
    ):
        self.speakers = speakers
        self.speaker_count = speaker_count
        self.speaker_interval = speaker_interval
        self.units = units
        self.unit_month_pairs = unit_month_pairs
        self.quarter_map = quarter_map
        self.speaker_indices = speaker_indices
        self.num_speakers = num_speakers
        self.num_unit_months = num_unit_months
        self.speaker_vars = speaker_vars
        self.solver = solver
