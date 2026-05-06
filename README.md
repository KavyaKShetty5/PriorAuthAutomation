# PriorAuthAutomation
Research on how AI can be applied to improve the efficiency, accuracy, and scalability of the prior authorization process.

## Repository Overview
This project combines prior authorization data from multiple sources and transforms it into training-ready datasets for machine learning.

## Key Datasets
- `Data/wa_data.csv` — WA prior authorization public dataset converted from Socrata JSON.
- `Data/cms_data.txt` — Raw CMS JSON export from the WA dataset source.
- `Data/prior_authorization_dataset_2000.csv` — Existing prior authorization dataset used as a schema reference.
- `Data/prior_authorization_dataset_wa_cms.csv` — Newly generated combined dataset using `wa_data.csv` and `cms_data.txt`, output in the same header format as `prior_authorization_dataset_2000.csv`.

## Main Utility Scripts
- `utils/convert_json_to_csv.py`
  - Converts a Socrata `rows.json` export to CSV.
  - Supports local JSON files or direct URLs.
- `utils/combine_wa_and_cms_to_prior_auth_dataset.py`
  - Merges `wa_data.csv` and `cms_data.txt` and generates `Data/prior_authorization_dataset_wa_cms.csv` with the project schema.
- `utils/combine_csvs.py`
  - Combines project source CSVs into `Data/combined_data_source.csv`.
- `utils/generate_training_dataset.py`
  - Preprocesses `Data/combined_data_source.csv` and writes `Data/synthetic_training_dataset.csv`.

## How to regenerate the new dataset
1. Convert the WA JSON source to CSV (if needed):
```bash
python utils/convert_json_to_csv.py --input "https://data.wa.gov/api/views/fysr-7kwx/rows.json?accessType=DOWNLOAD" --output Data/wa_data.csv
```
2. Generate the combined prior authorization dataset:
```bash
python utils/combine_wa_and_cms_to_prior_auth_dataset.py
```
3. Use the generated dataset for training or further preprocessing.

## Notes
- The new combined dataset uses the header schema from `prior_authorization_dataset_2000.csv`.
- The repository has been cleaned to keep only the current data pipeline utilities.
