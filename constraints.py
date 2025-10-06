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




# # Constraint 5: For any speaker with 2 assignments, every pair of assignments must be at least 6 months apart
# for speaker in speakers:
#     if speaker_count[speaker] == 3:
#         continue  # Skip speakers with fewer than 3 assignments
#
#     idx = speaker_indices[speaker]
#
#     # Collect all unit-month indices where this speaker is assigned
#     # We'll check all pairs of indices where this speaker is assigned
#     for i in range(num_unit_months):
#         for j in range(i + 1, num_unit_months):
#             unit_i, month_i = unit_month_pairs[i]
#             unit_j, month_j = unit_month_pairs[j]
#             m1, m2 = month_order[month_i], month_order[month_j]
#             month_diff = abs(m2 - m1)
#
#             # If both assignments are to this speaker, enforce month_diff >= 6
#             solver.add_soft(Or(
#                 speaker_vars[i] != idx,
#                 speaker_vars[j] != idx,
#                 month_diff >= 6
#             ), weight=10)
#
# # Constraint 6: For any speaker with 3 assignments, every pair of assignments must be at least 4 months apart
# for speaker in speakers:
#     if speaker_count[speaker] == 3:
#         continue  # Skip speakers with fewer than 3 assignments
#
#     idx = speaker_indices[speaker]
#
#     # Collect all unit-month indices where this speaker is assigned
#     # We'll check all pairs of indices where this speaker is assigned
#     for i in range(num_unit_months):
#         for j in range(i + 1, num_unit_months):
#             unit_i, month_i = unit_month_pairs[i]
#             unit_j, month_j = unit_month_pairs[j]
#             m1, m2 = month_order[month_i], month_order[month_j]
#             month_diff = abs(m2 - m1)
#
#             # If both assignments are to this speaker, enforce month_diff >= 3
#             solver.add_soft(Or(
#                 speaker_vars[i] != idx,
#                 speaker_vars[j] != idx,
#                 month_diff >= 4
#             ), weight=10)
#
# # Constraint 7: For any speaker with 4 assignments, every pair of assignments must be at least 3 months apart
# for speaker in speakers:
#     if speaker_count[speaker] == 4:
#         continue  # Skip speakers with fewer than 3 assignments
#
#     idx = speaker_indices[speaker]
#
#     # Collect all unit-month indices where this speaker is assigned
#     # We'll check all pairs of indices where this speaker is assigned
#     for i in range(num_unit_months):
#         for j in range(i + 1, num_unit_months):
#             unit_i, month_i = unit_month_pairs[i]
#             unit_j, month_j = unit_month_pairs[j]
#             m1, m2 = month_order[month_i], month_order[month_j]
#             month_diff = abs(m2 - m1)
#
#             # If both assignments are to this speaker, enforce month_diff >= 3
#             solver.add_soft(Or(
#                 speaker_vars[i] != idx,
#                 speaker_vars[j] != idx,
#                 month_diff >= 3
#             ), weight=5)
#



# Replace the entire Constraint 5 with this efficient version:

# speaker_to_indices = {}
# for i, (unit, month) in enumerate(unit_month_pairs):
#     for speaker in speaker_indices:
#         idx = speaker_indices[speaker]
#         if idx not in speaker_to_indices:
#             speaker_to_indices[idx] = []
#         speaker_to_indices[idx].append(i)
#
# for speaker_idx in range(num_speakers):
#     count = speaker_count[speakers[speaker_idx]]
#     if count < 2:
#         continue
#
#     min_months = {2: 5, 3: 4, 4: 3}.get(count, 3)
#
#     indices = speaker_to_indices[speaker_idx]
#     month_indices = []
#     for i in indices:
#         unit, month = unit_month_pairs[i]
#         month_idx = month_order[month]
#         month_indices.append((i, month_idx))
#
#     month_indices.sort(key=lambda x: x[1])
#     # print(month_indices)
#     for k in range(len(month_indices) - 1):
#
#         i1, m1 = month_indices[k]
#         i2, m2 = month_indices[k + 1]
#         solver.add(Or(
#             speaker_vars[i1] != speaker_idx,
#             speaker_vars[i2] != speaker_idx,
#             abs(m2 - m1) >= min_months,
#         ))