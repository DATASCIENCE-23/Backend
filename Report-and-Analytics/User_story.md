### User Story: Comprehensive Patient Journey & Analytical Insights

**As a** Hospital Administrator or Senior Clinician,
**I want to** access a centralized reporting dashboard that aggregates demographic, clinical, and financial data into both high-level analytics and detailed individual patient reports,
**So that** I can optimize hospital resources, monitor public health trends, and review a patient's entire medical and financial history in one .

---

### Scenarios

#### 1. Strategic Patient Analytics

- **The System shall** generate demographic reports by analyzing patient volume, age, and location from the **PATIENT** and **ADDRESS** tables to guide community outreach.
- **The System shall** calculate **Average Length of Stay (ALOS)** and real-time bed occupancy by processing `admission_date` and `discharge_date` from the **ADMISSION** table.
- **The System shall** track clinical trends (such as "Flu trends") and treatment effectiveness by aggregating **VISIT** reasons and **LAB_RESULT** data.

#### 2. Financial & Billing Intelligence

- **The System shall** provide a financial health summary by tracking outstanding debts and revenue cycles using the **INVOICE** and **PAYMENT** tables.
- **The System shall** identify insurance claim trends by analyzing the `status` of invoices linked to **INSURANCE_PROVIDER** data.

#### 3. Individual Patient Medical Report

- **The System shall** allow users to scroll through a patient list and select a specific record to view a unified report.
- **The Report shall** aggregate:
- **Demographics:** Name and contact details from the **PATIENT** table.
- **Clinical History:** Visit notes and reasons from the **VISIT** table.
- **Diagnostics:** Test results, reference ranges, and abnormal flags from **LAB_RESULT** and **LAB_TEST**.
- **Treatment:** Prescribed dosages from **PRESCRIPTION_ITEM** matched with fulfilled medications from **DISPENSE** and **MEDICINE**.
- **Billing Summary:** Total amount due and payment history from **INVOICE** and **PAYMENT**.
