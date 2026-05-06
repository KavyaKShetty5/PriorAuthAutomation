import argparse
import csv
import json
from urllib.request import urlopen


def is_url(path: str) -> bool:
    return path.startswith('http://') or path.startswith('https://')


def load_json(source: str):
    if is_url(source):
        with urlopen(source, timeout=30) as response:
            return json.load(response)
    with open(source, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_visible_columns(data):
    columns = data['meta']['view']['columns']
    visible_indexes = []
    headers = []
    for index, col in enumerate(columns):
        if 'flags' not in col or 'hidden' not in col.get('flags', []):
            visible_indexes.append(index)
            headers.append(col['name'])
    return headers, visible_indexes


def convert_json_to_csv(source: str, output_path: str):
    data = load_json(source)
    headers, visible_indexes = extract_visible_columns(data)

    rows = []
    for row in data['data']:
        rows.append([row[i] for i in visible_indexes])

    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)

    print(f"CSV conversion complete. Output: {output_path}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert Socrata JSON export to CSV. Accepts either a local JSON file or a URL.'
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Local JSON file path or URL to the Socrata rows.json export.'
    )
    parser.add_argument(
        '--output', '-o',
        default='Data/wa_data.csv',
        help='Output CSV file path. Default: Data/wa_data.csv'
    )
    args = parser.parse_args()

    convert_json_to_csv(args.input, args.output)
