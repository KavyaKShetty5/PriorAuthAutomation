import csv
import json
import random
from datetime import date, timedelta
from pathlib import Path

TARGET_HEADERS = [
    'Patient_ID',
    'Encounter_ID',
    'Age',
    'Gender',
    'Diagnosis_Code',
    'Diagnosis_Description',
    'Procedure_Code',
    'Procedure_Description',
    'Comorbidity_Count',
    'Procedure_Cost',
    'Insurance_Type',
    'Provider_Type',
    'Claim_Amount_Paid',
    'Clinical_Notes',
    'Severity_Level',
    'Urgency_Level',
    'Condition_Type',
    'PA_Status',
    'Submission_Type',
    'Turnaround_Time',
    'Encounter_Date',
]

DIAGNOSES = [
    ('M54', 'Back Pain'),
    ('K21', 'GERD'),
    ('J45', 'Asthma'),
    ('E11', 'Type 2 Diabetes'),
    ('I10', 'Hypertension'),
]

GENDER_CHOICES = [('Female', 0.511), ('Male', 0.489)]
INSURANCE_CHOICES = [('Private', 0.349), ('Medicaid', 0.343), ('Medicare', 0.308)]
SEVERITY_CHOICES = [('Medium', 0.416), ('High', 0.389), ('Low', 0.195)]
URGENCY_CHOICES = [('Urgent', 0.61), ('Emergency', 0.196), ('Routine', 0.194)]
CONDITION_CHOICES = [('Acute', 0.782), ('Chronic', 0.218)]
SUBMISSION_CHOICES = [('Manual', 0.516), ('AI', 0.484)]
PROVIDER_TYPES = ['Hospital', 'Clinic']
CLINICAL_NOTES = [
    'Chronic disease, requires continuous monitoring',
    'Stable condition, periodic evaluation needed',
    'Emergency case with acute complications',
    'Mild condition, routine follow-up recommended',
    'Patient shows severe symptoms and requires immediate attention',
]

AGE_VALUES = list(range(19, 90))
AGE_WEIGHTS = [1.0 for _ in AGE_VALUES]
COMORBIDITY_DISTRIBUTION = [(0, 0.05), (1, 0.15), (2, 0.35), (3, 0.30), (4, 0.15)]


def weighted_choice(options):
    choices, weights = zip(*options)
    return random.choices(choices, weights=weights, k=1)[0]


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))


def sample_comorbidity_count():
    values, weights = zip(*COMORBIDITY_DISTRIBUTION)
    return random.choices(values, weights=weights, k=1)[0]


def parse_wa_csv(path):
    rows = []
    with Path(path).open(newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({k.strip(): v.strip() for k, v in row.items()})
    return rows


def parse_cms_json(path):
    with Path(path).open('r', encoding='utf-8') as f:
        data = json.load(f)

    columns = data['meta']['view']['columns']
    visible_indexes, headers = [], []
    for index, col in enumerate(columns):
        if 'flags' not in col or 'hidden' not in col.get('flags', []):
            visible_indexes.append(index)
            headers.append(col['name'].strip())

    rows = []
    for item in data['data']:
        row = {}
        for out_index, data_index in enumerate(visible_indexes):
            row[headers[out_index]] = item[data_index] if data_index < len(item) else ''
        rows.append({k: str(v).strip() if v is not None else '' for k, v in row.items()})
    return rows


def normalize_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def generate_prior_auth_record(index, source_row):
    approval_rate = normalize_float(source_row.get('Approval rate', ''))
    standard_time = normalize_float(source_row.get('Standard - Avg response time', ''))
    num_requests = normalize_float(source_row.get('Number of requests per code', ''))

    procedure_code = source_row.get('Code', '') or source_row.get('Procedure_Code', '')
    procedure_desc = source_row.get('Description of service', '') or source_row.get('Procedure_Description', '')
    service_category = source_row.get('Service category', '')

    diagnosis_code, diagnosis_desc = random.choice(DIAGNOSES)
    if 'Diabetes' in service_category:
        diagnosis_code, diagnosis_desc = 'E11', 'Type 2 Diabetes'
    elif 'Mental health' in service_category or 'substance use' in service_category.lower():
        diagnosis_code, diagnosis_desc = 'J45', 'Asthma'
    elif 'surgical' in service_category.lower():
        diagnosis_code, diagnosis_desc = 'M54', 'Back Pain'

    if num_requests is None or num_requests <= 0:
        procedure_cost = random.randint(500, 40000)
    else:
        procedure_cost = int(num_requests * random.uniform(200, 2000) + random.uniform(500, 5000))
        procedure_cost = max(500, min(procedure_cost, 50000))

    claim_amount_paid = int(procedure_cost * random.uniform(0.4, 0.95))
    turnaround_time = int(standard_time) if standard_time is not None and standard_time > 0 else random.randint(1, 80)

    approved_probability = 0.75 if approval_rate is None else approval_rate
    pa_status = 'Approved' if random.random() < approved_probability else 'Denied'

    return {
        'Patient_ID': f'P{index}',
        'Encounter_ID': f'E{index}',
        'Age': str(random.choices(AGE_VALUES, weights=AGE_WEIGHTS, k=1)[0]),
        'Gender': weighted_choice(GENDER_CHOICES),
        'Diagnosis_Code': diagnosis_code,
        'Diagnosis_Description': diagnosis_desc,
        'Procedure_Code': procedure_code,
        'Procedure_Description': procedure_desc,
        'Comorbidity_Count': str(sample_comorbidity_count()),
        'Procedure_Cost': str(procedure_cost),
        'Insurance_Type': weighted_choice(INSURANCE_CHOICES),
        'Provider_Type': random.choice(PROVIDER_TYPES),
        'Claim_Amount_Paid': str(claim_amount_paid),
        'Clinical_Notes': random.choice(CLINICAL_NOTES),
        'Severity_Level': weighted_choice(SEVERITY_CHOICES),
        'Urgency_Level': weighted_choice(URGENCY_CHOICES),
        'Condition_Type': weighted_choice(CONDITION_CHOICES),
        'PA_Status': pa_status,
        'Submission_Type': weighted_choice(SUBMISSION_CHOICES),
        'Turnaround_Time': str(turnaround_time),
        'Encounter_Date': random_date(date(2023, 1, 1), date(2024, 12, 31)).strftime('%d-%m-%Y'),
    }


def combine_sources(wa_rows, cms_rows):
    seen = set()
    combined = []

    for row in wa_rows + cms_rows:
        key = (
            row.get('Carrier', ''),
            row.get('Year', ''),
            row.get('Service category', ''),
            row.get('Request', ''),
            row.get('Code type', ''),
            row.get('Code', ''),
            row.get('Description of service', ''),
            row.get('Number of requests per code', ''),
        )
        if key not in seen:
            seen.add(key)
            combined.append(row)

    return combined


def write_prior_auth_dataset(records, output_path):
    with Path(output_path).open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=TARGET_HEADERS)
        writer.writeheader()
        writer.writerows(records)


def main():
    base_dir = Path(__file__).resolve().parent.parent / 'Data'
    raw_dir = base_dir / 'RawData'
    clean_dir = base_dir / 'Clean_data'
    clean_dir.mkdir(parents=True, exist_ok=True)

    wa_csv = raw_dir / 'wa_data.csv'
    cms_json = raw_dir / 'cms_data.txt'
    output_csv = clean_dir / 'prior_authorization_dataset_wa_cms.csv'

    wa_rows = parse_wa_csv(wa_csv) if wa_csv.exists() else []
    cms_rows = parse_cms_json(cms_json) if cms_json.exists() else []

    if not wa_rows and not cms_rows:
        raise FileNotFoundError('Neither wa_data.csv nor cms_data.txt were found.')

    combined_source_rows = combine_sources(wa_rows, cms_rows)
    prior_records = [generate_prior_auth_record(idx + 1, row) for idx, row in enumerate(combined_source_rows)]

    write_prior_auth_dataset(prior_records, output_csv)
    print(f'Generated {len(prior_records)} rows to {output_csv}')


if __name__ == '__main__':
    random.seed(42)
    main()
