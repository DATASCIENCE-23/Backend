```mermaid
erDiagram
    %% ========================================
    %% PATIENT REGISTRATION & MANAGEMENT
    %% ========================================
    PATIENT {
        int patient_id PK
        string hospital_id UK
        string first_name
        string last_name
        date date_of_birth
        enum gender
        string blood_group
        string phone_number
        string email
        string marital_status
        string emergency_contact_name
        string emergency_contact_phone
        datetime registration_date
        string patient_type
        string medical_record_number UK
        int user_id FK
        boolean is_active
    }
    
    ADDRESS {
        int address_id PK
        int patient_id FK
        string street
        string city
        string state
        string pincode
        string country
    }
    
    INSURANCE_PROVIDER {
        int provider_id PK
        string company_name
        string contact_person
        string phone_number
        string email
        text address
        float coverage_limit
        boolean is_active
    }
    
    INSURANCE {
        int insurance_id PK
        int patient_id FK
        int provider_id FK
        string policy_number UK
        string coverage_type
        float coverage_percent
        date valid_from
        date valid_to
        boolean is_active
    }
    
    %% ========================================
    %% USER MANAGEMENT & AUTHENTICATION
    %% ========================================
    USER {
        int user_id PK
        string username UK
        string password_hash
        string email UK
        string full_name
        string status
        int department_id FK
        datetime created_at
        datetime last_login
    }
    
    ROLE {
        int role_id PK
        string role_name UK
        text description
    }
    
    USER_ROLE {
        int user_role_id PK
        int user_id FK
        int role_id FK
        date assigned_date
    }
    
    AUDIT_LOG {
        int log_id PK
        int user_id FK
        string entity_name
        int entity_id
        datetime action_time
        string action_type
        string ip_address
        text details
    }
    
    %% ========================================
    %% DOCTOR & SPECIALIZATION
    %% ========================================
    SPECIALIZATION {
        int specialization_id PK
        string specialization_name UK
        text description
        boolean is_active
    }
    
    DOCTOR {
        int doctor_id PK
        int user_id FK
        string first_name
        string last_name
        int specialization_id FK
        string qualification
        string license_number UK
        string phone_number
        string email
        int experience_years
        decimal consultation_fee
        date date_joined
        date date_of_birth
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
        int created_by FK
    }
    
    %% ========================================
    %% APPOINTMENT MANAGEMENT
    %% ========================================
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
        int cancelled_by FK
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
        int changed_by FK
        enum change_type
        date old_date
        date new_date
        time old_time
        time new_time
        string old_status
        string new_status
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
    
    %% ========================================
    %% VISIT & ADMISSION
    %% ========================================
    VISIT {
        int visit_id PK
        int patient_id FK
        int doctor_id FK
        enum visit_type
        datetime visit_datetime
        text chief_complaint
        enum status
        datetime created_at
    }
    
    ADMISSION {
        int admission_id PK
        int visit_id FK
        datetime admission_datetime
        datetime discharge_datetime
        int ward_id FK
        string bed_number
        text admission_reason
        text discharge_summary
        enum status
    }
    
    WARD {
        int ward_id PK
        string ward_name
        string ward_type
        int total_beds
        int available_beds
        boolean is_active
    }
    
    %% ========================================
    %% MEDICAL RECORDS & CLINICAL DATA
    %% ========================================
    MEDICAL_RECORD {
        int record_id PK
        int patient_id FK
        int doctor_id FK
        int visit_id FK
        datetime record_date
        text chief_complaint
        text history_of_present_illness
        text past_medical_history
        text physical_examination
        text diagnosis
        text treatment_plan
        text notes
    }
    
    PRESCRIPTION {
        int prescription_id PK
        int record_id FK
        int patient_id FK
        int doctor_id FK
        datetime created_at
        enum status
        text notes
    }
    
    PRESCRIPTION_ITEM {
        int prescription_item_id PK
        int prescription_id FK
        int medicine_id FK
        int prescribed_quantity
        string dosage
        string frequency
        int duration_days
        text instructions
    }
    
    REPORT {
        int report_id PK
        int record_id FK
        string report_type
        date report_date
        text findings
        string file_url
    }
    
    %% ========================================
    %% LABORATORY MANAGEMENT
    %% ========================================
    LAB {
        int lab_id PK
        string lab_name UK
        string lab_code UK
        string phone_number
        string email
        text address
        boolean is_active
        datetime created_at
    }
    
    LAB_TECHNICIAN {
        int technician_id PK
        int user_id FK
        string first_name
        string last_name
        string license_number UK
        string phone_number
        string email
        boolean is_active
    }
    
    LAB_TEST {
        int test_id PK
        string test_name
        string test_code UK
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
        datetime order_datetime
        enum priority
        enum status
        text clinical_notes
    }
    
    LAB_ORDER_TEST {
        int lab_order_test_id PK
        int lab_order_id FK
        int test_id FK
        enum status
    }
    
    LAB_SCHEDULE {
        int schedule_id PK
        int lab_order_id FK
        int lab_id FK
        int technician_id FK
        datetime scheduled_datetime
        time expected_duration
        enum sample_type
        enum schedule_status
        boolean home_collection
        text notes
    }
    
    LAB_RESULT {
        int result_id PK
        int lab_order_test_id FK
        datetime result_datetime
        text result_value
        text reference_range
        enum abnormal_flag
        text remarks
        int verified_by FK
        datetime verified_at
    }
    
    LAB_REPORT {
        int lab_report_id PK
        int lab_order_id FK
        datetime report_datetime
        text summary
        string report_file_url
        enum status
        int prepared_by FK
    }
    
    %% ========================================
    %% PHARMACY MANAGEMENT
    %% ========================================
    PHARMACIST {
        int pharmacist_id PK
        int user_id FK
        string first_name
        string last_name
        string employee_code UK
        string license_number UK
        string phone_number
        string email
        boolean is_active
    }
    
    MEDICINE {
        int medicine_id PK
        string medicine_name
        string generic_name
        string strength
        string form
        string shelf_location
        decimal unit_price
        boolean is_active
        int min_quantity
        int reorder_level
    }
    
    MEDICINE_BATCH {
        int batch_id PK
        int medicine_id FK
        string batch_number UK
        int quantity_in_stock
        date manufacture_date
        date expiry_date
        decimal purchase_price
        boolean is_active
    }
    
    DISPENSE {
        int dispense_id PK
        int prescription_id FK
        int pharmacist_id FK
        datetime dispensed_at
        decimal total_amount
        enum status
        int invoice_id FK
    }
    
    DISPENSE_ITEM {
        int dispense_item_id PK
        int dispense_id FK
        int prescription_item_id FK
        int batch_id FK
        int dispensed_quantity
        decimal unit_price
        decimal line_total
    }
    
    %% ========================================
    %% BILLING & INVOICING
    %% ========================================
    SERVICE_MASTER {
        int service_id PK
        string service_code UK
        string service_name
        string category
        decimal standard_price
        int tax_id FK
        boolean is_active
    }
    
    INVOICE {
        int invoice_id PK
        int patient_id FK
        datetime issue_datetime
        string invoice_type
        decimal subtotal
        decimal tax_amount
        decimal discount_amount
        decimal grand_total
        enum status
        int created_by FK
    }
    
    INVOICE_LINE_ITEM {
        int line_item_id PK
        int invoice_id FK
        int service_id FK
        string description
        int quantity
        decimal unit_price
        decimal line_subtotal
        decimal tax_amount
        decimal line_total
    }
    
    PAYMENT {
        int payment_id PK
        int invoice_id FK
        datetime payment_datetime
        decimal amount_paid
        string payment_mode
        string transaction_ref
        int bank_account_id FK
        int received_by FK
        enum status
    }
    
    %% ========================================
    %% VENDOR & PROCUREMENT
    %% ========================================
    VENDOR {
        int vendor_id PK
        string vendor_name
        string vendor_code UK
        string contact_person
        string phone_number
        string email
        string gst_number
        text address
        boolean is_active
    }
    
    BILL {
        int bill_id PK
        int vendor_id FK
        date bill_date
        string bill_number UK
        decimal subtotal
        decimal tax_amount
        decimal grand_total
        enum status
        date due_date
    }
    
    BILL_LINE {
        int bill_line_id PK
        int bill_id FK
        int expense_account_id FK
        text description
        int quantity
        decimal unit_price
        decimal line_total
    }
    
    BILL_PAYMENT {
        int bill_payment_id PK
        int bill_id FK
        datetime payment_datetime
        decimal amount_paid
        string payment_mode
        string transaction_ref
        int paid_by FK
    }
    
    %% ========================================
    %% INVENTORY MANAGEMENT
    %% ========================================
    DEPARTMENT {
        int department_id PK
        string department_name UK
        string department_code UK
        string floor
        boolean is_active
    }
    
    CATEGORY {
        int category_id PK
        string category_name UK
        text description
    }
    
    ITEM {
        int item_id PK
        string item_code UK
        string item_name
        string unit
        decimal unit_price
        boolean expiry_applicable
        int minimum_stock_level
        int reorder_level
        int category_id FK
        enum status
    }
    
    SUPPLIER {
        int supplier_id PK
        string supplier_name
        string supplier_code UK
        string contact_person
        string phone_number
        string email
        text address
        boolean is_active
    }
    
    STORE_LOCATION {
        int location_id PK
        string location_name UK
        string location_code UK
        string location_type
        boolean is_active
    }
    
    STOCK {
        int stock_id PK
        int item_id FK
        int location_id FK
        int quantity_available
        int reserved_quantity
        datetime last_updated
    }
    
    PURCHASE_ORDER {
        int purchase_id PK
        string po_number UK
        date order_date
        int supplier_id FK
        decimal total_amount
        enum status
        int created_by FK
        date expected_delivery_date
    }
    
    PURCHASE_ORDER_ITEM {
        int po_item_id PK
        int purchase_id FK
        int item_id FK
        int ordered_quantity
        int received_quantity
        decimal unit_price
        decimal line_total
        date expiry_date
    }
    
    GOODS_RECEIPT {
        int receipt_id PK
        int purchase_id FK
        string grn_number UK
        date receipt_date
        int received_by FK
        text notes
    }
    
    ISSUE_REQUEST {
        int request_id PK
        string request_number UK
        int department_id FK
        datetime request_datetime
        enum status
        int requested_by FK
        int approved_by FK
    }
    
    ISSUE_DETAILS {
        int issue_detail_id PK
        int request_id FK
        int item_id FK
        int requested_quantity
        int issued_quantity
        datetime issued_datetime
        int issued_by FK
    }
    
    STOCK_TRANSFER {
        int transfer_id PK
        string transfer_number UK
        int item_id FK
        int from_location_id FK
        int to_location_id FK
        int quantity
        datetime transfer_datetime
        int initiated_by FK
        int approved_by FK
        enum status
    }
    
    STOCK_ADJUSTMENT {
        int adjustment_id PK
        string adjustment_number UK
        int item_id FK
        int location_id FK
        string adjustment_type
        int quantity_before
        int quantity_after
        int quantity_changed
        text reason
        datetime adjustment_datetime
        int adjusted_by FK
    }
    
    STOCK_AUDIT {
        int audit_id PK
        string audit_number UK
        int location_id FK
        date audit_date
        text remarks
        int conducted_by FK
        enum status
    }
    
    STOCK_AUDIT_DETAILS {
        int audit_detail_id PK
        int audit_id FK
        int item_id FK
        int system_quantity
        int physical_quantity
        int difference
        text remarks
    }
    
    %% ========================================
    %% ACCOUNTING & FINANCE
    %% ========================================
    ACCOUNT {
        int account_id PK
        string account_code UK
        string account_name
        string account_type
        int parent_account_id FK
        boolean is_active
    }
    
    JOURNAL_ENTRY {
        int journal_id PK
        string journal_number UK
        date journal_date
        string reference_type
        int reference_id
        text description
        boolean posted_status
        int created_by FK
        datetime created_at
    }
    
    JOURNAL_LINE {
        int journal_line_id PK
        int journal_id FK
        int account_id FK
        decimal debit_amount
        decimal credit_amount
        text description
    }
    
    EXPENSE {
        int expense_id PK
        string expense_number UK
        date expense_date
        int account_id FK
        decimal amount
        int department_id FK
        text description
        int reference_id
        int created_by FK
    }
    
    ASSET {
        int asset_id PK
        string asset_code UK
        string asset_name
        int account_id FK
        date purchase_date
        decimal purchase_cost
        int useful_life_years
        decimal salvage_value
        decimal accumulated_depreciation
        enum status
    }
    
    DEPRECIATION {
        int depreciation_id PK
        int asset_id FK
        date depreciation_date
        decimal depreciation_amount
        decimal book_value
        int journal_id FK
    }
    
    TAX {
        int tax_id PK
        string tax_code UK
        string tax_name
        decimal tax_rate
        int account_id FK
        boolean is_active
    }
    
    BUDGET {
        int budget_id PK
        string financial_year
        int department_id FK
        decimal total_amount
        enum status
        int created_by FK
    }
    
    BUDGET_LINE {
        int budget_line_id PK
        int budget_id FK
        int account_id FK
        decimal allocated_amount
        decimal spent_amount
        decimal remaining_amount
    }
    
    BANK_ACCOUNT {
        int bank_account_id PK
        string account_number UK
        string bank_name
        string branch_name
        int account_id FK
        decimal current_balance
        boolean is_active
    }
    
    %% ========================================
    %% RELATIONSHIPS
    %% ========================================
    
    %% Patient Relationships
    PATIENT ||--o{ ADDRESS : "has"
    PATIENT ||--o{ INSURANCE : "has"
    INSURANCE_PROVIDER ||--o{ INSURANCE : "provides"
    PATIENT ||--o{ APPOINTMENT : "books"
    PATIENT ||--o{ WAITING_LIST : "joins"
    PATIENT ||--o{ VISIT : "has"
    PATIENT ||--o{ MEDICAL_RECORD : "owns"
    PATIENT ||--o{ INVOICE : "receives"
    PATIENT ||--o{ LAB_ORDER : "requests"
    PATIENT ||--o{ PRESCRIPTION : "receives"
    
    %% User & Role Relationships
    USER ||--o{ USER_ROLE : "assigned"
    ROLE ||--o{ USER_ROLE : "includes"
    USER ||--o| DOCTOR : "is"
    USER ||--o| PATIENT : "is"
    USER ||--o| PHARMACIST : "is"
    USER ||--o| LAB_TECHNICIAN : "is"
    USER ||--o{ AUDIT_LOG : "generates"
    DEPARTMENT ||--o{ USER : "employs"
    
    %% Doctor Relationships
    SPECIALIZATION ||--o{ DOCTOR : "categorizes"
    DOCTOR ||--o{ DOCTOR_SCHEDULE : "defines"
    DOCTOR ||--o{ BLOCKED_SLOTS : "blocks"
    USER ||--o{ BLOCKED_SLOTS : "creates"
    DOCTOR ||--o{ APPOINTMENT : "attends"
    DOCTOR ||--o{ WAITING_LIST : "manages"
    DOCTOR ||--o{ VISIT : "conducts"
    DOCTOR ||--o{ MEDICAL_RECORD : "creates"
    DOCTOR ||--o{ LAB_ORDER : "orders"
    DOCTOR ||--o{ PRESCRIPTION : "writes"
    
    %% Appointment Relationships
    APPOINTMENT ||--o{ APPOINTMENT_REMINDER : "triggers"
    APPOINTMENT ||--o{ APPOINTMENT_HISTORY : "logs"
    USER ||--o{ APPOINTMENT_HISTORY : "makes"
    
    %% Visit & Admission
    VISIT ||--o| ADMISSION : "leads_to"
    WARD ||--o{ ADMISSION : "accommodates"
    VISIT ||--o{ MEDICAL_RECORD : "documented_in"
    
    %% Medical Records
    MEDICAL_RECORD ||--o{ PRESCRIPTION : "generates"
    MEDICAL_RECORD ||--o{ REPORT : "contains"
    MEDICAL_RECORD ||--o{ LAB_ORDER : "triggers"
    
    %% Prescription & Pharmacy
    PRESCRIPTION ||--o{ PRESCRIPTION_ITEM : "contains"
    MEDICINE ||--o{ PRESCRIPTION_ITEM : "prescribed_as"
    PRESCRIPTION ||--o{ DISPENSE : "fulfilled_by"
    MEDICINE ||--o{ MEDICINE_BATCH : "batched_as"
    PHARMACIST ||--o{ DISPENSE : "performs"
    DISPENSE ||--o{ DISPENSE_ITEM : "includes"
    PRESCRIPTION_ITEM ||--o{ DISPENSE_ITEM : "fulfilled_as"
    MEDICINE_BATCH ||--o{ DISPENSE_ITEM : "sourced_from"
    
    %% Laboratory Relationships
    LAB_ORDER ||--o{ LAB_ORDER_TEST : "includes"
    LAB_TEST ||--o{ LAB_ORDER_TEST : "ordered_as"
    LAB_ORDER ||--o| LAB_SCHEDULE : "scheduled_as"
    LAB ||--o{ LAB_SCHEDULE : "hosts"
    LAB_TECHNICIAN ||--o{ LAB_SCHEDULE : "performs"
    LAB_ORDER_TEST ||--o| LAB_RESULT : "produces"
    USER ||--o{ LAB_RESULT : "verifies"
    LAB_ORDER ||--o| LAB_REPORT : "summarized_in"
    USER ||--o{ LAB_REPORT : "prepares"
    
    %% Billing & Invoice
    INVOICE ||--o{ INVOICE_LINE_ITEM : "contains"
    SERVICE_MASTER ||--o{ INVOICE_LINE_ITEM : "billed_as"
    TAX ||--o{ SERVICE_MASTER : "applies_to"
    INVOICE ||--o{ PAYMENT : "settled_by"
    USER ||--o{ INVOICE : "creates"
    USER ||--o{ PAYMENT : "receives"
    BANK_ACCOUNT ||--o{ PAYMENT : "credited_to"
    DISPENSE ||--o| INVOICE : "billed_as"
    INVOICE ||--o| JOURNAL_ENTRY : "generates"
    PAYMENT ||--o| JOURNAL_ENTRY : "posts"
    
    %% Vendor & Bills
    VENDOR ||--o{ BILL : "submits"
    BILL ||--o{ BILL_LINE : "contains"
    ACCOUNT ||--o{ BILL_LINE : "charged_to"
    BILL ||--o{ BILL_PAYMENT : "settled_by"
    USER ||--o{ BILL_PAYMENT : "makes"
    BILL ||--o| JOURNAL_ENTRY : "recorded_as"
    BILL_PAYMENT ||--o| JOURNAL_ENTRY : "posts"
    
    %% Inventory Relationships
    CATEGORY ||--o{ ITEM : "categorizes"
    ITEM ||--o{ STOCK : "tracked_in"
    STORE_LOCATION ||--o{ STOCK : "stores"
    SUPPLIER ||--o{ PURCHASE_ORDER : "receives"
    USER ||--o{ PURCHASE_ORDER : "creates"
    PURCHASE_ORDER ||--o{ PURCHASE_ORDER_ITEM : "contains"
    ITEM ||--o{ PURCHASE_ORDER_ITEM : "ordered_as"
    PURCHASE_ORDER ||--o{ GOODS_RECEIPT : "received_as"
    USER ||--o{ GOODS_RECEIPT : "receives"
    DEPARTMENT ||--o{ ISSUE_REQUEST : "raises"
    USER ||--o{ ISSUE_REQUEST : "requests"
    USER ||--o{ ISSUE_REQUEST : "approves"
    ISSUE_REQUEST ||--o{ ISSUE_DETAILS : "contains"
    ITEM ||--o{ ISSUE_DETAILS : "issued_as"
    USER ||--o{ ISSUE_DETAILS : "issues"
    STORE_LOCATION ||--o{ STOCK_TRANSFER : "from"
    STORE_LOCATION ||--o{ STOCK_TRANSFER : "to"
    ITEM ||--o{ STOCK_TRANSFER : "transferred"
    USER ||--o{ STOCK_TRANSFER : "initiates"
    USER ||--o{ STOCK_TRANSFER : "approves"
    ITEM ||--o{ STOCK_ADJUSTMENT : "adjusted"
    STORE_LOCATION ||--o{ STOCK_ADJUSTMENT : "location"
    USER ||--o{ STOCK_ADJUSTMENT : "performs"
    STORE_LOCATION ||--o{ STOCK_AUDIT : "audited"
    USER ||--o{ STOCK_AUDIT : "conducts"
    STOCK_AUDIT ||--o{ STOCK_AUDIT_DETAILS : "records"
    ITEM ||--o{ STOCK_AUDIT_DETAILS : "counted"
    
    %% Accounting Relationships
    ACCOUNT ||--o{ ACCOUNT : "has_parent"
    ACCOUNT ||--o{ JOURNAL_LINE : "records"
    JOURNAL_ENTRY ||--o{ JOURNAL_LINE : "contains"
    USER ||--o{ JOURNAL_ENTRY : "creates"
    ACCOUNT ||--o{ EXPENSE : "categorizes"
    DEPARTMENT ||--o{ EXPENSE : "incurs"
    USER ||--o{ EXPENSE : "records"
    ACCOUNT ||--o{ ASSET : "tracks"
    ASSET ||--o{ DEPRECIATION : "depreciates"
    DEPRECIATION ||--o{ JOURNAL_ENTRY : "posts"
    ACCOUNT ||--o{ TAX : "applies"
    DEPARTMENT ||--o{ BUDGET : "allocated_to"
    USER ||--o{ BUDGET : "prepares"
    BUDGET ||--o{ BUDGET_LINE : "contains"
    ACCOUNT ||--o{ BUDGET_LINE : "allocated_for"
    ACCOUNT ||--o{ BANK_ACCOUNT : "links_to"
```
