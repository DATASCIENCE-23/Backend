```mermaid
erDiagram

PATIENT {
    int patient_id PK
    varchar first_name
    varchar last_name
    date date_of_birth
    enum gender
    varchar blood_group
    varchar phone_number
    varchar email
    text address
    varchar emergency_contact_name
    varchar emergency_contact_phone
    datetime registration_date
    boolean is_active
}

SPECIALIZATION {
    int specialization_id PK
    varchar specialization_name
    text description
    boolean is_active
}

DOCTOR {
    int doctor_id PK
    varchar first_name
    varchar last_name
    int specialization_id FK
    varchar qualification
    varchar license_number
    varchar phone_number
    varchar email
    int experience_years
    decimal consultation_fee
    date date_joined
    boolean is_active
}

DOCTOR_SCHEDULE {
    int schedule_id PK
    int doctor_id FK
    enum day_of_week
    time start_time
    time end_time
    int slot_duration
    int max_patients_per_slot
    boolean is_active
    date effective_from
    date effective_to
}

BLOCKED_SLOTS {
    int blocked_slot_id PK
    int doctor_id FK
    date blocked_date
    time start_time
    time end_time
    text reason
    datetime created_at
    int created_by
}

APPOINTMENT {
    int appointment_id PK
    int patient_id FK
    int doctor_id FK
    date appointment_date
    time start_time
    time end_time
    enum appointment_type
    enum status
    text reason_for_visit
    text symptoms
    text notes
    decimal consultation_fee
    datetime booking_date
    text cancellation_reason
    datetime cancelled_at
    enum cancelled_by
}

APPOINTMENT_REMINDER {
    int reminder_id PK
    int appointment_id FK
    enum reminder_type
    datetime reminder_time
    datetime sent_at
    enum status
    text message_content
}

APPOINTMENT_HISTORY {
    int history_id PK
    int appointment_id FK
    int changed_by
    enum change_type
    date old_date
    date new_date
    time old_time
    time new_time
    varchar old_status
    varchar new_status
    text change_reason
    datetime changed_at
}

WAITING_LIST {
    int waiting_id PK
    int patient_id FK
    int doctor_id FK
    date preferred_date
    time preferred_time_start
    time preferred_time_end
    text reason
    enum status
    datetime added_at
    datetime notified_at
    datetime expires_at
}

PATIENT ||--o{ APPOINTMENT : books
DOCTOR ||--o{ APPOINTMENT : attends
SPECIALIZATION ||--o{ DOCTOR : contains
DOCTOR ||--o{ DOCTOR_SCHEDULE : defines
DOCTOR ||--o{ BLOCKED_SLOTS : blocks
APPOINTMENT ||--o{ APPOINTMENT_REMINDER : triggers
APPOINTMENT ||--o{ APPOINTMENT_HISTORY : logs
PATIENT ||--o{ WAITING_LIST : joins
DOCTOR ||--o{ WAITING_LIST : manages