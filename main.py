from z3 import *
import itertools

# Define speakers and their allowed number of assignments
speakers = [
    'SSP', 'SS', 'YMP', 'YM', 'HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9',
    'YW', 'RS', 'PRI'
]
speaker_count = {
    'HC1': 3, 'HC2': 3, 'HC3': 3, 'HC4': 3, 'HC5': 3, 'HC6': 3, 'HC7': 3, 'HC8': 3, 'HC9': 3,
    'SSP': 3, 'YMP': 3, 'YW': 4, 'RS': 4, 'PRI': 4, 'YM': 2, 'SS': 2
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
solver = Solver()






# Constraint 1: Each speaker variable must be in the range of speakers
for var in speaker_vars:
    solver.add(And(0 <= var, var < num_speakers))






# Constraint 2: Each speaker must have exactly their permitted number of assignments
for speaker in speakers:
    idx = speaker_indices[speaker]
    count = speaker_count[speaker]
    total = Sum([If(var == idx, 1, 0) for var in speaker_vars])
    solver.add(total == count)






# Constraint 3: No speaker can speak at the same unit more than once
unit_to_indices = {}
for i, (unit, month) in enumerate(unit_month_pairs):
    if unit not in unit_to_indices:
        unit_to_indices[unit] = []
    unit_to_indices[unit].append(i)
for unit, indices in unit_to_indices.items():
    for speaker_idx in range(num_speakers):
        total = Sum([If(speaker_vars[i] == speaker_idx, 1, 0) for i in indices])
        solver.add(total <= 1)






# Constraint 4: Each speaker must have at most 2 assignments in special units
special_units = ['Durham 5th', 'Roxboro', 'FSLG-CH1']
for speaker_idx in range(num_speakers):
    total = 0
    for unit in special_units:
        if unit in unit_to_indices:
            for i in unit_to_indices[unit]:
                total += If(speaker_vars[i] == speaker_idx, 1, 0)
    solver.add(total <= 2)






# Constraint 5: Each speaker with 4 assignments must have one assignment per quarter
for speaker in speakers:
    if speaker_count[speaker] == 4:
        idx = speaker_indices[speaker]
        for q in [1, 2, 3, 4]:
            total = Sum([
                If(And(speaker_vars[i] == idx, quarter_map[(unit, month)] == q), 1, 0)
                for i, (unit, month) in enumerate(unit_month_pairs)
            ])
            solver.add(total == 1)



# Precompute: for each speaker and period, which unit-month indices are relevant
speaker_period_indices = {}
for speaker in speakers:
    idx = speaker_indices[speaker]
    speaker_period_indices[idx] = {p: [] for p in [1, 2, 3]}
    for i, (unit, month) in enumerate(unit_month_pairs):
        period = period_map[month]
        speaker_period_indices[idx][period].append(i)

# Constraint 6: Each speaker with 3 assignments must have exactly one assignment per period (1, 2, 3)
for speaker in speakers:
    if speaker_count[speaker] == 3:
        idx = speaker_indices[speaker]
        for period in [1, 2, 3]:
            # Only sum over the unit-months in this period for this speaker
            total = Sum([
                If(speaker_vars[i] == idx, 1, 0)
                for i in speaker_period_indices[idx][period]
            ])
            solver.add(total == 1)
#
#
# # Constraint 7: Each speaker with 2 assignments must have one assignment every 6 months
# for speaker in speakers:
#     if speaker_count[speaker] == 2:
#         idx = speaker_indices[speaker]
#         month_order = {'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
#                        'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
#         for i in range(num_unit_months):
#             for j in range(i + 1, num_unit_months):
#                 unit1, month1 = unit_month_pairs[i]
#                 unit2, month2 = unit_month_pairs[j]
#                 m1, m2 = month_order[month1], month_order[month2]
#                 diff = abs(m2 - m1)
#                 solver.add(Or(speaker_vars[i] != idx, speaker_vars[j] != idx, diff >= 6))


































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