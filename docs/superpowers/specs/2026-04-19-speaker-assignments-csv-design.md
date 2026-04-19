# Speaker Assignments CSV Generator - Design

## Context

The project maintains speaker configuration in `config.py` with three related data structures:
- `speakers` array: list of 15 speaker IDs
- `speaker_count` dict: number of assignments per speaker
- `speaker_interval` dict: minimum interval between assignments per speaker

These values are currently only used internally by the optimizer. There is no standalone CSV export of speaker assignment metadata.

## Goal

Create a standalone script that generates `speaker_assignments.csv` from the config data, providing a human-readable reference of each speaker's assignment count and interval requirements.

## Design

### Script: `generate_speakers_csv.py`

A simple Python script that:
1. Imports `speakers`, `speaker_count`, `speaker_interval` from `config.py`
2. Writes `speaker_assignments.csv` with columns: `id`, `assignment_count`, `interval`, `name`
3. Each row corresponds to one speaker, in the order they appear in the `speakers` array
4. The `name` column is left empty for now

### CSV Output

```
id,assignment_count,interval,name
HC1,3,3,
HC2,3,3,
...
```

### Implementation Details

- Uses Python stdlib only (`csv` module)
- No classes or complex structure — procedural script
- Overwrites existing file if present
- Follows existing project patterns (see `mappers/*.py` for csv module usage)

### Files

- **New:** `generate_speakers_csv.py` (project root)
- **New:** `speaker_assignments.csv` (generated output)
