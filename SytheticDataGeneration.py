import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_synthetic_prior_auth(num_records=2000):
    # Setup for reproducibility
    random.seed(42)
    np.random.seed(42)

    # Reference mappings from your source data
    diagnoses = {
        'I10': 'Hypertension', 'M54': 'Back Pain', 
        'K21': 'GERD', 'E11': 'Type 2 Diabetes', 'J45': 'Asthma'
    }
    procedures = {
        'CT': 'CT', 'BT': 'Blood Test', 
        'XR': 'X-Ray', 'SR': 'Surgery', 'MR': 'MRI'
    }
    clinical_notes_pool = [
        "Stable condition, periodic evaluation needed",
        "Emergency case with acute complications",
        "Chronic disease, requires continuous monitoring",
        "Mild condition, routine follow-up recommended"
    ]
    
    insurance_types = ['Private', 'Medicaid', 'Medicare']
    provider_types = ['Hospital', 'Clinic']
    severity_levels = ['Medium', 'High', 'Low']
    urgency_levels = ['Urgent', 'Emergency', 'Routine']
    condition_types = ['Acute', 'Chronic']
    pa_statuses = ['Approved', 'Denied']
    submission_types = ['Manual', 'AI']

    data = []
    start_date = datetime(2023, 1, 1)
    date_range = 730  # 2 years

    for i in range(1, num_records + 1):
        p_id = f"P{i}"
        e_id = f"E{i}"
        age = random.randint(18, 90)
        gender = random.choice(['Female', 'Male'])
        
        diag_code = random.choice(list(diagnoses.keys()))
        diag_desc = diagnoses[diag_code]
        
        proc_code = random.choice(list(procedures.keys()))
        proc_desc = procedures[proc_code]
        
        procedure_cost = random.randint(500, 50000)
        # Typically insurance pays 50% to 90% of the cost
        claim_paid = int(procedure_cost * random.uniform(0.5, 0.9))
        
        # Assemble row
        data.append({
            'Patient_ID': p_id,
            'Encounter_ID': e_id,
            'Age': age,
            'Gender': gender,
            'Diagnosis_Code': diag_code,
            'Diagnosis_Description': diag_desc,
            'Procedure_Code': proc_code,
            'Procedure_Description': proc_desc,
            'Comorbidity_Count': random.randint(0, 4),
            'Procedure_Cost': procedure_cost,
            'Insurance_Type': random.choice(insurance_types),
            'Provider_Type': random.choice(provider_types),
            'Claim_Amount_Paid': claim_paid,
            'Clinical_Notes': random.choice(clinical_notes_pool),
            'Severity_Level': random.choice(severity_levels),
            'Urgency_Level': random.choice(urgency_levels),
            'Condition_Type': random.choice(condition_types),
            'PA_Status': np.random.choice(pa_statuses, p=[0.74, 0.26]), # 74% Approval rate
            'Submission_Type': random.choice(submission_types),
            'Turnaround_Time': random.randint(1, 72),
            'Encounter_Date': (start_date + timedelta(days=random.randint(0, date_range))).strftime('%d-%m-%Y')
        })

    return pd.DataFrame(data)

# Generate 2000 rows
synthetic_df = generate_synthetic_prior_auth(2000)

# Save to CSV
synthetic_df.to_csv('synthetic_prior_auth_data.csv', index=False)
print("Synthetic dataset created successfully.")
