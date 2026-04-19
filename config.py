"""Static configuration for the speaker schedule optimizer."""

import csv
from enum import Enum


class Month(str, Enum):
    """Months used by units for speaking assignments."""
    JAN = 'January'
    FEB = 'February'
    MAR = 'March'
    APR = 'April'
    MAY = 'May'
    JUN = 'June'
    JUL = 'July'
    AUG = 'August'
    SEP = 'September'
    OCT = 'October'
    NOV = 'November'
    DEC = 'December'

    @classmethod
    def by_value(cls):
        """Return a dict mapping month string value to Month enum member."""
        return {m.value: m for m in cls}


# Load speaker data from speakers.csv
_csv_path = "speakers.csv"

speakers = []
speaker_count = {}
speaker_interval = {}

with open(_csv_path, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        sid = row["speaker_id"]
        speakers.append(sid)
        speaker_count[sid] = int(row["assignment_count"])
        speaker_interval[sid] = int(row["interval"])

# Define units and their available months
ALL_MONTHS = [Month.JAN, Month.FEB, Month.MAR, Month.APR, Month.MAY, Month.JUN,
              Month.JUL, Month.AUG, Month.SEP, Month.OCT, Month.NOV, Month.DEC]

units = {
    'Durham 5th': ALL_MONTHS,
    'Roxboro': ALL_MONTHS,
    'Durham YSA': [Month.JUN, Month.SEP, Month.DEC],
    'Chapel Hill 1st': [Month.JUN, Month.SEP, Month.DEC],
    'Chapel Hill 2nd': [Month.APR, Month.JUL, Month.OCT],
    'Durham 1st': [Month.MAY, Month.AUG, Month.NOV],
    'Durham 2nd': [Month.JUN, Month.SEP, Month.DEC],
    'Hillsborough': [Month.MAY, Month.AUG, Month.NOV],
    'Mebane': [Month.APR, Month.JUL, Month.OCT],
    'FSLG-CH1': [Month.JAN, Month.APR, Month.JUL, Month.OCT],
}

# Month-to-quarter lookup
month_to_quarter = {
    Month.JAN: 1, Month.FEB: 1, Month.MAR: 1,
    Month.APR: 2, Month.MAY: 2, Month.JUN: 2,
    Month.JUL: 3, Month.AUG: 3, Month.SEP: 3,
    Month.OCT: 4, Month.NOV: 4, Month.DEC: 4,
}

month_index = {
    Month.JAN: 1, Month.FEB: 2, Month.MAR: 3, Month.APR: 4, Month.MAY: 5, Month.JUN: 6,
    Month.JUL: 7, Month.AUG: 8, Month.SEP: 9, Month.OCT: 10, Month.NOV: 11, Month.DEC: 12
}


def get_quarter(month):
    """Return the quarter (1-4) for a given month."""
    return month_to_quarter[month]


def build_unit_month_pairs(units):
    """Build list of (unit, month) pairs and their quarter mappings."""
    unit_month_pairs = []
    quarter_map = {}
    for unit, months in units.items():
        for month in months:
            unit_month_pairs.append((unit, month))
            quarter_map[(unit, month)] = get_quarter(month)
    return unit_month_pairs, quarter_map
