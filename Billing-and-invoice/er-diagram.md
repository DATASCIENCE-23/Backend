```mermaid
erDiagram
    PATIENT ||--o{ INVOICE : receives
    INVOICE ||--|{ INVOICE_LINE_ITEM : contains
    SERVICE_MASTER ||--o{ INVOICE_LINE_ITEM : billed_as
    INVOICE ||--o{ PAYMENT : settled_by
    INSURANCE_PROVIDER ||--o{ INVOICE : covers

    PATIENT {
        int patient_id PK
        string full_name
        string contact_number
        string medical_record_number
    }

    INVOICE {
        int invoice_id PK
        int patient_id FK
        datetime issue_date
        string invoice_type "OPD/IPD"
        float total_tax
        float grand_total
        string status "Draft/Issued/Paid/Cancelled"
    }

    INVOICE_LINE_ITEM {
        int line_item_id PK
        int invoice_id FK
        int service_id FK
        string description
        int quantity
        float unit_price
        float line_total
    }

    SERVICE_MASTER {
        int service_id PK
        string service_name
        string category "Consultation/Lab/Room"
        float standard_price
    }

    PAYMENT {
        int payment_id PK
        int invoice_id FK
        datetime payment_date
        float amount_paid
        string payment_mode "Cash/Card/Online"
        string transaction_ref
    }

    INSURANCE_PROVIDER {
        int provider_id PK
        string company_name
        float coverage_limit
    }
