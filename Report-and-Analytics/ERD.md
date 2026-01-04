# Reports and Analytics Module – ER Diagram

This module serves as the central intelligence hub, aggregating data from Clinical, Pharmacy, Laboratory, and Financial modules to provide actionable insights.

## ER Diagram

```mermaid
erDiagram
    %% Analytical Entities
    ANALYTICAL_SNAPSHOT {
        int snapshot_id PK
        datetime captured_at
        string metric_type "Occupancy/Revenue/Clinical"
        decimal value
        string dimensions "Ward/Doctor/Location"
    }

    REPORT_TEMPLATE {
        int template_id PK
        string template_name "Patient_Medical_Summary"
        text layout_json
        string category "Clinical/Financial/Operational"
    }

    GENERATED_REPORT {
        int report_id PK
        int template_id FK
        int patient_id FK
        int generated_by_user_id FK
        datetime generated_at
        string file_path_url
    }

    %% Relationships to existing data modules
    PATIENT ||--o{ GENERATED_REPORT : "subject_of"
    REPORT_TEMPLATE ||--o{ GENERATED_REPORT : "defines_format"

    %% Implicit Data Source Relationships
    ADMISSION ||--o| ANALYTICAL_SNAPSHOT : "calculates_occupancy"
    INVOICE ||--o| ANALYTICAL_SNAPSHOT : "calculates_revenue"
    LAB_RESULT ||--o| GENERATED_REPORT : "populates_diagnostics"
    PRESCRIPTION_ITEM ||--o| GENERATED_REPORT : "populates_treatment"

```
