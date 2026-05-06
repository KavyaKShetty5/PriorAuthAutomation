# PriorAuthAutomation
Research on how AI can be applied to improve the efficiency, accuracy, and scalability of the prior authorization process.

## Repository Overview
This project combines prior authorization data from multiple sources and transforms it into training-ready datasets for machine learning.

## Key Datasets
- `Data/RawData/wa_data.csv` — WA prior authorization public dataset converted from Socrata JSON.
- `Data/RawData/cms_data.txt` — Raw CMS JSON export from the WA dataset source.
- `Data/Clean_data/prior_authorization_dataset_wa_cms.csv` — Newly generated combined dataset using `wa_data.csv` and `cms_data.txt`, output in the target project schema.

## Main Utility Scripts
- `utils/convert_json_to_csv.py`
  - Converts a Socrata `rows.json` export to CSV.
  - Supports local JSON files or direct URLs.
- `utils/combine_wa_and_cms_to_prior_auth_dataset.py`
  - Reads raw data from `Data/RawData/` and outputs the combined schema dataset to `Data/Clean_data/`.
- `utils/combine_csvs.py`
  - Combines project raw CSVs from `Data/RawData/` into `Data/Clean_data/combined_data_source.csv`.
- `utils/generate_training_dataset.py`
  - Preprocesses `Data/Clean_data/combined_data_source.csv` and writes `Data/Clean_data/synthetic_training_dataset.csv`.

## How to regenerate the new dataset
1. Convert the WA JSON source to CSV (if needed):
```bash
python utils/convert_json_to_csv.py --input "https://data.wa.gov/api/views/fysr-7kwx/rows.json?accessType=DOWNLOAD" --output Data/RawData/wa_data.csv
```
2. Generate the combined prior authorization dataset:
```bash
python utils/combine_wa_and_cms_to_prior_auth_dataset.py
```
3. Use the generated dataset for training or further preprocessing.

## Notes
- The new combined dataset uses the target project schema defined by the current utility pipeline.
- The repository has been cleaned to keep only the current data pipeline utilities.
