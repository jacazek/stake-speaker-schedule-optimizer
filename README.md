# Stake Speaker Schedule Optimizer

A constraint-based scheduler that automatically assigns stake speakers to ward/branch meetings throughout the year using the Z3 theorem prover.

## Overview

This tool solves the recurring problem of scheduling stake speakers (e.g., HC, SSP, YM, YW, RS, PRI) across multiple wards and branches. It finds a valid schedule that satisfies all hard constraints, including:

- **Exact assignment counts** — each speaker is assigned their required number of talks per year
- **No repeat visits** — no speaker speaks at the same unit more than once
- **Special unit limits** — speakers are limited to 2 visits in special units (Durham 5th, Roxboro, FSLG-CH1); SS and YM are limited to 1
- **Overlap prevention** — SS and SSP never speak in the same month; YM and YMP never speak in the same month
- **Custom intervals** — each speaker has a configurable minimum month gap between assignments (defined in `speakers.csv`)

## Project Structure

```
.
├── main.py                  # Z3 constraint solver — generates the schedule
├── config.py                # Static configuration (units, months, speaker defaults)
├── speakers.csv             # Speaker ID, assignment count, interval, and name
├── generate_speakers_csv.py # Utility to regenerate speakers.csv from config.py
├── export_final_schedule.sh # Bash pipeline to format output
├── constraints/             # Constraint implementations (Z3)
│   ├── __init__.py
│   ├── base.py              # Base Constraint class
│   ├── context.py           # ConstraintContext (shared data)
│   ├── assignment_counts.py # Exact assignment counts per speaker
│   ├── no_repeat_visits.py  # No speaker repeats at same unit
│   ├── special_unit_limits.py # Limits on special unit visits
│   ├── overlap_prevention.py # Prevent overlapping speaker types in same month
│   ├── speaker_spacing.py   # Minimum month gap between assignments
│   └── variable_range.py    # Speaker index bounds
├── mappers/
│   ├── sort-by-month.py     # Sorts schedule rows by month
│   ├── speaker-name-mapper.py   # Maps speaker IDs to full names
│   ├── month-name-mapper.py   # Expands month abbreviations to full names
│   ├── unit-name-mapper.py      # Expands unit abbreviations to full names
│   └── inject_date.py       # Adds exact dates (third Sunday of each month)
└── .gitignore
```

## Installation

1. Ensure Python 3.x is installed
2. Create a virtual environment:

```bash
python3 -m venv venv
```

3. Activate the virtual environment:

```bash
# macOS / Linux
source venv/bin/activate

# Windows (Command Prompt)
venv\Scripts\activate

# Windows (PowerShell)
venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

### 1. Generate the schedule

```bash
python main.py
```

This outputs a CSV to stdout with columns: `Unit,Month,Speaker` (using speaker IDs).

Save the output to a file:

```bash
python main.py > test_snapshot.csv
```

### 2. Format the schedule

Run the pipeline script to sort and expand names:

```bash
bash export_final_schedule.sh
```

This reads `test_snapshot.csv` and pipes it through the mappers to produce `final_schedule.csv` with human-readable unit names, speaker names, and full month names.

### 3. (Optional) Add dates

The `inject_date.py` mapper computes the third Sunday of each month (the typical stake speaker date) and adds a `Date` column. Include it in the pipeline:

```bash
cat test_snapshot.csv \
  | python mappers/sort-by-month.py \
  | python mappers/speaker-name-mapper.py \
  | python mappers/unit-name-mapper.py \
  | python mappers/month-name-mapper.py \
  | python mappers/inject_date.py \
  > final_schedule.csv
```

## Customization

- **Speakers & counts** — Edit `speakers.csv` to add/remove speakers, change assignment counts, or set custom intervals
- **Unit schedules** — Modify the `units` dict in `config.py` to add/remove wards and their meeting months
- **Constraints** — All constraints are defined in the `constraints/` package and use data from `config.py` and `speakers.csv`
