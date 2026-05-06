# Synthetic Training Dataset

## Overview
`synthetic_training_dataset.csv` is a unified, preprocessed dataset created from multiple data sources (CMS, EHR, and Prior Authorization datasets) and ready for machine learning model training.

## Dataset Statistics
- **Total Records:** 12,970
- **Total Features:** 33
- **Numeric Features:** 11
- **Categorical Features:** 15
- **Binary Features:** 7
- **Text Features:** 3

## Data Processing Pipeline

### 1. **Data Consolidation**
   - Combined 2 CSV sources:
     - `cms_chunk_1.csv` (9,323 records)
     - `EHR_Dataset.csv` (1,447 records)

### 2. **Data Cleaning**
   - Replaced 54,962 NA/null values with empty strings or imputed values
   - Removed invalid/empty rows
   - Standardized field names across all sources

### 3. **Feature Normalization**
   - **Gender:** Normalized to 'Male', 'Female', 'Unknown'
   - **Binary Features:** Normalized to '0' or '1'
   - **Categorical Features:** Title-cased and standardized
   - **Numeric Features:** Converted to float values with median imputation

### 4. **Missing Value Imputation**
   - Numeric features: Filled with median values
   - Categorical features: Filled with 'Unknown'
   - Binary features: Defaulted to '0'

## Feature Categories

### Patient Demographics
- `beneficiary_id` - Patient identifier
- `age` - Age in years
- `sex`, `gender` - Patient gender
- `race_ethnicity` - Race/ethnicity classification

### Insurance Information
- `HMO_months` - Months enrolled in HMO
- `insurance_type` - Type of insurance coverage

### Chronic Conditions (Binary Flags)
- `diabetes_flag` - Diabetes indicator
- `CHF_flag` - Congestive heart failure
- `CKD_flag` - Chronic kidney disease
- `COPD_flag` - COPD indicator
- `cancer_flag` - Cancer indicator

### Financial Metrics
- `medreimb_IP` - Annual inpatient reimbursement
- `medreimb_OP` - Annual outpatient reimbursement
- `medreimb_CAR` - Annual carrier (physician) reimbursement
- `total_annual_cost` - Total annual cost

### Target Variables (Model Labels)
- `PA_prone_user` - Binary: Prone to prior authorization requests
- `high_cost_user` - Binary: High cost user (top decile)

### Clinical/ICU Data
- `apacheadmissiondx` - ICU admission diagnosis
- `unittype` - ICU type (Neuro ICU, Med-Surg ICU, etc.)
- `unitadmitsource` - Source of admission to ICU
- `LOS_ICU` - Length of stay in ICU
- `hospitaldischargelocation` - Discharge location
- `hospitaldischargestatus` - Patient status at discharge (Alive/Deceased)
- `clinical_text` - Free text summary of clinical notes

### Prior Authorization Metrics
- `carrier` - Insurance carrier ID
- `year` - Reporting year
- `service_category` - Service category
- `service_code` - Medical service code
- `total_PA_requests` - Number of PA requests
- `approval_rate` - Proportion approved (0-1)
- `mean_decision_time_standard` - Average decision time in hours

### Additional Fields
- `search_query` - Clinical context label
- `severity_level` - Severity classification
- `urgency_level` - Urgency classification
- `turnaround_time` - Processing time

## Data Completeness

| Feature | Missing % | Notes |
|---------|-----------|-------|
| sex | 100.0% | Not available in source data, set to Unknown |
| beneficiary_id | 83.0% | Partially available from sources |
| clinical_text | 71.9% | From EHR dataset subset |
| Most others | < 20% | High completeness |

## Usage for Model Training

### Python with Pandas
```python
import pandas as pd

# Load the dataset
df = pd.read_csv('synthetic_training_dataset.csv')

# Split features and target
X = df.drop(['PA_prone_user', 'high_cost_user'], axis=1)
y = df['PA_prone_user']  # or 'high_cost_user' for another target

# Train model
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```

### Python with scikit-learn
```python
from sklearn.preprocessing import LabelEncoder, StandardScaler
import pandas as pd

df = pd.read_csv('synthetic_training_dataset.csv')

# Encode categorical variables
le = LabelEncoder()
categorical_cols = ['gender', 'race_ethnicity', 'insurance_type', 'carrier', ...]
for col in categorical_cols:
    df[col] = le.fit_transform(df[col].astype(str))

# Scale numeric features
scaler = StandardScaler()
numeric_cols = ['age', 'HMO_months', 'medreimb_IP', ...]
df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
```

## Data Quality Assurance
✓ No completely empty rows  
✓ Standardized data types  
✓ Consistent categorical values  
✓ Numeric values validated and imputed  
✓ All 33 features present in all records  

## Files Generated
- `combined_data_source.csv` - Intermediate combined file (before preprocessing)
- `synthetic_training_dataset.csv` - **Final training-ready dataset** ← Use this for models

## Scripts
- `combine_csvs.py` - Combines raw CSVs into unified source
- `generate_training_dataset.py` - Preprocesses combined data into training dataset
- `data_dictionary.py` - Defines standard schema and column mappings

## Next Steps
1. Load the synthetic dataset into your ML framework
2. Perform exploratory data analysis (EDA)
3. Handle any remaining domain-specific preprocessing
4. Split into train/validation/test sets
5. Train your model using the standardized features
