import csv
import sys

# Load speaker mapping from speakers.csv
speaker_map = {}
with open('speakers.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        speaker_map[row['speaker_id']] = row['name']

# Process input stream
reader = csv.DictReader(sys.stdin)
fieldnames = reader.fieldnames

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for row in reader:
    speaker_id = row['Speaker']
    if speaker_id in speaker_map:
        row['Speaker'] = speaker_map[speaker_id]
    else:
        # Optional: log missing IDs to stderr
        sys.stderr.write(f"Warning: Missing speaker ID '{speaker_id}'\n")
        pass
    writer.writerow(row)