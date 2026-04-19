from z3 import Int, Optimize, sat

from constraints import (
    AssignmentCountsConstraint,
    ConstraintContext,
    NoRepeatVisitsConstraint,
    OverlapPreventionConstraint,
    SpeakerSpacingConstraint,
    SpecialUnitLimitsConstraint,
    VariableRangeConstraint,
)
import config

unit_month_pairs, quarter_map = config.build_unit_month_pairs(config.units)

# Map speakers to indices
speaker_indices = {s: i for i, s in enumerate(config.speakers)}
num_speakers = len(config.speakers)
num_unit_months = len(unit_month_pairs)

# Create Z3 variables for each unit-month pair
speaker_vars = [Int(f'speaker_{i}') for i in range(num_unit_months)]

# Initialize solver
solver = Optimize()

# Build context and add constraints
ctx = ConstraintContext(
    speakers=config.speakers,
    speaker_count=config.speaker_count,
    speaker_interval=config.speaker_interval,
    units=config.units,
    unit_month_pairs=unit_month_pairs,
    quarter_map=quarter_map,
    speaker_indices=speaker_indices,
    num_speakers=num_speakers,
    num_unit_months=num_unit_months,
    speaker_vars=speaker_vars,
    solver=solver,
)

VariableRangeConstraint().add(ctx)
AssignmentCountsConstraint().add(ctx)
NoRepeatVisitsConstraint().add(ctx)
SpecialUnitLimitsConstraint().add(ctx)
OverlapPreventionConstraint().add(ctx)
SpeakerSpacingConstraint().add(ctx)

# Check for solution
if solver.check() == sat:
    model = solver.model()
    assignments = []
    for i in range(num_unit_months):
        unit, month = unit_month_pairs[i]
        speaker_idx = model[speaker_vars[i]].as_long()
        speaker = config.speakers[speaker_idx]
        assignments.append((unit, month, speaker))

    # Print the result in tabular format
    print("Unit,Month,Speaker")
    for unit, month, speaker in assignments:
        print(f"{unit},{month},{speaker}")
else:
    print("No solution found.")
    core = solver.unsat_core()
    print("Conflicting assumptions: ", core)
