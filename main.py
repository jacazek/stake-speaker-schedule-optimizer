from z3 import *
import itertools

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

period_map = {
    'Jan': 1, 'Feb': 1, 'March': 1, 'April': 1,
    'May': 2, 'June': 2, 'July': 2, 'Aug': 2,
    'Sep': 3, 'Oct': 3, 'Nov': 3, 'Dec': 3
}

# Map speakers to indices
speaker_indices = {s: i for i, s in enumerate(speakers)}
num_speakers = len(speakers)
num_unit_months = len(unit_month_pairs)

# Create Z3 variables for each unit-month pair
speaker_vars = [Int(f'speaker_{i}') for i in range(num_unit_months)]

# Initialize solver
solver = Optimize()



a1, a2, a3, a4, a5 = Bools('a1 a2 a3 a4 a5')

# Constraint 1: Each speaker variable must be in the range of speakers
for var in speaker_vars:
    solver.add(Implies(a1, And(0 <= var, var < num_speakers)))






# Constraint 2: Each speaker must have exactly their permitted number of assignments
for speaker in speakers:
    idx = speaker_indices[speaker]
    count = speaker_count[speaker]
    total = Sum([If(var == idx, 1, 0) for var in speaker_vars])
    solver.add(Implies(a2, total == count))






# Constraint 3: No speaker can speak at the same unit more than once
unit_to_indices = {}
for i, (unit, month) in enumerate(unit_month_pairs):
    if unit not in unit_to_indices:
        unit_to_indices[unit] = []
    unit_to_indices[unit].append(i)
for unit, indices in unit_to_indices.items():
    for speaker_idx in range(num_speakers):
        total = Sum([If(speaker_vars[i] == speaker_idx, 1, 0) for i in indices])
        solver.add(Implies(a3, total <= 1))






# Constraint 4: Each speaker must have at most 2 assignments in special units
special_units = ['Durham 5th', 'Roxboro', 'FSLG-CH1']
for speaker_idx in range(num_speakers):
    total = 0
    for unit in special_units:
        if unit in unit_to_indices:
            for i in unit_to_indices[unit]:
                total += If(speaker_vars[i] == speaker_idx, 1, 0)
    solver.add(Implies(a4, total <= 2))


# Precompute month order for distance checks
month_order = {
    'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
    'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
}

# Constraint 5: For each speaker, every pair of assignments must be at least `min_months` apart,
# where `min_months` depends on the speaker's total assignment count.
# - 3 assignments → min 4 months apart
# - 4 assignments → min 3 months apart
# - 2 assignments → min 6 months apart
# (Note: We skip speakers with 1 assignment since no pairs exist.)
soft_months = {
    2: 6,
    3: 4,
    4: 3
}

hard_months = {
    2: 5,
    3: 3,
    4: 2
}
for speaker in speakers:
    idx = speaker_indices[speaker]
    count = speaker_count[speaker]

    # Skip if fewer than 2 assignments (no pairs to check)
    if count > 3:
        continue

    # Define minimum required month gap based on count
    min_soft_months = soft_months.get(count, 1)  # Default to 1 if not in map (shouldn't happen)
    min_hard_months = hard_months.get(count, 1)

    # Check all pairs of unit-month indices for this speaker
    for i in range(num_unit_months):
        for j in range(i + 1, num_unit_months):
            unit_i, month_i = unit_month_pairs[i]
            unit_j, month_j = unit_month_pairs[j]
            m1, m2 = month_order[month_i], month_order[month_j]
            month_diff = abs(m2 - m1)

            # If both assignments are to this speaker, enforce month_diff >= min_months
            solver.add_soft(Or(
                speaker_vars[i] != idx,
                speaker_vars[j] != idx,
                month_diff >= min_soft_months
            ), weight=10)

            solver.add(Or(
                speaker_vars[i] != idx,
                speaker_vars[j] != idx,
                month_diff >= min_hard_months
            ))






# Check for solution
if solver.check(a1, a2, a3, a4, a5) == sat:
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
