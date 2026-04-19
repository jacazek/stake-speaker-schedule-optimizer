import sys
import csv
from datetime import datetime, timedelta

def get_third_sunday(month, year=2026):
    month_map = {
        'Jan': 1, 'Feb': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    first_day = datetime(year, month_map[month], 1)
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