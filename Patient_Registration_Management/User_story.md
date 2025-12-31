# Patient Registration & Management Module – User Story

## User Story

**As a registration desk staff member**,  
**I want to register and manage patient details, addresses, visits, admissions, and insurance information**,  
**so that every patient is uniquely identified and their complete medical journey can be accurately tracked and reused across hospital departments.**

---

## Acceptance Criteria

### 1. Patient Table
- The system shall auto-generate a unique **Patient ID** for each patient.
- **Name**, **Date of Birth**, and **Gender** are mandatory fields.
- **Gender** must be restricted to predefined values: `Male`, `Female`, `Other`.
- **Blood Group** must be selected from a valid predefined list (e.g., A+, A−, B+, O+).
- **Contact Number** must be unique per patient.
- Emergency contact details must be stored.
- Patient type must be classified as either:
  - `Inpatient`
  - `Outpatient`
- Duplicate patient records must not be allowed.
- Patient records can be updated without loss of existing data.

---

### 2. Address Table
- Each patient may have one or more associated address records.
- Address details must include:
  - Address line
  - City
  - State
  - Postal code
- Each address record must be linked to a patient using **Patient ID** as a foreign key.
- Address data must support filtering and reporting operations.

---

### 3. Visit Table
- Every interaction between a patient and the hospital must generate a visit record.
- Visit type must be one of:
  - `OPD`
  - `Emergency`
  - `Follow-up`
- Each visit must record:
  - Visit date and time
  - Attending doctor ID (foreign key)
- Visit status must be maintained as one of:
  - `Open`
  - `Closed`
  - `Referred`
- Visit records must be stored in chronological order for each patient.

---

### 4. Admission Table
- Only eligible visits may be converted into inpatient admissions.
- Admission records must include:
  - Ward number
  - Bed number
  - Admission date
- Discharge date must be recorded before closing an admission.
- Each admission must be linked to:
  - Patient ID
  - Visit ID
- Inpatient status must be maintained throughout the hospital stay.

---

### 5. Insurance Table
- Insurance details must include:
  - Insurance provider name
  - Policy number
  - Validity start date
  - Validity end date
- Insurance records must be linked to the patient using **Patient ID**.
- Insurance validity must be available for billing and financial workflows.

---
