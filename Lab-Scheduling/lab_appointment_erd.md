erDiagram

LAB {
    int lab_id PK
    varchar lab_name
    varchar lab_code
    varchar phone_number
    varchar email
    text address
    boolean is_active
    datetime created_at
}

LAB_TECHNICIAN {
    int technician_id PK
    varchar first_name
    varchar last_name
    varchar license_number
    varchar phone_number
    varchar email
    boolean is_active
}

LAB_TEST {
    int test_id PK
    varchar test_name
    varchar test_code
    text description
    decimal test_cost
    boolean fasting_required
    int expected_duration_minutes
    boolean is_active
}

LAB_ORDER {
    int lab_order_id PK
    int patient_id FK
    int doctor_id FK
    int record_id FK
    date order_date
    enum priority
    enum status
    text clinical_notes
    datetime created_at
}

LAB_SCHEDULE {
    int schedule_id PK
    int lab_order_id FK
    int lab_id FK
    int technician_id FK
    date scheduled_date
    time start_time
    time end_time
    enum sample_type
    enum schedule_status
    boolean home_collection
    text notes
    datetime scheduled_at
}

LAB_RESULT {
    int result_id PK
    int lab_order_id FK
    int test_id FK
    date result_date
    text result_value
    text reference_range
    enum abnormal_flag
    text remarks
    datetime verified_at
}

LAB_REPORT {
    int lab_report_id PK
    int lab_order_id FK
    date report_date
    text summary
    varchar report_file_url
    enum status
}

PATIENT ||--o{ LAB_ORDER : requests
DOCTOR ||--o{ LAB_ORDER : orders
MEDICAL_RECORD ||--o{ LAB_ORDER : generates

LAB_ORDER ||--o{ LAB_SCHEDULE : scheduled_as
LAB ||--o{ LAB_SCHEDULE : provides
LAB_TECHNICIAN ||--o{ LAB_SCHEDULE : handles

LAB_ORDER ||--o{ LAB_RESULT : produces
LAB_TEST ||--o{ LAB_RESULT : referenced_in

LAB_ORDER ||--|| LAB_REPORT : summarized_as
