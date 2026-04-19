import csv
import sys

# Month abbreviation to full name mapping
month_map = {
    'Jan': 'January',
    'Feb': 'February',
    'March': 'March',
    'April': 'April',
    'May': 'May',
    'June': 'June',
    'July': 'July',
    'Aug': 'August',
    'Sep': 'September',
    'Oct': 'October',
    'Nov': 'November',
    'Dec': 'December'
}

reader = csv.DictReader(sys.stdin)
fieldnames = reader.fieldnames

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for row in reader:
    if row['Month'] in month_map:
        row['Month'] = month_map[row['Month']]
    writer.writerow(row)