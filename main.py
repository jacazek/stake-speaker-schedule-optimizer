from z3 import *

from constraints import (
    AssignmentCountsConstraint,
    ConstraintContext,
    NoRepeatVisitsConstraint,
    OverlapPreventionConstraint,
    SpeakerSpacingConstraint,
    SpecialUnitLimitsConstraint,
    VariableRangeConstraint,
)

# Define speakers and their allowed number of assignments
speakers = [
    'HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9', 'SSP', 'YMP', # 3
    'SS',  'YM', # 2
    'YW', 'RS', 'PRI' # 4
]
speaker_count = {
    'HC1': 3, 'HC2': 3, 'HC3': 3, 'HC4': 3, 'HC5': 3, 'HC6': 3, 'HC7': 3, 'HC8': 3, 'HC9': 3, 'SSP': 3, 'YMP': 3,
    'YM': 2, 'SS': 2,
    'YW': 4, 'RS': 4, 'PRI': 4
}

speaker_interval = {
    # Those who speak 3 times should speak every 4 months
    'HC6': 4, 'HC7': 4, 'HC8': 3, 'HC9': 3, 'SSP': 4, 'YMP': 4,
    # There are not enough speaking slots in the first quarter/third of the year for 4-month interval for all HC speakers
    # Therefore some are assigned 3-month intervals as all 3 of their assignments will happen in the last 3 quarters of the year
    'HC1': 3, 'HC2': 3, 'HC3': 3, 'HC4': 3, 'HC5': 3,
    # Those who speak 2 times should speak every 6 months
    'YM': 6, 'SS': 6,
    # Those who speak 4 times should speak every 3 months
    'YW': 3, 'RS': 3, 'PRI': 3
}

# Define units and their months
units = {
    'Durham 5th': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Roxboro': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Durham YSA': ['June', 'Sep', 'Dec'],
    'Chapel Hill 1st': ['June', 'Sep', 'Dec'],
    'Chapel Hill 2nd': ['April', 'July', 'Oct'],
    'Durham 1st': ['May', 'Aug', 'Nov'],
    'Durham 2nd': ['June', 'Sep', 'Dec'],
    'Hillsborough': ['May', 'Aug', 'Nov'],
    'Mebane': ['April', 'July', 'Oct'],
    'FSLG-CH1': ['Jan', 'April', 'July', 'Oct']
}

# Create all unit-month pairs and their quarter mappings
unit_month_pairs = []
quarter_map = {}


def get_quarter(month):
    if month in ['Jan', 'Feb', 'March']:
        return 1
    elif month in ['April', 'May', 'June']:
        return 2
    elif month in ['July', 'Aug', 'Sep']:
        return 3
    elif month in ['Oct', 'Nov', 'Dec']:
        return 4


for unit, months in units.items():
    for month in months:
        unit_month_pairs.append((unit, month))
        quarter_map[(unit, month)] = get_quarter(month)

# Map speakers to indices
speaker_indices = {s: i for i, s in enumerate(speakers)}
num_speakers = len(speakers)
num_unit_months = len(unit_month_pairs)

# Create Z3 variables for each unit-month pair
speaker_vars = [Int(f'speaker_{i}') for i in range(num_unit_months)]

# Initialize solver
solver = Optimize()

# Build context and add constraints
ctx = ConstraintContext(
    speakers=speakers,
    speaker_count=speaker_count,
    speaker_interval=speaker_interval,
    units=units,
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

# Add optimization objective to make solver deterministic
# Minimize the sum of speaker variables to prefer lower indices
# solver.minimize(Sum(ctx.speaker_vars))

# Check for solution
if solver.check() == sat:
    model = solver.model()
    assignments = []
    for i in range(num_unit_months):
        unit, month = unit_month_pairs[i]
        speaker_idx = model[speaker_vars[i]].as_long()
        speaker = speakers[speaker_idx]
        assignments.append((unit, month, speaker))

    # Print the result in tabular format
    print("Unit,Month,Speaker")
    for unit, month, speaker in assignments:
        print(f"{unit},{month},{speaker}")
else:
    print("No solution found.")
    core = solver.unsat_core()
    print("Conflicting assumptions: ", core)
