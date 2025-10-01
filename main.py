from z3 import *
import itertools

# Define speakers and their allowed number of assignments
speakers = [
    'SSP', 'SS', 'YMP', 'YM', 'HC1', 'HC2', 'HC3', 'HC4', 'HC5', 'HC6', 'HC7', 'HC8', 'HC9',
    'YW', 'RS', 'PRI'
]
speaker_count = {
    'HC1': 4, 'HC2': 4, 'HC3': 4, 'HC4': 4, 'HC5': 4, 'HC6': 4, 'HC7': 4, 'HC8': 4, 'HC9': 4,
    'SSP': 2, 'YMP': 2, 'YW': 4, 'RS': 4, 'PRI': 4, 'YM': 2, 'SS': 2
}

# Define units and their months
units = {
    'Durham 5th': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Roxboro': ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'Durham YSA': ['Jan', 'April', 'July', 'Oct'],
    'Chapel Hill 1st': ['March', 'June', 'Sep', 'Dec'],
    'Chapel Hill 2nd': ['Jan', 'April', 'July', 'Oct'],
    'Durham 1st': ['March', 'June', 'Sep', 'Dec'],
    'Durham 2nd': ['Feb', 'May', 'Aug', 'Nov'],
    'Hillsborough': ['March', 'June', 'Sep', 'Dec'],
    'Mebane': ['Feb', 'May', 'Aug', 'Nov'],
    'FSLG-CH1': ['Feb', 'May', 'Aug', 'Nov']
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

# Constraint 4: For special units, no speaker can have more than 2 assignments
special_units = ['Durham 5th', 'Roxboro', 'FSLG-CH1']
for speaker_idx in range(num_speakers):
    total = 0
    for unit in special_units:
        if unit in unit_to_indices:
            for i in unit_to_indices[unit]:
                total += If(speaker_vars[i] == speaker_idx, 1, 0)
    solver.add(total <= 2)

# Constraint 5: Speakers with 4 assignments must have one assignment per quarter
four_assignment_speakers = [s for s in speakers if speaker_count[s] == 4]
for speaker in four_assignment_speakers:
    speaker_idx = speaker_indices[speaker]
    for q in [1, 2, 3, 4]:
        total = 0
        for i, (unit, month) in enumerate(unit_month_pairs):
            if quarter_map[(unit, month)] == q:
                total += If(speaker_vars[i] == speaker_idx, 1, 0)
        solver.add(total == 1)


ym_idx = speaker_indices['YM']
ymp_idx = speaker_indices['YMP']
ss_idx = speaker_indices['SS']
ssp_idx = speaker_indices['SSP']

# Constraint 6: YM/YMP must use at least 3 distinct units
for unit, indices in unit_to_indices.items():
    total = Sum([If(Or(speaker_vars[i] == ym_idx, speaker_vars[i] == ymp_idx), 1, 0) for i in indices])
    solver.add(total <= 1)

# Ensure exactly 3 distinct units are used by YM and YMP
total_units = Sum([If(Or(speaker_vars[i] == ym_idx, speaker_vars[i] == ymp_idx), 1, 0) for i in range(num_unit_months)])
solver.add(total_units >= 3)

# Constraint 7: YM/YMP must have assignments in alternating quarters
# Ensure YM and YMP do not share any quarter
for q in [1, 2, 3, 4]:
    total = 0
    for i, (unit, month) in enumerate(unit_month_pairs):
        if quarter_map[(unit, month)] == q:
            total += If(speaker_vars[i] == ym_idx, 1, 0)
            total += If(speaker_vars[i] == ymp_idx, 1, 0)
    solver.add(total <= 1)


# Constraint 8: SS/SSP cannot share any quarter
# Ensure each unit is used at most once by SS or SSP
for unit, indices in unit_to_indices.items():
    total = Sum([If(Or(speaker_vars[i] == ss_idx, speaker_vars[i] == ssp_idx), 1, 0) for i in indices])
    solver.add(total <= 1)

# Ensure exactly 3 distinct units are used by SS and SSP
total_units = Sum([If(Or(speaker_vars[i] == ss_idx, speaker_vars[i] == ssp_idx), 1, 0) for i in range(num_unit_months)])
solver.add(total_units >= 3)

# Ensure YM and YMP do not share any quarter
for q in [1, 2, 3, 4]:
    total = 0
    for i, (unit, month) in enumerate(unit_month_pairs):
        if quarter_map[(unit, month)] == q:
            total += If(speaker_vars[i] == ss_idx, 1, 0)
            total += If(speaker_vars[i] == ssp_idx, 1, 0)
    solver.add(total <= 1)



# # Constraint 7: YM and YMP combined must be on 4 different units
# for unit, indices in unit_to_indices.items():
#     total = Sum([If(Or(speaker_vars[i] == ym_idx, speaker_vars[i] == ymp_idx), 1, 0) for i in indices])
#     solver.add(total <= 1)
#
# # Constraint 8: SS and SSP combined must be on 4 different units
# for unit, indices in unit_to_indices.items():
#     total = Sum([If(Or(speaker_vars[i] == ss_idx, speaker_vars[i] == ssp_idx), 1, 0) for i in indices])
#     solver.add(total <= 1)

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