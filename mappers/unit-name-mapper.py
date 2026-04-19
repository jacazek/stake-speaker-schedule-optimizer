import csv
import sys

reader = csv.DictReader(sys.stdin)
fieldnames = reader.fieldnames

writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
writer.writeheader()

for row in reader:
    if row['Unit'] == 'Durham 5th':
        row['Unit'] = 'Durham 5th (Spanish)'
    elif row['Unit'] == 'FSLG-CH1':
        row['Unit'] = 'French Sango Language Group'
    writer.writerow(row)