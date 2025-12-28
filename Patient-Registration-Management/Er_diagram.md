erDiagram

    PATIENT {
        int patient_id PK
        string first_name
        string last_name
        date dob
        string gender
        string blood_group
        string phone
        string email
        string marital_status
        string emergency_contact_name
        string emergency_contact_phone
        date registration_date
        string patient_type
    }

    ADDRESS {
        int address_id PK
        string street
        string city
        string state
        string pincode
        string country
        int patient_id FK
    }

    VISIT {
        int visit_id PK
        int patient_id FK
        int doctor_id FK
        string visit_type
        date visit_date
        string reason_for_visit
        string status
    }

    ADMISSION {
        int admission_id PK
        int visit_id FK
        date admission_date
        date discharge_date
        string ward
        string bed_number
        string admission_reason
        string status
    }

    DOCTOR {
        int doctor_id PK
        string name
        string specialization
        string department
        string phone
        string email
        date doj
        date dob
        string status
    }

    INSURANCE {
        int insurance_id PK
        int patient_id FK
        string provider_name
        string policy_number
        string coverage_type
        date valid_from
        date valid_to
    }

    PATIENT ||--o{ ADDRESS : has
    PATIENT ||--o{ VISIT : has
    DOCTOR ||--o{ VISIT : attends
    VISIT ||--o| ADMISSION : results_in
    PATIENT ||--o{ INSURANCE : has
