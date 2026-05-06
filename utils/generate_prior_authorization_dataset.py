import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path


DIAGNOSES = [
    ('M54', 'Back Pain'),
    ('K21', 'GERD'),
    ('J45', 'Asthma'),
    ('E11', 'Type 2 Diabetes'),
    ('I10', 'Hypertension'),
]

PROCEDURES = [
    ('CT', 'CT', 1000, 45000),
    ('Blood Test', 'Blood Test', 500, 25000),
    ('X-Ray', 'X-Ray', 800, 35000),
    ('Surgery', 'Surgery', 10000, 48000),
    ('MRI', 'MRI', 5000, 47000),
]

GENDER_WEIGHTS = [('Female', 0.511), ('Male', 0.489)]
INSURANCE_WEIGHTS = [('Private', 0.349), ('Medicaid', 0.343), ('Medicare', 0.308)]
SEVERITY_WEIGHTS = [('Medium', 0.416), ('High', 0.389), ('Low', 0.195)]
URGENCY_WEIGHTS = [('Urgent', 0.61), ('Emergency', 0.196), ('Routine', 0.194)]
PA_STATUS_WEIGHTS = [('Approved', 0.739), ('Denied', 0.261)]
SUBMISSION_WEIGHTS = [('Manual', 0.516), ('AI', 0.484)]
CONDITION_WEIGHTS = [('Acute', 0.782), ('Chronic', 0.218)]

CLINICAL_NOTES = [
    'Chronic disease, requires continuous monitoring',
    'Stable condition, periodic evaluation needed',
    'Emergency case with acute complications',
    'Mild condition, routine follow-up recommended',
    'Patient shows severe symptoms and requires immediate attention',
]

AGE_VALUES = list(range(19, 89))
AGE_WEIGHTS = [1.0 for _ in AGE_VALUES]

COMORBIDITY_DISTRIBUTION = [(0, 0.05), (1, 0.15), (2, 0.35), (3, 0.30), (4, 0.15)]

FIELDNAMES = [
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

PROVIDER_TYPES = ['Hospital', 'Clinic']


def weighted_choice(options):
    choices, weights = zip(*options)
    return random.choices(choices, weights=weights, k=1)[0]


def random_date(start_date, end_date):
    delta = end_date - start_date
    return start_date + timedelta(days=random.randint(0, delta.days))


def sample_comorbidity_count():
    values, weights = zip(*COMORBIDITY_DISTRIBUTION)
    return random.choices(values, weights=weights, k=1)[0]


def generate_row(index):
    diagnosis_code, diagnosis_desc = weighted_choice([
        (code, 1.0) for code, _ in DIAGNOSES
    ]), None
    # map selected diagnosis code to description
    diagnosis_desc = next(desc for code, desc in DIAGNOSES if code == diagnosis_code)

    procedure_code, procedure_desc, low_cost, high_cost = random.choice(PROCEDURES)
    procedure_cost = random.randint(low_cost, high_cost)
    claim_amount_paid = int(procedure_cost * random.uniform(0.4, 0.95))

    age = random.choices(AGE_VALUES, weights=AGE_WEIGHTS, k=1)[0]
    gender = weighted_choice(GENDER_WEIGHTS)
    insurance = weighted_choice(INSURANCE_WEIGHTS)
    severity = weighted_choice(SEVERITY_WEIGHTS)
    urgency = weighted_choice(URGENCY_WEIGHTS)
    pa_status = weighted_choice(PA_STATUS_WEIGHTS)
    submission = weighted_choice(SUBMISSION_WEIGHTS)
    condition = weighted_choice(CONDITION_WEIGHTS)
    comorbidity = sample_comorbidity_count()
    provider_type = random.choice(PROVIDER_TYPES)
    turnaround_time = random.randint(1, 80)
    encounter_date = random_date(date(2023, 1, 1), date(2024, 12, 31)).strftime('%d-%m-%Y')
    clinical_note = random.choice(CLINICAL_NOTES)

    return {
        'Patient_ID': f'P{index}',
        'Encounter_ID': f'E{index}',
        'Age': str(age),
        'Gender': gender,
        'Diagnosis_Code': diagnosis_code,
        'Diagnosis_Description': diagnosis_desc,
        'Procedure_Code': procedure_code,
        'Procedure_Description': procedure_desc,
        'Comorbidity_Count': str(comorbidity),
        'Procedure_Cost': str(procedure_cost),
        'Insurance_Type': insurance,
        'Provider_Type': provider_type,
        'Claim_Amount_Paid': str(claim_amount_paid),
        'Clinical_Notes': clinical_note,
        'Severity_Level': severity,
        'Urgency_Level': urgency,
        'Condition_Type': condition,
        'PA_Status': pa_status,
        'Submission_Type': submission,
        'Turnaround_Time': str(turnaround_time),
        'Encounter_Date': encounter_date,
    }


def generate_dataset(record_count, output_path, seed=42):
    random.seed(seed)
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    with output_file.open('w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for idx in range(1, record_count + 1):
            writer.writerow(generate_row(idx))

    print(f'Generated {record_count} synthetic records to {output_path}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate a synthetic prior authorization dataset with a schema similar to prior_authorization_dataset_2000.csv.'
    )
    parser.add_argument('--records', '-n', type=int, default=2200, help='Number of records to generate.')
    parser.add_argument('--output', '-o', default='Data/prior_authorization_dataset_2000.csv', help='Output CSV file path.')
    parser.add_argument('--seed', '-s', type=int, default=42, help='Random seed for reproducibility.')
    args = parser.parse_args()

    generate_dataset(args.records, args.output, seed=args.seed)
