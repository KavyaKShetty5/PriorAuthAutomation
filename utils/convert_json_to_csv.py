import json
import csv

# Load the JSON data
with open('Data/cms_data.txt', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract column names, skipping hidden meta columns
columns = data['meta']['view']['columns']
headers = []
for col in columns:
    if 'flags' not in col or 'hidden' not in col.get('flags', []):
        headers.append(col['name'])

# Extract data rows, skipping the first 8 meta fields per row
rows = []
for row in data['data']:
    # Skip the first 8 fields (meta data)
    data_row = row[8:]
    rows.append(data_row)

# Write to CSV
with open('Data/cms_chunk_1.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    writer.writerows(rows)

print("CSV conversion complete. Output: Data/cms_chunk_1.csv")