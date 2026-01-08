-- Fix Sample Data for Lab Scheduling Module
-- Corrections and updates to sample data

-- Update any incorrect data
UPDATE lab_orders SET status = 'completed' WHERE lab_order_id IN (1, 2, 5);
UPDATE lab_orders SET status = 'scheduled' WHERE lab_order_id = 3;
UPDATE lab_orders SET status = 'ordered' WHERE lab_order_id = 4;

-- Ensure schedule statuses match order statuses
UPDATE lab_schedules SET schedule_status = 'completed' WHERE lab_order_id IN (1, 2, 5);
UPDATE lab_schedules SET schedule_status = 'scheduled' WHERE lab_order_id = 3;

-- Add missing lab facility data if needed
INSERT INTO lab_facilities (lab_id, lab_name, location, is_active) VALUES
(1, 'Main Laboratory', 'Building A, Floor 2', true),
(2, 'Emergency Lab', 'Emergency Department', true),
(3, 'Outpatient Lab', 'Outpatient Building', true)
ON CONFLICT (lab_id) DO NOTHING;

-- Ensure all results have proper verification
UPDATE lab_results SET verified_at = created_at + INTERVAL '2 hours', verified_by = 301 
WHERE verified_at IS NULL AND lab_order_id IN (1, 2, 5);

-- Fix any date inconsistencies
UPDATE lab_results SET result_date = (SELECT scheduled_date FROM lab_schedules WHERE lab_schedules.lab_order_id = lab_results.lab_order_id LIMIT 1)
WHERE result_date < (SELECT scheduled_date FROM lab_schedules WHERE lab_schedules.lab_order_id = lab_results.lab_order_id LIMIT 1);

-- Ensure reports are generated for completed orders
UPDATE lab_reports SET status = 'finalized', finalized_at = generated_at + INTERVAL '4 hours', finalized_by = 301
WHERE lab_order_id IN (SELECT lab_order_id FROM lab_orders WHERE status = 'completed') AND status = 'draft';