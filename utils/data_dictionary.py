"""
Data Dictionary for Prior Authorization Automation
Defines the standard schema across all data sources
"""

# Standard headers based on the data description
STANDARD_HEADERS = [
    # Beneficiary/Patient identifiers and demographics
    "beneficiary_id",
    "age",
    "sex",
    "gender",
    "race_ethnicity",
    
    # Insurance and enrollment
    "HMO_months",
    "insurance_type",
    
    # Chronic condition flags
    "diabetes_flag",
    "CHF_flag",
    "CKD_flag",
    "COPD_flag",
    "cancer_flag",
    
    # Medical reimbursement data
    "medreimb_IP",
    "medreimb_OP",
    "medreimb_CAR",
    "total_annual_cost",
    
    # Prior authorization labels
    "PA_prone_user",
    "high_cost_user",
    
    # Clinical/ICU data
    "apacheadmissiondx",
    "unittype",
    "unitadmitsource",
    "LOS_ICU",
    "hospitaldischargelocation",
    "hospitaldischargestatus",
    "clinical_text",
    "search_query",
    
    # Prior authorization requests (WA OIC dataset)
    "carrier",
    "year",
    "service_category",
    "service_code",
    "total_PA_requests",
    "approval_rate",
    "mean_decision_time_standard",
]

# Column mapping from source CSV files to standard headers
COLUMN_MAPPING = {
    "cms_chunk_1.csv": {
        "Carrier": "carrier",
        "Year": "year",
        "Service category": "service_category",
        "Code": "service_code",
        "Number of requests per code": "total_PA_requests",
        "Approval rate": "approval_rate",
        "Standard - Avg response time": "mean_decision_time_standard",
    },
    "EHR_Dataset.csv": {
        "gender": "gender",
        "age": "age",
        "ethnicity": "race_ethnicity",
        "apacheadmissiondx": "apacheadmissiondx",
        "unittype": "unittype",
        "unitadmitsource": "unitadmitsource",
        "hospitaldischargelocation": "hospitaldischargelocation",
        "hospitaldischargestatus": "hospitaldischargestatus",
        "clinical_text": "clinical_text",
        "search_query": "search_query",
    },
    "prior_authorization_dataset_2000.csv": {
        "Patient_ID": "beneficiary_id",
        "Age": "age",
        "Gender": "gender",
        "Insurance_Type": "insurance_type",
        "Severity_Level": "severity_level",
        "Urgency_Level": "urgency_level",
        "PA_Status": "PA_status",
        "Turnaround_Time": "turnaround_time",
        "Clinical_Notes": "clinical_text",
    },
}

if __name__ == "__main__":
    print("Standard Headers:")
    for i, header in enumerate(STANDARD_HEADERS, 1):
        print(f"{i:2d}. {header}")
    print(f"\nTotal headers: {len(STANDARD_HEADERS)}")
