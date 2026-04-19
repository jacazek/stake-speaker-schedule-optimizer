import sys
import os
import csv

from datetime import datetime, timedelta

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import month_index

def get_third_sunday(month, year=2026):
    first_day = datetime(year, month_index[month], 1)
    days_to_sunday = (6 - first_day.weekday() + 7) % 7
    first_sunday = first_day + timedelta(days=days_to_sunday)
    return (first_sunday + timedelta(days=14)).strftime("%Y-%m-%d")

reader = csv.DictReader(sys.stdin)
fieldnames = reader.fieldnames + ['Date']
writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for row in reader:
    row['Date'] = get_third_sunday(row['Month'])
    writer.writerow(row)