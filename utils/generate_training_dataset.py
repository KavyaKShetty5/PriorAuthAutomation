"""
Generate a training-ready synthetic dataset from combined data sources.
This script:
1. Loads combined data
2. Preprocesses and cleans all records
3. Handles missing values intelligently
4. Performs feature engineering
5. Outputs a unified synthetic dataset ready for ML model training
"""

import csv
import os
from data_dictionary import STANDARD_HEADERS

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "Data")
COMBINED_FILE = os.path.join(DATA_DIR, "combined_data_source.csv")
TRAINING_FILE = os.path.join(DATA_DIR, "synthetic_training_dataset.csv")

# Define feature types and handling strategies
NUMERIC_FEATURES = {
    'age', 'HMO_months', 'medreimb_IP', 'medreimb_OP', 'medreimb_CAR',
    'total_annual_cost', 'LOS_ICU', 'total_PA_requests', 'approval_rate',
    'mean_decision_time_standard', 'turnaround_time'
}

CATEGORICAL_FEATURES = {
    'gender', 'race_ethnicity', 'insurance_type', 'carrier', 'service_category',
    'service_code', 'apacheadmissiondx', 'unittype', 'unitadmitsource',
    'hospitaldischargelocation', 'hospitaldischargestatus', 'search_query',
    'year', 'severity_level', 'urgency_level'
}

BINARY_FEATURES = {
    'diabetes_flag', 'CHF_flag', 'CKD_flag', 'COPD_flag', 'cancer_flag',
    'PA_prone_user', 'high_cost_user'
}

TEXT_FEATURES = {'clinical_text', 'apacheadmissiondx', 'search_query'}

# Target variables for model training
TARGET_VARIABLES = {'PA_Status', 'PA_prone_user', 'high_cost_user'}


def try_float(value, default=0.0):
    """Safely convert value to float."""
    try:
        return float(value) if value and str(value).strip() else default
    except (ValueError, TypeError):
        return default


def normalize_categorical(value, feature_name):
    """Normalize categorical values to standard formats."""
    if not value or str(value).strip() == "":
        return "Unknown"
    
    value_str = str(value).strip().lower()
    
    # Gender normalization
    if feature_name == 'gender':
        if value_str in ['m', 'male', '1']:
            return 'Male'
        elif value_str in ['f', 'female', '0']:
            return 'Female'
        return 'Unknown'
    
    # Boolean/Binary normalization
    if feature_name in BINARY_FEATURES:
        if value_str in ['yes', 'true', '1', 'y']:
            return '1'
        elif value_str in ['no', 'false', '0', 'n']:
            return '0'
        return '0'
    
    # Capitalize categorical values
    return value_str.title() if value_str else "Unknown"


def impute_numeric(values, feature_name):
    """Calculate imputation value for numeric features."""
    numeric_vals = [try_float(v) for v in values if v and str(v).strip()]
    
    if not numeric_vals:
        return 0.0
    
    # Use median for outlier-resistant imputation
    numeric_vals.sort()
    if len(numeric_vals) % 2 == 0:
        return (numeric_vals[len(numeric_vals)//2 - 1] + numeric_vals[len(numeric_vals)//2]) / 2
    else:
        return numeric_vals[len(numeric_vals)//2]


def load_combined_data(file_path):
    """Load combined data from CSV file."""
    data = []
    try:
        with open(file_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Run combine_csvs.py first.")
        return None
    
    return data


def preprocess_row(row):
    """
    Preprocess a single row:
    - Clean numeric values
    - Normalize categorical values
    - Impute missing values
    - Create derived features
    """
    processed = {}
    
    for header in STANDARD_HEADERS:
        value = row.get(header, "")
        
        # Handle numeric features
        if header in NUMERIC_FEATURES:
            processed[header] = str(try_float(value))
        
        # Handle binary features
        elif header in BINARY_FEATURES:
            processed[header] = normalize_categorical(value, header)
        
        # Handle categorical features
        elif header in CATEGORICAL_FEATURES:
            processed[header] = normalize_categorical(value, header)
        
        # Handle text features
        elif header in TEXT_FEATURES:
            processed[header] = str(value).strip() if value else ""
        
        # Keep other fields as-is
        else:
            processed[header] = str(value).strip() if value else ""
    
    return processed


def create_training_dataset(combined_data):
    """
    Transform combined data into training-ready synthetic dataset.
    """
    if not combined_data:
        return None
    
    # Calculate statistics for imputation
    print("Computing statistics for numeric features...")
    numeric_stats = {}
    for feature in NUMERIC_FEATURES:
        values = [row.get(feature, "") for row in combined_data]
        numeric_stats[feature] = impute_numeric(values, feature)
    
    print(f"Processing {len(combined_data)} records...")
    training_data = []
    skipped_rows = 0
    
    for idx, row in enumerate(combined_data):
        # Preprocess the row
        processed_row = preprocess_row(row)
        
        # Second pass: impute missing numeric values
        for feature, default_value in numeric_stats.items():
            if feature in processed_row:
                val_str = processed_row[feature].strip()
                if not val_str or val_str == "0":
                    processed_row[feature] = str(default_value)
        
        # Validate that row has at least some data
        non_empty_count = sum(1 for v in processed_row.values() if v and str(v).strip())
        if non_empty_count > 0:
            training_data.append(processed_row)
        else:
            skipped_rows += 1
        
        if (idx + 1) % 1000 == 0:
            print(f"  Processed {idx + 1}/{len(combined_data)} records...")
    
    print(f"Skipped {skipped_rows} empty rows")
    return training_data


def write_training_dataset(training_data, output_path):
    """Write training dataset to CSV file."""
    if not training_data:
        print("No data to write.")
        return 0
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=STANDARD_HEADERS, restval="")
        writer.writeheader()
        
        for row in training_data:
            writer.writerow(row)
    
    return len(training_data)


def validate_dataset(training_data):
    """Validate and generate statistics about the training dataset."""
    if not training_data:
        return None
    
    stats = {
        'total_records': len(training_data),
        'total_columns': len(STANDARD_HEADERS),
        'numeric_features': len(NUMERIC_FEATURES),
        'categorical_features': len(CATEGORICAL_FEATURES),
        'binary_features': len(BINARY_FEATURES),
        'text_features': len(TEXT_FEATURES),
        'missing_by_column': {}
    }
    
    # Calculate missing values per column
    for header in STANDARD_HEADERS:
        missing_count = sum(1 for row in training_data 
                          if not row.get(header, "").strip())
        missing_pct = (missing_count / len(training_data)) * 100
        if missing_pct > 0:
            stats['missing_by_column'][header] = {
                'count': missing_count,
                'percentage': round(missing_pct, 2)
            }
    
    return stats


if __name__ == "__main__":
    print("=" * 80)
    print("SYNTHETIC TRAINING DATASET GENERATOR")
    print("=" * 80)
    print()
    
    # Step 1: Load combined data
    print("Step 1: Loading combined data...")
    combined_data = load_combined_data(COMBINED_FILE)
    if not combined_data:
        exit(1)
    print(f"  ✓ Loaded {len(combined_data):,} records")
    print()
    
    # Step 2: Preprocess and create training dataset
    print("Step 2: Preprocessing and creating training dataset...")
    training_data = create_training_dataset(combined_data)
    if not training_data:
        print("  ✗ Failed to create training dataset")
        exit(1)
    print(f"  ✓ Created {len(training_data):,} training records")
    print()
    
    # Step 3: Write training dataset
    print("Step 3: Writing training dataset to file...")
    rows_written = write_training_dataset(training_data, TRAINING_FILE)
    print(f"  ✓ Wrote {rows_written:,} records to {TRAINING_FILE}")
    print()
    
    # Step 4: Validate dataset
    print("Step 4: Validating dataset...")
    stats = validate_dataset(training_data)
    
    print("=" * 80)
    print("DATASET SUMMARY")
    print("=" * 80)
    print(f"Total Records:        {stats['total_records']:,}")
    print(f"Total Columns:        {stats['total_columns']}")
    print(f"Numeric Features:     {stats['numeric_features']}")
    print(f"Categorical Features: {stats['categorical_features']}")
    print(f"Binary Features:      {stats['binary_features']}")
    print(f"Text Features:        {stats['text_features']}")
    print()
    
    print("Columns with Missing Values:")
    if stats['missing_by_column']:
        for col, info in sorted(stats['missing_by_column'].items(), 
                               key=lambda x: x[1]['percentage'], reverse=True)[:10]:
            print(f"  {col:40s} {info['count']:6,} ({info['percentage']:5.1f}%)")
    else:
        print("  None - All columns are complete!")
    
    print()
    print("=" * 80)
    print(f"✓ Synthetic training dataset created successfully!")
    print(f"✓ Output: {TRAINING_FILE}")
    print("=" * 80)
