-- Sample Data for Lab Scheduling Module
-- Insert test data for development and testing

-- Insert Lab Technicians
INSERT INTO lab_technicians (technician_id, first_name, last_name, license_number, phone_number, email, specialization, is_active) VALUES
(1, 'Alice', 'Johnson', 'LT001', '555-0101', 'alice.johnson@hospital.com', 'Hematology', true),
(2, 'Bob', 'Smith', 'LT002', '555-0102', 'bob.smith@hospital.com', 'Chemistry', true),
(3, 'Carol', 'Davis', 'LT003', '555-0103', 'carol.davis@hospital.com', 'Microbiology', true),
(4, 'David', 'Wilson', 'LT004', '555-0104', 'david.wilson@hospital.com', 'Immunology', true);

-- Insert Lab Tests
INSERT INTO lab_tests (test_id, test_name, test_code, category, description, sample_type, reference_range_min, reference_range_max, reference_range_text, turnaround_time_hours, is_active, requires_fasting, cost) VALUES
(1, 'Complete Blood Count', 'CBC', 'Hematology', 'Complete blood count with differential', 'Blood', NULL, NULL, 'See individual components', 4, true, false, 25.00),
(2, 'Blood Glucose', 'GLU', 'Chemistry', 'Fasting blood glucose level', 'Blood', 70, 100, '70-100 mg/dL', 2, true, true, 15.00),
(3, 'Lipid Panel', 'LIPID', 'Chemistry', 'Cholesterol and triglycerides', 'Blood', NULL, NULL, 'See individual components', 4, true, true, 45.00),
(4, 'Thyroid Stimulating Hormone', 'TSH', 'Endocrinology', 'TSH level', 'Blood', 0.4, 4.0, '0.4-4.0 mIU/L', 24, true, false, 35.00),
(5, 'Urinalysis', 'UA', 'Chemistry', 'Complete urinalysis', 'Urine', NULL, NULL, 'Normal', 2, true, false, 20.00);

-- Insert Lab Orders
INSERT INTO lab_orders (lab_order_id, patient_id, doctor_id, record_id, order_date, priority, status, clinical_notes) VALUES
(1, 101, 201, 301, '2024-01-10 09:00:00', 'normal', 'completed', 'Routine annual checkup'),
(2, 102, 202, 302, '2024-01-11 10:30:00', 'urgent', 'sample_collected', 'Patient experiencing fatigue'),
(3, 103, 201, 303, '2024-01-12 14:15:00', 'normal', 'scheduled', 'Pre-operative testing'),
(4, 104, 203, 304, '2024-01-13 11:45:00', 'stat', 'ordered', 'Emergency department referral'),
(5, 105, 202, 305, '2024-01-14 08:30:00', 'normal', 'completed', 'Follow-up testing');

-- Insert Lab Schedules
INSERT INTO lab_schedules (schedule_id, lab_order_id, lab_id, technician_id, scheduled_date, start_time, end_time, sample_type, schedule_status, home_collection, notes) VALUES
(1, 1, 1, 1, '2024-01-15', '09:00:00', '09:30:00', 'Blood', 'completed', false, 'Patient arrived on time'),
(2, 2, 1, 2, '2024-01-16', '10:00:00', '10:30:00', 'Blood', 'completed', false, 'Urgent processing requested'),
(3, 3, 1, 1, '2024-01-17', '14:00:00', '14:30:00', 'Blood', 'scheduled', false, 'Pre-op patient'),
(4, 5, 1, 3, '2024-01-18', '08:30:00', '09:00:00', 'Blood', 'completed', true, 'Home collection completed');

-- Insert Lab Results
INSERT INTO lab_results (result_id, lab_order_id, test_id, result_date, result_value, reference_range, abnormal_flag, remarks, verified_at, verified_by) VALUES
(1, 1, 1, '2024-01-15', 'Normal', 'Normal ranges', 'normal', 'All parameters within normal limits', '2024-01-15 15:30:00', 301),
(2, 1, 2, '2024-01-15', '85', '70-100 mg/dL', 'normal', 'Fasting glucose normal', '2024-01-15 15:30:00', 301),
(3, 2, 2, '2024-01-16', '145', '70-100 mg/dL', 'high', 'Elevated glucose, recommend follow-up', '2024-01-16 16:00:00', 302),
(4, 2, 4, '2024-01-16', '8.5', '0.4-4.0 mIU/L', 'high', 'Elevated TSH, possible hypothyroidism', '2024-01-16 16:00:00', 302),
(5, 5, 3, '2024-01-18', 'Normal', 'See individual components', 'normal', 'Lipid panel within normal limits', '2024-01-18 14:00:00', 301);

-- Insert Lab Reports
INSERT INTO lab_reports (lab_report_id, lab_order_id, report_date, status, summary, finalized_at, finalized_by) VALUES
(1, 1, '2024-01-15', 'finalized', 'All test results are within normal ranges. Patient shows good health indicators for annual checkup.', '2024-01-15 16:00:00', 301),
(2, 2, '2024-01-16', 'finalized', 'Elevated glucose and TSH levels detected. Recommend endocrinology consultation and dietary counseling.', '2024-01-16 17:00:00', 302),
(3, 5, '2024-01-18', 'finalized', 'Follow-up lipid panel shows improvement. Continue current treatment plan.', '2024-01-18 15:00:00', 301);

-- Update sequences to avoid conflicts
SELECT setval('lab_technicians_technician_id_seq', 10);
SELECT setval('lab_tests_test_id_seq', 10);
SELECT setval('lab_orders_lab_order_id_seq', 10);
SELECT setval('lab_schedules_schedule_id_seq', 10);
SELECT setval('lab_results_result_id_seq', 10);
SELECT setval('lab_reports_lab_report_id_seq', 10);