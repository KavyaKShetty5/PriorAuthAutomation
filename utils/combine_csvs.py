import csv
import os
from data_dictionary import STANDARD_HEADERS, COLUMN_MAPPING

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "Data")
OUTPUT_FILE = os.path.join(DATA_DIR, "combined_data_source.csv")

# List CSV files to combine.
# If you only want specific files, update this list.
CSV_FILES = [
    "cms_chunk_1.csv",
    "EHR_Dataset.csv",
    "prior_authorization_dataset_2000.csv",
]


def clean_value(value):
    """
    Clean a value by replacing NA/null representations with empty string.
    Handles 'NA', 'nan', 'NaN', 'NULL', 'None', etc.
    """
    if value is None or value == "":
        return ""
    
    value_str = str(value).strip()
    
    # List of NA representations to replace
    na_values = ["NA", "nan", "NaN", "NULL", "None", "NONE", "null"]
    
    if value_str in na_values:
        return ""
    
    return value_str


def map_row(source_file, row):
    """
    Map a row from a source CSV file to standardized headers.
    Uses the COLUMN_MAPPING to rename columns.
    Cleans NA values during the mapping process.
    """
    mapping = COLUMN_MAPPING.get(source_file, {})
    mapped_row = {}
    
    for source_col, value in row.items():
        # Use mapping if available, otherwise keep original column name
        target_col = mapping.get(source_col, source_col)
        # Clean the value (replace NA with empty string)
        cleaned_value = clean_value(value)
        mapped_row[target_col] = cleaned_value
    
    return mapped_row


def combine_csvs(files, output_path):
    """
    Combine multiple CSV files using standardized headers.
    Creates a union of all data and replaces NA values with empty strings.
    """
    na_count = 0
    
    with open(output_path, 'w', newline='', encoding='utf-8') as out_file:
        writer = csv.DictWriter(out_file, fieldnames=STANDARD_HEADERS, restval="")
        writer.writeheader()

        total_rows = 0
        for file_name in files:
            path = os.path.join(DATA_DIR, file_name)
            if not os.path.exists(path):
                print(f"Warning: {file_name} not found, skipping.")
                continue
            
            print(f"Processing {file_name}...")
            rows_from_file = 0
            with open(path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                if reader.fieldnames is None:
                    continue
                
                for row in reader:
                    # Map the row to standardized headers and clean NA values
                    mapped_row = map_row(file_name, row)
                    
                    # Count NA values that were cleaned from the original row
                    for source_col, value in row.items():
                        cleaned_value = clean_value(value)
                        if cleaned_value == "" and value not in (None, ""):
                            na_count += 1
                    
                    # Fill in only the columns that are in STANDARD_HEADERS
                    combined_row = {header: mapped_row.get(header, "") for header in STANDARD_HEADERS}
                    writer.writerow(combined_row)
                    total_rows += 1
                    rows_from_file += 1
            
            print(f"  → {rows_from_file} rows processed from {file_name}")

    return total_rows, na_count


if __name__ == "__main__":
    print("=" * 70)
    print("Prior Authorization Data Union - Combining Multiple Sources")
    print("=" * 70)
    print(f"Combining {len(CSV_FILES)} files into combined data source")
    print(f"Using {len(STANDARD_HEADERS)} standardized headers")
    print("=" * 70)
    print()
    
    rows_written, na_replaced = combine_csvs(CSV_FILES, OUTPUT_FILE)
    
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Total rows written: {rows_written:,}")
    print(f"Total columns: {len(STANDARD_HEADERS)}")
    print(f"NA/null values replaced: {na_replaced:,}")
    print("=" * 70)
    print("✓ Combined data source created successfully!")
    print("=" * 70)
