# Mappers

A pipeline of CSV transformation scripts that convert the raw output from the Z3 solver into a human-readable schedule. Each mapper reads CSV from stdin, transforms it, and writes to stdout — designed to be chained together with pipes.

## Pipeline

```bash
cat possible-solution-4.csv \
  | python sort-by-month.py \
  | python speaker-name-mapper.py \
  | python month-name-mapper.py \
  | python unit-name-mapper.py \
  | python inject_date.py \
  > final_schedule.csv
```

## Mappers

### sort-by-month.py

Sorts the schedule rows chronologically by month, then alphabetically by unit within each month.

- **Input columns:** `Unit`, `Month` (abbreviated)
- **Output columns:** Same as input, sorted
- **Month order:** Jan → Dec

### speaker-name-mapper.py

Maps speaker IDs (e.g., `HC1`, `YW`, `PRI`) to their full names using the mapping defined in `speakers.csv`.

- **Input columns:** `Unit`, `Month`, `Speaker`
- **Output columns:** Same as input, with `Speaker` replaced by full name
- **Dependency:** Reads `speakers.csv` from the project root

### month-name-mapper.py

Converts month abbreviations to full month names for readability.

| Abbreviation | Full Name   |
|-------------|-------------|
| Jan         | January     |
| Feb         | February    |
| March       | March       |
| April       | April       |
| May         | May         |
| June        | June        |
| July        | July        |
| Aug         | August      |
| Sep         | September   |
| Oct         | October     |
| Nov         | November    |
| Dec         | December    |

### unit-name-mapper.py

Expands abbreviated unit names to their full descriptive names.

| Abbreviation   | Full Name                  |
|---------------|----------------------------|
| Durham 5th    | Durham 5th (Spanish)       |
| FSLG-CH1      | French Sango Language Group|
| All others    | Unchanged                  |

### inject_date.py

Adds a `Date` column with the exact date of the third Sunday of each month, which is the typical stake meeting date. The year is hardcoded to 2026 but can be changed by modifying the `year` parameter in `get_third_sunday()`.

- **Input columns:** `Unit`, `Month`, `Speaker`
- **Output columns:** Same as input + `Date` (format: `YYYY-MM-DD`)
- **Logic:** Computes the third Sunday of each month using Python's `datetime` module
