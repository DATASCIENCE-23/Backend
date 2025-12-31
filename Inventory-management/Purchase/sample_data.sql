-- ============================================
-- FINAL SAMPLE DATA FOR PURCHASE MODULE
-- ============================================

-- Delete existing test data first (optional, comment out if you want to keep)
-- DELETE FROM hms.goods_receipt WHERE grn_number LIKE 'GRN-2025%';
-- DELETE FROM hms.stock WHERE item_id IN (SELECT item_id FROM hms.item WHERE item_code LIKE 'MED-%' OR item_code LIKE 'EQP-%' OR item_code LIKE 'CON-%');
-- DELETE FROM hms.purchase_order_item WHERE purchase_id IN (SELECT purchase_id FROM hms.purchase_order WHERE po_number LIKE 'PO-2025%');
-- DELETE FROM hms.purchase_order WHERE po_number LIKE 'PO-2025%';
-- DELETE FROM hms.item WHERE item_code LIKE 'MED-%' OR item_code LIKE 'EQP-%' OR item_code LIKE 'CON-%';
-- DELETE FROM hms.category WHERE category_name IN ('Medicines', 'Medical Equipment', 'Consumables');
-- DELETE FROM hms.supplier WHERE supplier_code LIKE 'SUP-%';
-- DELETE FROM hms.store_location WHERE location_code LIKE 'LOC-%';
-- DELETE FROM hms.users WHERE username IN ('procurement_user', 'store_manager', 'receiving_officer');
-- DELETE FROM hms.department WHERE department_code = 'PROC-001';

-- ============================================
-- Step 1: Check/Insert Department
-- ============================================
INSERT INTO hms.department (department_name, department_code, floor, is_active)
SELECT 'Procurement', 'PROC-001', '1', true
WHERE NOT EXISTS (SELECT 1 FROM hms.department WHERE department_code = 'PROC-001');

-- ============================================
-- Step 2: Insert Users
-- ============================================
INSERT INTO hms.users (username, password_hash, email, full_name, status, department_id)
SELECT 'procurement_user', 'hash1', 'procurement@hospital.com', 'John Procurement', 'active', d.department_id
FROM hms.department d WHERE d.department_code = 'PROC-001'
AND NOT EXISTS (SELECT 1 FROM hms.users WHERE username = 'procurement_user');

INSERT INTO hms.users (username, password_hash, email, full_name, status, department_id)
SELECT 'store_manager', 'hash2', 'store@hospital.com', 'Sarah Store Manager', 'active', d.department_id
FROM hms.department d WHERE d.department_code = 'PROC-001'
AND NOT EXISTS (SELECT 1 FROM hms.users WHERE username = 'store_manager');

INSERT INTO hms.users (username, password_hash, email, full_name, status, department_id)
SELECT 'receiving_officer', 'hash3', 'receiving@hospital.com', 'Mike Receiving Officer', 'active', d.department_id
FROM hms.department d WHERE d.department_code = 'PROC-001'
AND NOT EXISTS (SELECT 1 FROM hms.users WHERE username = 'receiving_officer');

-- ============================================
-- Step 3: Insert Suppliers
-- ============================================
INSERT INTO hms.supplier (supplier_name, supplier_code, contact_person, phone_number, email, address, is_active)
SELECT 'ABC Medical Supplies', 'SUP-001', 'John Smith', '555-0101', 'john@abcmedical.com', '123 Medical Street, City A', true
WHERE NOT EXISTS (SELECT 1 FROM hms.supplier WHERE supplier_code = 'SUP-001');

INSERT INTO hms.supplier (supplier_name, supplier_code, contact_person, phone_number, email, address, is_active)
SELECT 'XYZ Pharma Ltd', 'SUP-002', 'Sarah Johnson', '555-0102', 'sarah@xyzpharma.com', '456 Pharma Avenue, City B', true
WHERE NOT EXISTS (SELECT 1 FROM hms.supplier WHERE supplier_code = 'SUP-002');

INSERT INTO hms.supplier (supplier_name, supplier_code, contact_person, phone_number, email, address, is_active)
SELECT 'Global Healthcare Inc', 'SUP-003', 'Mike Davis', '555-0103', 'mike@globalhc.com', '789 Health Boulevard, City C', true
WHERE NOT EXISTS (SELECT 1 FROM hms.supplier WHERE supplier_code = 'SUP-003');

-- ============================================
-- Step 4: Insert Categories
-- ============================================
INSERT INTO hms.category (category_name, description)
SELECT 'Medicines', 'Pharmaceutical medicines and drugs'
WHERE NOT EXISTS (SELECT 1 FROM hms.category WHERE category_name = 'Medicines');

INSERT INTO hms.category (category_name, description)
SELECT 'Medical Equipment', 'Hospital equipment and devices'
WHERE NOT EXISTS (SELECT 1 FROM hms.category WHERE category_name = 'Medical Equipment');

INSERT INTO hms.category (category_name, description)
SELECT 'Consumables', 'Medical consumables and supplies'
WHERE NOT EXISTS (SELECT 1 FROM hms.category WHERE category_name = 'Consumables');

-- ============================================
-- Step 5: Insert Items
-- ============================================
INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'MED-001', 'Paracetamol 500mg', 'Box', 150.00, true, 100, 50, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medicines'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'MED-001');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'MED-002', 'Amoxicillin 250mg', 'Box', 200.00, true, 80, 40, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medicines'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'MED-002');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'MED-003', 'Ibuprofen 400mg', 'Box', 180.00, true, 120, 60, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medicines'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'MED-003');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'EQP-001', 'Oxygen Cylinder', 'Unit', 5000.00, false, 10, 5, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medical Equipment'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'EQP-001');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'EQP-002', 'ECG Machine', 'Unit', 50000.00, false, 2, 1, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medical Equipment'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'EQP-002');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'EQP-003', 'Blood Pressure Monitor', 'Unit', 3000.00, false, 15, 8, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Medical Equipment'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'EQP-003');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'CON-001', 'Syringe 5ml', 'Pack', 200.00, false, 500, 250, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Consumables'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'CON-001');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'CON-002', 'Gauze Pads', 'Box', 150.00, false, 1000, 500, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Consumables'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'CON-002');

INSERT INTO hms.item (item_code, item_name, unit, unit_price, expiry_applicable, minimum_stock_level, reorder_level, category_id, status)
SELECT 'CON-003', 'Surgical Gloves', 'Box', 300.00, false, 200, 100, c.category_id, 'active'
FROM hms.category c WHERE c.category_name = 'Consumables'
AND NOT EXISTS (SELECT 1 FROM hms.item WHERE item_code = 'CON-003');

-- ============================================
-- Step 6: Insert Store Locations
-- ============================================
INSERT INTO hms.store_location (location_name, location_code, location_type, is_active)
SELECT 'Main Warehouse', 'LOC-001', 'Warehouse', true
WHERE NOT EXISTS (SELECT 1 FROM hms.store_location WHERE location_code = 'LOC-001');

INSERT INTO hms.store_location (location_name, location_code, location_type, is_active)
SELECT 'Pharmacy Store', 'LOC-002', 'Pharmacy', true
WHERE NOT EXISTS (SELECT 1 FROM hms.store_location WHERE location_code = 'LOC-002');

INSERT INTO hms.store_location (location_name, location_code, location_type, is_active)
SELECT 'Emergency Supply', 'LOC-003', 'Emergency', true
WHERE NOT EXISTS (SELECT 1 FROM hms.store_location WHERE location_code = 'LOC-003');

-- ============================================
-- Step 7: Insert Purchase Orders
-- ============================================
INSERT INTO hms.purchase_order (po_number, order_date, supplier_id, total_amount, status, created_by, expected_delivery_date)
SELECT 'PO-2025-001', '2025-01-15'::date, s.supplier_id, 140000.00, 'pending', u.user_id, '2025-01-25'::date
FROM hms.supplier s, hms.users u WHERE s.supplier_code = 'SUP-001' AND u.username = 'procurement_user'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order WHERE po_number = 'PO-2025-001');

INSERT INTO hms.purchase_order (po_number, order_date, supplier_id, total_amount, status, created_by, expected_delivery_date)
SELECT 'PO-2025-002', '2025-01-16'::date, s.supplier_id, 290000.00, 'pending', u.user_id, '2025-01-26'::date
FROM hms.supplier s, hms.users u WHERE s.supplier_code = 'SUP-002' AND u.username = 'procurement_user'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order WHERE po_number = 'PO-2025-002');

INSERT INTO hms.purchase_order (po_number, order_date, supplier_id, total_amount, status, created_by, expected_delivery_date)
SELECT 'PO-2025-003', '2025-01-17'::date, s.supplier_id, 132000.00, 'approved', u.user_id, '2025-01-27'::date
FROM hms.supplier s, hms.users u WHERE s.supplier_code = 'SUP-003' AND u.username = 'store_manager'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order WHERE po_number = 'PO-2025-003');

-- ============================================
-- Step 8: Insert Purchase Order Items
-- ============================================
INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 100, 0, 150.00, 15000.00, '2026-01-15'::date
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-001' AND i.item_code = 'MED-001'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 5, 0, 5000.00, 25000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-001' AND i.item_code = 'EQP-001'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 500, 0, 200.00, 100000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-001' AND i.item_code = 'CON-001'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 200, 0, 200.00, 40000.00, '2026-02-16'::date
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-002' AND i.item_code = 'MED-002'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 2, 0, 50000.00, 100000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-002' AND i.item_code = 'EQP-002'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 1000, 0, 150.00, 150000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-002' AND i.item_code = 'CON-002'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 150, 0, 180.00, 27000.00, '2026-01-17'::date
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-003' AND i.item_code = 'MED-003'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 15, 0, 3000.00, 45000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-003' AND i.item_code = 'EQP-003'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

INSERT INTO hms.purchase_order_item (purchase_id, item_id, ordered_quantity, received_quantity, unit_price, line_total, expiry_date)
SELECT p.purchase_id, i.item_id, 200, 0, 300.00, 60000.00, NULL
FROM hms.purchase_order p, hms.item i WHERE p.po_number = 'PO-2025-003' AND i.item_code = 'CON-003'
AND NOT EXISTS (SELECT 1 FROM hms.purchase_order_item WHERE purchase_id = p.purchase_id AND item_id = i.item_id);

-- ============================================
-- Step 9: Insert Stock
-- ============================================
INSERT INTO hms.stock (item_id, location_id, quantity_available, reserved_quantity, last_updated)
SELECT i.item_id, l.location_id, 150, 0, NOW()
FROM hms.item i, hms.store_location l WHERE i.item_code = 'MED-003' AND l.location_code = 'LOC-001'
AND NOT EXISTS (SELECT 1 FROM hms.stock WHERE item_id = i.item_id AND location_id = l.location_id);

INSERT INTO hms.stock (item_id, location_id, quantity_available, reserved_quantity, last_updated)
SELECT i.item_id, l.location_id, 15, 0, NOW()
FROM hms.item i, hms.store_location l WHERE i.item_code = 'EQP-003' AND l.location_code = 'LOC-001'
AND NOT EXISTS (SELECT 1 FROM hms.stock WHERE item_id = i.item_id AND location_id = l.location_id);

INSERT INTO hms.stock (item_id, location_id, quantity_available, reserved_quantity, last_updated)
SELECT i.item_id, l.location_id, 200, 0, NOW()
FROM hms.item i, hms.store_location l WHERE i.item_code = 'CON-003' AND l.location_code = 'LOC-001'
AND NOT EXISTS (SELECT 1 FROM hms.stock WHERE item_id = i.item_id AND location_id = l.location_id);

-- ============================================
-- Step 10: Insert Goods Receipts
-- ============================================
INSERT INTO hms.goods_receipt (purchase_id, grn_number, receipt_date, received_by, notes)
SELECT p.purchase_id, 'GRN-2025-01-00001', '2025-01-25'::date, u.user_id, 'All items received in good condition'
FROM hms.purchase_order p, hms.users u WHERE p.po_number = 'PO-2025-001' AND u.username = 'receiving_officer'
AND NOT EXISTS (SELECT 1 FROM hms.goods_receipt WHERE grn_number = 'GRN-2025-01-00001');

INSERT INTO hms.goods_receipt (purchase_id, grn_number, receipt_date, received_by, notes)
SELECT p.purchase_id, 'GRN-2025-01-00002', '2025-01-26'::date, u.user_id, 'Partial delivery - 2 items received, 1 pending'
FROM hms.purchase_order p, hms.users u WHERE p.po_number = 'PO-2025-002' AND u.username = 'receiving_officer'
AND NOT EXISTS (SELECT 1 FROM hms.goods_receipt WHERE grn_number = 'GRN-2025-01-00002');

-- ============================================
-- VERIFICATION
-- ============================================
SELECT '✓ DATA INSERTED SUCCESSFULLY' as status;

SELECT 'Departments' as table_name, COUNT(*) as count FROM hms.department WHERE department_code = 'PROC-001'
UNION ALL
SELECT 'Users', COUNT(*) FROM hms.users WHERE username IN ('procurement_user', 'store_manager', 'receiving_officer')
UNION ALL
SELECT 'Suppliers', COUNT(*) FROM hms.supplier WHERE supplier_code IN ('SUP-001', 'SUP-002', 'SUP-003')
UNION ALL
SELECT 'Categories', COUNT(*) FROM hms.category WHERE category_name IN ('Medicines', 'Medical Equipment', 'Consumables')
UNION ALL
SELECT 'Items', COUNT(*) FROM hms.item WHERE item_code LIKE 'MED-%' OR item_code LIKE 'EQP-%' OR item_code LIKE 'CON-%'
UNION ALL
SELECT 'Store Locations', COUNT(*) FROM hms.store_location WHERE location_code IN ('LOC-001', 'LOC-002', 'LOC-003')
UNION ALL
SELECT 'Purchase Orders', COUNT(*) FROM hms.purchase_order WHERE po_number IN ('PO-2025-001', 'PO-2025-002', 'PO-2025-003')
UNION ALL
SELECT 'Purchase Order Items', COUNT(*) FROM hms.purchase_order_item WHERE purchase_id IN (SELECT purchase_id FROM hms.purchase_order WHERE po_number LIKE 'PO-2025%')
UNION ALL
SELECT 'Stock', COUNT(*) FROM hms.stock WHERE item_id IN (3, 6, 9)
UNION ALL
SELECT 'Goods Receipts', COUNT(*) FROM hms.goods_receipt WHERE grn_number IN ('GRN-2025-01-00001', 'GRN-2025-01-00002');
