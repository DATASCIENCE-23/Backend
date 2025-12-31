## Lab Appointment Scheduling

### Goal

Enable patients to schedule laboratory tests prescribed by a doctor, ensure smooth sample collection, accurate results, and automatic availability in EMR.

---

## User Story 1: Doctor Creates Lab Order

**As a** Doctor
**I want to** create a lab order from the patient’s medical record
**So that** required diagnostic tests can be performed

### Acceptance Criteria

* Doctor can create a lab order linked to:

  * Patient
  * Medical record
* Priority can be selected
* Lab order status defaults to `ORDERED`
* Lab order is visible to patient and lab staff

---

## User Story 2: Patient Views Lab Order

**As a** Patient
**I want to** view my lab order
**So that** I know which tests are required

### Acceptance Criteria

* Patient can see:

  * Test names
  * Fasting requirement
  * Priority
* Lab order status is clearly displayed

---

## User Story 3: Schedule Lab Appointment

**As a** Patient
**I want to** schedule a lab appointment
**So that** I can give samples at a convenient time

### Acceptance Criteria

* Patient can select:

  * Lab location
  * Date and time
  * Home collection (if available)
* System validates lab availability
* Lab schedule is created and linked to the lab order
* Lab order status updates to `SCHEDULED`

---

## User Story 4: Lab Technician Handles Appointment

**As a** Lab Technician
**I want to** see my assigned lab schedules
**So that** I can collect samples on time

### Acceptance Criteria

* Technician can view:

  * Patient details
  * Ordered tests
  * Appointment time
  * Sample type
* Technician can mark schedule status as `IN_PROGRESS` or `COMPLETED`

---

## User Story 5: Enter Lab Test Results

**As a** Lab Technician / Lab Staff
**I want to** record lab test results
**So that** doctors can review them

### Acceptance Criteria

* Results are entered per test
* Each result is linked to:

  * Lab order
  * Lab test
* Results can be saved as draft or verified
* Lab order status updates to `COMPLETED` when all results are verified

---

## User Story 6: Doctor Reviews Lab Report

**As a** Doctor
**I want to** view lab reports in the EMR
**So that** I can update diagnosis and treatment

### Acceptance Criteria

* Lab report is linked to the medical record
* Doctor can view historical lab reports
* Report is read-only after finalization

---
