------------------------------------------------------------
-- DROP TABLES IF THEY EXIST (order due to FKs)
------------------------------------------------------------

DROP TABLE IF EXISTS invoice CASCADE;
DROP TABLE IF EXISTS prescription_item CASCADE;
DROP TABLE IF EXISTS prescription CASCADE;
DROP TABLE IF EXISTS doctor CASCADE;
DROP TABLE IF EXISTS patient CASCADE;
DROP TABLE IF EXISTS user_role CASCADE;
DROP TABLE IF EXISTS role CASCADE;
DROP TABLE IF EXISTS users CASCADE;

------------------------------------------------------------
-- 1) users
------------------------------------------------------------

CREATE TABLE users (
    user_id        SERIAL PRIMARY KEY,
    username       VARCHAR(50)  NOT NULL UNIQUE,
    password_hash  VARCHAR(255) NOT NULL,
    email          VARCHAR(100) NOT NULL UNIQUE,
    full_name      VARCHAR(150),
    status         VARCHAR(30)  NOT NULL DEFAULT 'ACTIVE',
    department_id  INT,
    created_at     TIMESTAMP    NOT NULL DEFAULT NOW(),
    last_login     TIMESTAMP    NULL
);

------------------------------------------------------------
-- 2) role
------------------------------------------------------------

CREATE TABLE role (
    role_id     SERIAL PRIMARY KEY,
    role_name   VARCHAR(50) NOT NULL UNIQUE,   -- 'admin','doctor','patient','pharmacist',...
    description TEXT
);

------------------------------------------------------------
-- 3) user_role
------------------------------------------------------------

CREATE TABLE user_role (
    user_role_id  SERIAL PRIMARY KEY,
    user_id       INT NOT NULL,
    role_id       INT NOT NULL,
    assigned_date DATE NOT NULL DEFAULT CURRENT_DATE,
    CONSTRAINT fk_user_role_user
        FOREIGN KEY (user_id) REFERENCES users(user_id),
    CONSTRAINT fk_user_role_role
        FOREIGN KEY (role_id) REFERENCES role(role_id)
);

------------------------------------------------------------
-- 4) patient
------------------------------------------------------------

CREATE TABLE patient (
    id                      SERIAL PRIMARY KEY,
    first_name              VARCHAR(100) NOT NULL,
    last_name               VARCHAR(100),
    dob                     DATE        NOT NULL,
    gender                  VARCHAR(10) NOT NULL,    -- 'Male','Female','Other'
    blood_group             VARCHAR(3)  NOT NULL,    -- 'A+','A-',...,'O-'
    phone                   VARCHAR(20) NOT NULL,
    emergency_contact_name  VARCHAR(100) NOT NULL,
    emergency_contact_phone VARCHAR(20)  NOT NULL,
    patient_type            VARCHAR(20)  NOT NULL,   -- 'Inpatient','Outpatient'
    is_active               BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT uq_patient_phone UNIQUE (phone)
);

------------------------------------------------------------
-- 5) doctor
------------------------------------------------------------

CREATE TABLE doctor (
    doctor_id        SERIAL PRIMARY KEY,
    user_id          INT NOT NULL,
    first_name       VARCHAR(100) NOT NULL,
    last_name        VARCHAR(100) NOT NULL,
    specialization_id INT,
    qualification    VARCHAR(150),
    license_number   VARCHAR(100) NOT NULL UNIQUE,
    phone_number     VARCHAR(15)  NOT NULL,
    email            VARCHAR(100) UNIQUE,
    experience_years INT,
    consultation_fee NUMERIC(10,2),
    date_joined      DATE,
    date_of_birth    DATE,
    is_active        BOOLEAN NOT NULL DEFAULT TRUE,
    CONSTRAINT fk_doctor_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
);

------------------------------------------------------------
-- 6) prescription
------------------------------------------------------------

CREATE TABLE prescription (
    prescription_id   SERIAL PRIMARY KEY,
    patient_id        INT         NOT NULL,
    doctor_id         INT         NOT NULL,
    created_at        TIMESTAMP   NOT NULL DEFAULT NOW(),
    notes             VARCHAR(500),
    status            VARCHAR(50) NOT NULL DEFAULT 'active',
    CONSTRAINT fk_prescription_patient
        FOREIGN KEY (patient_id) REFERENCES patient(id),
    CONSTRAINT fk_prescription_doctor
        FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
);

------------------------------------------------------------
-- 7) prescription_item
------------------------------------------------------------

CREATE TABLE prescription_item (
    prescription_item_id SERIAL PRIMARY KEY,
    prescription_id      INT         NOT NULL,
    medicine_id          INT         NOT NULL,
    dosage               VARCHAR(100) NOT NULL,
    frequency            VARCHAR(50)  NOT NULL,
    duration_days        INT          NOT NULL,
    quantity             INT          NOT NULL,
    CONSTRAINT fk_prescription_item_prescription
        FOREIGN KEY (prescription_id) REFERENCES prescription(prescription_id)
);

------------------------------------------------------------
-- 8) invoice
------------------------------------------------------------

CREATE TABLE invoice (
    invoice_id       SERIAL PRIMARY KEY,
    patient_id       INT         NOT NULL,
    issue_datetime   TIMESTAMP   NOT NULL DEFAULT NOW(),
    invoice_type     VARCHAR(50) NOT NULL,          -- 'OPD','IPD','Pharmacy',...
    subtotal         NUMERIC(10,2) NOT NULL,
    tax_amount       NUMERIC(10,2) NOT NULL,
    discount_amount  NUMERIC(10,2) NOT NULL,
    grand_total      NUMERIC(10,2) NOT NULL,
    status           VARCHAR(20)  NOT NULL,         -- 'PENDING','PAID','CANCELLED'
    created_by       INT          NOT NULL,
    CONSTRAINT fk_invoice_patient
        FOREIGN KEY (patient_id) REFERENCES patient(id),
    CONSTRAINT fk_invoice_user
        FOREIGN KEY (created_by) REFERENCES users(user_id)
);

------------------------------------------------------------
-- SAMPLE DATA
------------------------------------------------------------

-- roles
INSERT INTO role (role_name, description) VALUES
('admin',      'System administrator'),
('doctor',     'Medical doctor'),
('patient',    'Patient user'),
('pharmacist', 'Pharmacy staff');

-- users
INSERT INTO users (username, password_hash, email, full_name, status, department_id)
VALUES
('admin',   'hash_admin',   'admin@example.com',   'System Admin',       'ACTIVE', 1),
('docuser', 'hash_doc',     'doctor@example.com',  'Dr. John Smith',     'ACTIVE', 2),
('patuser', 'hash_patient', 'patient@example.com', 'Arjun Sharma',       'ACTIVE', 3),
('pharm',   'hash_pharm',   'pharm@example.com',   'Pharmacist Kumar',   'ACTIVE', 4);

-- user_role mappings (admin, doctor, patient, pharmacist)
INSERT INTO user_role (user_id, role_id)
SELECT u.user_id, r.role_id FROM users u, role r
WHERE u.username = 'admin' AND r.role_name = 'admin';

INSERT INTO user_role (user_id, role_id)
SELECT u.user_id, r.role_id FROM users u, role r
WHERE u.username = 'docuser' AND r.role_name = 'doctor';

INSERT INTO user_role (user_id, role_id)
SELECT u.user_id, r.role_id FROM users u, role r
WHERE u.username = 'patuser' AND r.role_name = 'patient';

INSERT INTO user_role (user_id, role_id)
SELECT u.user_id, r.role_id FROM users u, role r
WHERE u.username = 'pharm' AND r.role_name = 'pharmacist';

-- patient
INSERT INTO patient (
    first_name, last_name, dob, gender, blood_group,
    phone, emergency_contact_name, emergency_contact_phone,
    patient_type, is_active
) VALUES
('Arjun', 'Sharma', '1995-03-10', 'Male', 'B+',
 '9000000001', 'Ravi Sharma', '9000001001', 'Outpatient', TRUE);

-- doctor (linked to docuser)
INSERT INTO doctor (
    user_id, first_name, last_name, specialization_id,
    qualification, license_number, phone_number, email,
    experience_years, consultation_fee, date_joined, date_of_birth, is_active
)
SELECT
    u.user_id, 'John', 'Smith', 1,
    'MBBS, MD (Cardiology)', 'LIC-IND-CARD-001',
    '9876500001', u.email,
    10, 800.00, DATE '2015-06-01', DATE '1980-04-12', TRUE
FROM users u
WHERE u.username = 'docuser';

-- prescription for patient 1 by doctor 1
INSERT INTO prescription (
    patient_id, doctor_id, created_at, notes, status
) VALUES
(1, 1, NOW(), 'Test prescription for API checks', 'active');

-- prescription items for prescription 1
INSERT INTO prescription_item (
    prescription_id, medicine_id, dosage, frequency, duration_days, quantity
) VALUES
(1, 1001, '500 mg', '1-0-1', 5, 10),
(1, 1002, '10 mg',  '0-1-0', 7, 7);

-- invoice for patient 1, created by pharmacist user
INSERT INTO invoice (
    patient_id, issue_datetime, invoice_type,
    subtotal, tax_amount, discount_amount, grand_total,
    status, created_by
)
SELECT
    1, NOW(), 'Pharmacy',
    500.00, 25.00, 0.00, 525.00,
    'PAID', u.user_id
FROM users u
WHERE u.username = 'pharm';
