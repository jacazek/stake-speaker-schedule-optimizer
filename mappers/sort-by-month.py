import sys
import csv

# Define month order for sorting
month_order = {
    'Jan': 0, 'Feb': 1, 'March': 2, 'April': 3, 'May': 4, 'June': 5,
    'July': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
}

reader = csv.DictReader(sys.stdin)
fieldnames = reader.fieldnames

# Sort rows by month order and then by Unit
sorted_rows = sorted(
    reader,
    key=lambda row: (month_order.get(row['Month'], 12), row['Unit'])  # Sort by Month then Unit
)

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()
writer.writerows(sorted_rows)
