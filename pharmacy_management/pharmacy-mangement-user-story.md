# Hospital Pharmacy Module – User Stories

## 1. Actors

- Pharmacist
- Doctor
- Inventory Manager
- Billing Staff
- System (background jobs / integrations)

---

## 2. High-level Features (Scope for 1 Week)

- Maintain medicines master (basic CRUD).
- Receive prescriptions from doctors (via simple web service).
- Dispense medicines against a prescription.
- Auto‑update stock when dispensing.
- Basic low‑stock alerts for integration with Inventory module later.

---

## 3. User Stories

### 3.1 Medicine Catalogue Management

**US-1: Add new medicine**

As a **pharmacist**,  
I want to add a new medicine with name, generic name, strength, form, expiry date, and unit price,  
so that it is available for prescribing and dispensing.

**Acceptance criteria:**
- Given valid medicine details, when I click save, the medicine record is created with a unique ID.
- Required fields validated (name, generic name, strength, form, unit price).
- Duplicate name + strength + form combination is not allowed.

---

**US-2: Update medicine details**

As a **pharmacist**,  
I want to update medicine information (price, active status, shelf location),  
so that current stock can be maintained without deleting historical data.

**Acceptance criteria:**
- I can mark medicines as active/inactive instead of deleting.
- Price changes apply only to future transactions.
- History of changes is stored (at least last modified timestamp and user).

---

**US-3: View and search medicines**

As a **pharmacist**,  
I want to search medicines by name, generic name, or code,  
so that I can quickly find the correct item during dispensing.  

**Acceptance criteria:**
- Search box filters by name, generic name, or ID.
- Results show available quantity and expiry for each batch.

---

### 3.2 Prescription Handling (Web Service Learning)

**US-4: Receive prescription via web service**

As a **pharmacy system**,  
I want to receive electronic prescriptions from the doctor module through a REST API,  
so that the pharmacist does not have to manually re‑enter prescription details.

**Acceptance criteria:**
- API endpoint `/api/prescriptions` accepts prescription data (patient ID, doctor ID, list of medicine IDs, dosage, quantity).
- Valid request creates a Prescription record with status = “Pending”.
- Invalid requests return meaningful error codes/messages.
- Prescription is visible in the pharmacist’s “Pending prescriptions” list.

---

**US-5: View pending prescriptions**

As a **pharmacist**,  
I want to see a list of pending prescriptions with patient and doctor details,  
so that I can prioritize and process dispensing.

**Acceptance criteria:**
- List shows prescription ID, patient name, doctor name, timestamp, and status.
- I can open a prescription to see item‑wise details.

---

### 3.3 Dispensing and Stock Update

**US-6: Validate stock before dispensing**

As a **pharmacist**,  
I want the system to check available stock for each prescribed medicine,  
so that I can know if I can fully or partially dispense the prescription.

**Acceptance criteria:**
- When opening a prescription, system shows available quantity per medicine.
- If requested quantity > available, system highlights that line and suggests partial quantity.
- Pharmacist can choose partial dispense and document it.

---

**US-7: Dispense medicines**

As a **pharmacist**,  
I want to confirm dispensing of medicines and record quantities taken from stock,  
so that the patient receives medicines and inventory stays accurate.  

**Acceptance criteria:**
- On confirm, stock quantity decreases from corresponding medicine batch(es).
- A “Dispense record” is created with date, pharmacist ID, and dispensed quantities.
- Prescription status changes to “Completed” or “Partially Completed”.

---

**US-8: Generate billable dispensing information**

As **billing staff**,  
I want to see total amount for dispensed medicines linked to the patient visit,  
so that I can generate the final patient bill.

**Acceptance criteria:**
- The system calculates line total = quantity × unit price for each item.
- Total amount and list of items are exposed via an API for the billing module.
- Dispense record has a flag whether it is already billed or not.

---

### 3.4 Basic Stock Monitoring (for Inventory Integration)

**US-9: Low stock alert**

As an **inventory manager**,  
I want to see which medicines have stock below a minimum threshold,  
so that I can create purchase requests in the inventory module.

**Acceptance criteria:**
- Each medicine has a configurable minimum quantity.
- A “Low stock” view lists medicines where available quantity < minimum quantity.
- Data can be fetched via an API endpoint so the inventory module can read it.

---

### 3.5 Non-functional / Technical Stories (Web Services)

**NFR-1: Simple REST API**

As a **developer**,  
I want the pharmacy module to expose REST endpoints for prescriptions and low‑stock data,  
so that other modules (doctor, inventory, billing) can integrate easily.

**Acceptance criteria:**
- APIs documented (URL, method, request/response JSON).
- Returns proper HTTP status codes (200, 201, 400, 404, 500).
- Basic input validation and error messages.

**NFR-2: Audit and security (minimal)**

As a **system administrator**,  
I want user actions (create/update/dispense) to be recorded with timestamps and user,  
so that we have a basic audit trail.

**Acceptance criteria:**
- Create/update/dispense operations store user ID and timestamp.
- Only authenticated users can access APIs and UI.