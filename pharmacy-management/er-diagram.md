# Hospital Pharmacy Module – ER Diagram

PATIENT {
    int patient_id PK
    string hospital_id
    string name
    string gender
    date date_of_birth
    string phone
}

DOCTOR {
    int doctor_id PK
    string name
    string specialization
}

PHARMACIST {
    int pharmacist_id PK
    string name
    string employee_code
}

MEDICINE {
    int medicine_id PK
    string name
    string generic_name
    string strength
    string form
    string shelf_location
    decimal unit_price
    boolean is_active
    int min_quantity
}

MEDICINE_BATCH {
    int batch_id PK
    int medicine_id FK
    string batch_number
    int quantity_in_stock
    date manufacture_date
    date expiry_date
}

PRESCRIPTION {
    int prescription_id PK
    int patient_id FK
    int doctor_id FK
    datetime created_at
    string status        // Pending, Completed, Partially_Completed
    string source        // e.g. "DOCTOR_MODULE_API"
}

PRESCRIPTION_ITEM {
    int prescription_item_id PK
    int prescription_id FK
    int medicine_id FK
    int prescribed_quantity
    string dosage_instructions
}

DISPENSE {
    int dispense_id PK
    int prescription_id FK
    int pharmacist_id FK
    datetime dispensed_at
    decimal total_amount
    boolean is_billed
}

DISPENSE_ITEM {
    int dispense_item_id PK
    int dispense_id FK
    int medicine_id FK
    int batch_id FK
    int dispensed_quantity
    decimal unit_price_at_time
    decimal line_total
}

AUDIT_LOG {
    int audit_id PK
    string entity_name
    int entity_id
    string action      // CREATE, UPDATE, DISPENSE
    int performed_by   // user id (pharmacist/doctor/etc.)
    datetime performed_at
    string details
}

PATIENT ||--o{ PRESCRIPTION : "has"
DOCTOR ||--o{ PRESCRIPTION : "creates"
PRESCRIPTION ||--|{ PRESCRIPTION_ITEM : "contains"
MEDICINE ||--o{ PRESCRIPTION_ITEM : "is prescribed as"
MEDICINE ||--o{ MEDICINE_BATCH : "has batches"
PRESCRIPTION ||--o{ DISPENSE : "is fulfilled by"
PHARMACIST ||--o{ DISPENSE : "performs"
DISPENSE ||--|{ DISPENSE_ITEM : "includes"
MEDICINE_BATCH ||--o{ DISPENSE_ITEM : "taken from"
MEDICINE ||--o{ DISPENSE_ITEM : "dispensed as"

PRESCRIPTION ||--o{ AUDIT_LOG : "changes logged"
DISPENSE ||--o{ AUDIT_LOG : "changes logged"
MEDICINE ||--o{ AUDIT_LOG : "changes logged"