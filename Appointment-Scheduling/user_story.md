# Appointment Scheduling Module - User Story

## Book Appointment
**Role:** Patient  
**Goal:** Book an appointment with a doctor based on specialization, date, and available time slots.  
**Benefit:** Consult the doctor conveniently.

**Acceptance Criteria:**
- Patient must be logged in.
- Patient can select a specialization.
- System displays doctors under the selected specialization.
- Patient can select date and view available time slots.
- System prevents booking of already booked or blocked slots.
- Appointment is created successfully upon confirmation.

---

## View Appointments
**Role:** Patient  
**Goal:** View upcoming and past appointments.  
**Benefit:** Keep track of consultations efficiently.

---

## Cancel Appointment
**Role:** Patient  
**Goal:** Cancel an appointment before the consultation time.  
**Benefit:** Frees the slot for other patients.

**Acceptance Criteria:**
- Cancellation allowed only before a defined cutoff time.
- Cancellation reason is mandatory.
- Appointment status changes to Cancelled.

---

## View Doctor Schedule
**Role:** Doctor  
**Goal:** View daily appointment schedule.  
**Benefit:** Manage consultations efficiently.

---

## Block Doctor Availability
**Role:** Doctor  
**Goal:** Block specific dates or time slots.  
**Benefit:** Prevent appointments during unavailability.

---

## Manage Doctor Schedule
**Role:** Admin  
**Goal:** Define and update doctor working schedules.  
**Benefit:** Ensure appointment slots are generated correctly.

---

## Manage Appointments
**Role:** Admin  
**Goal:** Reschedule or cancel appointments.  
**Benefit:** Handle operational changes smoothly.
