# Stake Speaker Schedule Optimizer

A constraint-based scheduler that automatically assigns stake speakers to ward/branch meetings throughout the year using the Z3 theorem prover.

## Overview

This tool solves the recurring problem of scheduling stake speakers (e.g., HC, SSP, YM, YW, RS, PRI) across multiple wards and branches. It finds a valid schedule that satisfies all hard constraints, including:

- **Exact assignment counts** — each speaker is assigned their required number of talks per year
- **No repeat visits** — no speaker speaks at the same unit more than once
- **Special unit limits** — speakers with 4 assignments are limited to 2 visits in special units (Durham 5th, Roxboro, FSLG-CH1); SS and YM are limited to 1
- **Overlap prevention** — SS and SSP never speak in the same month; YM and YMP never speak in the same month
- **Speaking frequency** — speakers with 4 assignments get exactly one per quarter
- **Minimum spacing** — pairs of assignments for each speaker are spaced at least as many months apart as their interval requirement (e.g., 6 months for 2-assignment speakers, 3 months for 3-assignment speakers)

## Project Structure

```
.
├── main.py                  # Z3 constraint solver — generates the schedule
├── constraints.py           # Additional/hard constraints (imported by main.py)
├── speakers.csv             # Speaker ID-to-name mapping
├── email_reminder_pipeline.sh  # Bash pipeline to format output
├── mappers/
│   ├── sort-by-month.py     # Sorts schedule rows by month
│   ├── speaker-name-mapper.py   # Maps speaker IDs to full names
│   ├── month-name-mapper.py     # Expands month abbreviations to full names
│   ├── unit-name-mapper.py      # Expands unit abbreviations to full names
│   └── inject_date.py       # Adds exact dates (third Sunday of each month)
└── .gitignore
```

## Requirements

- Python 3.x
- Z3 solver: `pip install z3-solver`

## How to Run

### 1. Generate the schedule

```bash
python main.py
```

This outputs a CSV to stdout with columns: `Unit,Month,Speaker` (using speaker IDs).

Save the output to a file:

```bash
python main.py > possible-solution-4.csv
```

### 2. Format the schedule

Run the pipeline script to sort, expand names, and add dates:

```bash
bash email_reminder_pipeline.sh
```

This reads `possible-solution-4.csv` and pipes it through the mappers to produce `final_schedule.csv` with human-readable unit names, speaker names, full month names, and exact dates.

### 3. (Optional) Add dates manually

The `inject_date.py` mapper computes the third Sunday of each month (the typical stake speaker date) and adds a `Date` column. Include it in the pipeline:

```bash
cat possible-solution-4.csv \
  | python mappers/sort-by-month.py \
  | python mappers/speaker-name-mapper.py \
  | python mappers/month-name-mapper.py \
  | python mappers/unit-name-mapper.py \
  | python mappers/inject_date.py \
  > final_schedule.csv
```

## Customization

- **Speakers & counts** — Edit the `speakers` and `speaker_count` lists in `main.py`
- **Unit schedules** — Modify the `units` dict in `main.py` to add/remove wards and their meeting months
- **Constraints** — Adjust `speaker_interval`, `special_units`, and constraint blocks in `main.py` and `constraints.py`
