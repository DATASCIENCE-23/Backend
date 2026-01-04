--
-- PostgreSQL database dump
--

\restrict 9UTpp3XxQ7mrpDbZjOdjnfflvP0WHalJfkNs4Us6FvbrmZyVt1Rj06h7dMsYQvI

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: hms; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA hms;


ALTER SCHEMA hms OWNER TO postgres;

--
-- Name: appointment_status_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.appointment_status_enum AS ENUM (
    'scheduled',
    'completed',
    'cancelled',
    'no_show'
);


ALTER TYPE hms.appointment_status_enum OWNER TO postgres;

--
-- Name: appointment_type_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.appointment_type_enum AS ENUM (
    'opd',
    'follow_up',
    'emergency'
);


ALTER TYPE hms.appointment_type_enum OWNER TO postgres;

--
-- Name: common_status_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.common_status_enum AS ENUM (
    'active',
    'inactive'
);


ALTER TYPE hms.common_status_enum OWNER TO postgres;

--
-- Name: day_of_week_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.day_of_week_enum AS ENUM (
    'mon',
    'tue',
    'wed',
    'thu',
    'fri',
    'sat',
    'sun'
);


ALTER TYPE hms.day_of_week_enum OWNER TO postgres;

--
-- Name: gender_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.gender_enum AS ENUM (
    'male',
    'female',
    'other'
);


ALTER TYPE hms.gender_enum OWNER TO postgres;

--
-- Name: inventory_status_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.inventory_status_enum AS ENUM (
    'active',
    'inactive'
);


ALTER TYPE hms.inventory_status_enum OWNER TO postgres;

--
-- Name: lab_priority_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.lab_priority_enum AS ENUM (
    'normal',
    'urgent',
    'stat'
);


ALTER TYPE hms.lab_priority_enum OWNER TO postgres;

--
-- Name: lab_status_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.lab_status_enum AS ENUM (
    'ordered',
    'sample_collected',
    'completed',
    'cancelled'
);


ALTER TYPE hms.lab_status_enum OWNER TO postgres;

--
-- Name: payment_status_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.payment_status_enum AS ENUM (
    'pending',
    'paid',
    'failed'
);


ALTER TYPE hms.payment_status_enum OWNER TO postgres;

--
-- Name: visit_type_enum; Type: TYPE; Schema: hms; Owner: postgres
--

CREATE TYPE hms.visit_type_enum AS ENUM (
    'opd',
    'ipd',
    'emergency'
);


ALTER TYPE hms.visit_type_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: account; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.account (
    account_id integer NOT NULL,
    account_code character varying(50),
    account_name character varying(150),
    account_type character varying(50),
    parent_account_id integer,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.account OWNER TO postgres;

--
-- Name: account_account_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.account_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.account_account_id_seq OWNER TO postgres;

--
-- Name: account_account_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.account_account_id_seq OWNED BY hms.account.account_id;


--
-- Name: address; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.address (
    address_id integer NOT NULL,
    patient_id integer,
    street text,
    city character varying(50),
    state character varying(50),
    pincode character varying(10),
    country character varying(50)
);


ALTER TABLE hms.address OWNER TO postgres;

--
-- Name: address_address_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.address_address_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.address_address_id_seq OWNER TO postgres;

--
-- Name: address_address_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.address_address_id_seq OWNED BY hms.address.address_id;


--
-- Name: admission; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.admission (
    admission_id integer NOT NULL,
    visit_id integer,
    admission_datetime timestamp without time zone,
    discharge_datetime timestamp without time zone,
    ward_id integer,
    bed_number character varying(20),
    admission_reason text,
    discharge_summary text,
    status character varying(30)
);


ALTER TABLE hms.admission OWNER TO postgres;

--
-- Name: admission_admission_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.admission_admission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.admission_admission_id_seq OWNER TO postgres;

--
-- Name: admission_admission_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.admission_admission_id_seq OWNED BY hms.admission.admission_id;


--
-- Name: appointment; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.appointment (
    appointment_id integer NOT NULL,
    patient_id integer,
    doctor_id integer,
    appointment_date date,
    start_time time without time zone,
    end_time time without time zone,
    appointment_type hms.appointment_type_enum,
    status hms.appointment_status_enum,
    reason_for_visit text,
    symptoms text,
    notes text,
    consultation_fee numeric(10,2),
    booking_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.appointment OWNER TO postgres;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.appointment_appointment_id_seq OWNER TO postgres;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.appointment_appointment_id_seq OWNED BY hms.appointment.appointment_id;


--
-- Name: appointment_history; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.appointment_history (
    history_id integer NOT NULL,
    appointment_id integer,
    changed_by integer,
    change_type character varying(30),
    old_date date,
    new_date date,
    old_time time without time zone,
    new_time time without time zone,
    old_status character varying(30),
    new_status character varying(30),
    change_reason text,
    changed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.appointment_history OWNER TO postgres;

--
-- Name: appointment_history_history_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.appointment_history_history_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.appointment_history_history_id_seq OWNER TO postgres;

--
-- Name: appointment_history_history_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.appointment_history_history_id_seq OWNED BY hms.appointment_history.history_id;


--
-- Name: appointment_reminder; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.appointment_reminder (
    reminder_id integer NOT NULL,
    appointment_id integer,
    reminder_type character varying(30),
    reminder_time timestamp without time zone,
    sent_at timestamp without time zone,
    status character varying(30),
    message_content text
);


ALTER TABLE hms.appointment_reminder OWNER TO postgres;

--
-- Name: appointment_reminder_reminder_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.appointment_reminder_reminder_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.appointment_reminder_reminder_id_seq OWNER TO postgres;

--
-- Name: appointment_reminder_reminder_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.appointment_reminder_reminder_id_seq OWNED BY hms.appointment_reminder.reminder_id;


--
-- Name: asset; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.asset (
    asset_id integer NOT NULL,
    asset_code character varying(50),
    asset_name character varying(150),
    account_id integer,
    purchase_date date,
    purchase_cost numeric(12,2),
    useful_life_years integer,
    salvage_value numeric(12,2),
    accumulated_depreciation numeric(12,2),
    status character varying(30)
);


ALTER TABLE hms.asset OWNER TO postgres;

--
-- Name: asset_asset_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.asset_asset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.asset_asset_id_seq OWNER TO postgres;

--
-- Name: asset_asset_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.asset_asset_id_seq OWNED BY hms.asset.asset_id;


--
-- Name: audit_log; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.audit_log (
    log_id integer NOT NULL,
    user_id integer,
    entity_name character varying(100),
    entity_id integer,
    action_time timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    action_type character varying(30),
    ip_address character varying(50),
    details text
);


ALTER TABLE hms.audit_log OWNER TO postgres;

--
-- Name: audit_log_log_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.audit_log_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.audit_log_log_id_seq OWNER TO postgres;

--
-- Name: audit_log_log_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.audit_log_log_id_seq OWNED BY hms.audit_log.log_id;


--
-- Name: bank_account; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.bank_account (
    bank_account_id integer NOT NULL,
    account_number character varying(50),
    bank_name character varying(100),
    branch_name character varying(100),
    account_id integer,
    current_balance numeric(12,2),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.bank_account OWNER TO postgres;

--
-- Name: bank_account_bank_account_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.bank_account_bank_account_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.bank_account_bank_account_id_seq OWNER TO postgres;

--
-- Name: bank_account_bank_account_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.bank_account_bank_account_id_seq OWNED BY hms.bank_account.bank_account_id;


--
-- Name: bill; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.bill (
    bill_id integer NOT NULL,
    vendor_id integer,
    bill_date date,
    bill_number character varying(50),
    subtotal numeric(12,2),
    tax_amount numeric(12,2),
    grand_total numeric(12,2),
    status character varying(30),
    due_date date
);


ALTER TABLE hms.bill OWNER TO postgres;

--
-- Name: bill_bill_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.bill_bill_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.bill_bill_id_seq OWNER TO postgres;

--
-- Name: bill_bill_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.bill_bill_id_seq OWNED BY hms.bill.bill_id;


--
-- Name: bill_line; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.bill_line (
    bill_line_id integer NOT NULL,
    bill_id integer,
    expense_account_id integer,
    description text,
    quantity integer,
    unit_price numeric(10,2),
    line_total numeric(12,2)
);


ALTER TABLE hms.bill_line OWNER TO postgres;

--
-- Name: bill_line_bill_line_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.bill_line_bill_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.bill_line_bill_line_id_seq OWNER TO postgres;

--
-- Name: bill_line_bill_line_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.bill_line_bill_line_id_seq OWNED BY hms.bill_line.bill_line_id;


--
-- Name: bill_payment; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.bill_payment (
    bill_payment_id integer NOT NULL,
    bill_id integer,
    payment_datetime timestamp without time zone,
    amount_paid numeric(12,2),
    payment_mode character varying(30),
    transaction_ref character varying(100),
    paid_by integer
);


ALTER TABLE hms.bill_payment OWNER TO postgres;

--
-- Name: bill_payment_bill_payment_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.bill_payment_bill_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.bill_payment_bill_payment_id_seq OWNER TO postgres;

--
-- Name: bill_payment_bill_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.bill_payment_bill_payment_id_seq OWNED BY hms.bill_payment.bill_payment_id;


--
-- Name: blocked_slots; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.blocked_slots (
    blocked_slot_id integer NOT NULL,
    doctor_id integer,
    blocked_date date,
    start_time time without time zone,
    end_time time without time zone,
    reason text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    created_by integer
);


ALTER TABLE hms.blocked_slots OWNER TO postgres;

--
-- Name: blocked_slots_blocked_slot_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.blocked_slots_blocked_slot_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.blocked_slots_blocked_slot_id_seq OWNER TO postgres;

--
-- Name: blocked_slots_blocked_slot_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.blocked_slots_blocked_slot_id_seq OWNED BY hms.blocked_slots.blocked_slot_id;


--
-- Name: budget; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.budget (
    budget_id integer NOT NULL,
    financial_year character varying(20),
    department_id integer,
    total_amount numeric(12,2),
    status character varying(30),
    created_by integer
);


ALTER TABLE hms.budget OWNER TO postgres;

--
-- Name: budget_budget_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.budget_budget_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.budget_budget_id_seq OWNER TO postgres;

--
-- Name: budget_budget_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.budget_budget_id_seq OWNED BY hms.budget.budget_id;


--
-- Name: budget_line; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.budget_line (
    budget_line_id integer NOT NULL,
    budget_id integer,
    account_id integer,
    allocated_amount numeric(12,2),
    spent_amount numeric(12,2),
    remaining_amount numeric(12,2)
);


ALTER TABLE hms.budget_line OWNER TO postgres;

--
-- Name: budget_line_budget_line_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.budget_line_budget_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.budget_line_budget_line_id_seq OWNER TO postgres;

--
-- Name: budget_line_budget_line_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.budget_line_budget_line_id_seq OWNED BY hms.budget_line.budget_line_id;


--
-- Name: category; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.category (
    category_id integer NOT NULL,
    category_name character varying(100),
    description text
);


ALTER TABLE hms.category OWNER TO postgres;

--
-- Name: category_category_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.category_category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.category_category_id_seq OWNER TO postgres;

--
-- Name: category_category_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.category_category_id_seq OWNED BY hms.category.category_id;


--
-- Name: department; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.department (
    department_id integer NOT NULL,
    department_name character varying(100) NOT NULL,
    department_code character varying(50) NOT NULL,
    floor character varying(20),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.department OWNER TO postgres;

--
-- Name: department_department_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.department_department_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.department_department_id_seq OWNER TO postgres;

--
-- Name: department_department_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.department_department_id_seq OWNED BY hms.department.department_id;


--
-- Name: depreciation; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.depreciation (
    depreciation_id integer NOT NULL,
    asset_id integer,
    depreciation_date date,
    depreciation_amount numeric(12,2),
    book_value numeric(12,2),
    journal_id integer
);


ALTER TABLE hms.depreciation OWNER TO postgres;

--
-- Name: depreciation_depreciation_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.depreciation_depreciation_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.depreciation_depreciation_id_seq OWNER TO postgres;

--
-- Name: depreciation_depreciation_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.depreciation_depreciation_id_seq OWNED BY hms.depreciation.depreciation_id;


--
-- Name: dispense; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.dispense (
    dispense_id integer NOT NULL,
    prescription_id integer,
    pharmacist_id integer,
    dispensed_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    total_amount numeric(12,2),
    status character varying(30),
    invoice_id integer
);


ALTER TABLE hms.dispense OWNER TO postgres;

--
-- Name: dispense_dispense_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.dispense_dispense_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.dispense_dispense_id_seq OWNER TO postgres;

--
-- Name: dispense_dispense_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.dispense_dispense_id_seq OWNED BY hms.dispense.dispense_id;


--
-- Name: dispense_item; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.dispense_item (
    dispense_item_id integer NOT NULL,
    dispense_id integer,
    prescription_item_id integer,
    batch_id integer,
    dispensed_quantity integer,
    unit_price numeric(10,2),
    line_total numeric(12,2)
);


ALTER TABLE hms.dispense_item OWNER TO postgres;

--
-- Name: dispense_item_dispense_item_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.dispense_item_dispense_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.dispense_item_dispense_item_id_seq OWNER TO postgres;

--
-- Name: dispense_item_dispense_item_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.dispense_item_dispense_item_id_seq OWNED BY hms.dispense_item.dispense_item_id;


--
-- Name: doctor; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.doctor (
    doctor_id integer NOT NULL,
    user_id integer,
    first_name character varying(100),
    last_name character varying(100),
    specialization_id integer,
    qualification character varying(100),
    license_number character varying(50),
    phone_number character varying(20),
    email character varying(100),
    experience_years integer,
    consultation_fee numeric(10,2),
    date_joined date,
    date_of_birth date,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.doctor OWNER TO postgres;

--
-- Name: doctor_doctor_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.doctor_doctor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.doctor_doctor_id_seq OWNER TO postgres;

--
-- Name: doctor_doctor_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.doctor_doctor_id_seq OWNED BY hms.doctor.doctor_id;


--
-- Name: doctor_schedule; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.doctor_schedule (
    schedule_id integer NOT NULL,
    doctor_id integer,
    day_of_week hms.day_of_week_enum,
    start_time time without time zone,
    end_time time without time zone,
    slot_duration integer,
    max_patients_per_slot integer,
    is_active boolean DEFAULT true,
    effective_from date,
    effective_to date
);


ALTER TABLE hms.doctor_schedule OWNER TO postgres;

--
-- Name: doctor_schedule_schedule_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.doctor_schedule_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.doctor_schedule_schedule_id_seq OWNER TO postgres;

--
-- Name: doctor_schedule_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.doctor_schedule_schedule_id_seq OWNED BY hms.doctor_schedule.schedule_id;


--
-- Name: expense; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.expense (
    expense_id integer NOT NULL,
    expense_number character varying(50),
    expense_date date,
    account_id integer,
    amount numeric(12,2),
    department_id integer,
    description text,
    reference_id integer,
    created_by integer
);


ALTER TABLE hms.expense OWNER TO postgres;

--
-- Name: expense_expense_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.expense_expense_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.expense_expense_id_seq OWNER TO postgres;

--
-- Name: expense_expense_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.expense_expense_id_seq OWNED BY hms.expense.expense_id;


--
-- Name: goods_receipt; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.goods_receipt (
    receipt_id integer NOT NULL,
    purchase_id integer,
    grn_number character varying(50),
    receipt_date date,
    received_by integer,
    notes text
);


ALTER TABLE hms.goods_receipt OWNER TO postgres;

--
-- Name: goods_receipt_receipt_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.goods_receipt_receipt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.goods_receipt_receipt_id_seq OWNER TO postgres;

--
-- Name: goods_receipt_receipt_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.goods_receipt_receipt_id_seq OWNED BY hms.goods_receipt.receipt_id;


--
-- Name: insurance; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.insurance (
    insurance_id integer NOT NULL,
    patient_id integer,
    provider_id integer,
    policy_number character varying(50),
    coverage_type character varying(50),
    coverage_percent numeric(5,2),
    valid_from date,
    valid_to date,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.insurance OWNER TO postgres;

--
-- Name: insurance_insurance_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.insurance_insurance_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.insurance_insurance_id_seq OWNER TO postgres;

--
-- Name: insurance_insurance_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.insurance_insurance_id_seq OWNED BY hms.insurance.insurance_id;


--
-- Name: insurance_provider; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.insurance_provider (
    provider_id integer NOT NULL,
    company_name character varying(150),
    contact_person character varying(100),
    phone_number character varying(20),
    email character varying(100),
    address text,
    coverage_limit numeric(12,2),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.insurance_provider OWNER TO postgres;

--
-- Name: insurance_provider_provider_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.insurance_provider_provider_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.insurance_provider_provider_id_seq OWNER TO postgres;

--
-- Name: insurance_provider_provider_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.insurance_provider_provider_id_seq OWNED BY hms.insurance_provider.provider_id;


--
-- Name: invoice; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.invoice (
    invoice_id integer NOT NULL,
    patient_id integer,
    issue_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    invoice_type character varying(30),
    subtotal numeric(10,2),
    tax_amount numeric(10,2),
    discount_amount numeric(10,2),
    grand_total numeric(10,2),
    status character varying(30),
    created_by integer
);


ALTER TABLE hms.invoice OWNER TO postgres;

--
-- Name: invoice_invoice_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.invoice_invoice_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.invoice_invoice_id_seq OWNER TO postgres;

--
-- Name: invoice_invoice_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.invoice_invoice_id_seq OWNED BY hms.invoice.invoice_id;


--
-- Name: invoice_line_item; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.invoice_line_item (
    line_item_id integer NOT NULL,
    invoice_id integer,
    service_id integer,
    description text,
    quantity integer,
    unit_price numeric(10,2),
    line_subtotal numeric(10,2),
    tax_amount numeric(10,2),
    line_total numeric(10,2)
);


ALTER TABLE hms.invoice_line_item OWNER TO postgres;

--
-- Name: invoice_line_item_line_item_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.invoice_line_item_line_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.invoice_line_item_line_item_id_seq OWNER TO postgres;

--
-- Name: invoice_line_item_line_item_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.invoice_line_item_line_item_id_seq OWNED BY hms.invoice_line_item.line_item_id;


--
-- Name: issue_details; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.issue_details (
    issue_detail_id integer NOT NULL,
    request_id integer,
    item_id integer,
    requested_quantity integer,
    issued_quantity integer,
    issued_datetime timestamp without time zone,
    issued_by integer
);


ALTER TABLE hms.issue_details OWNER TO postgres;

--
-- Name: issue_details_issue_detail_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.issue_details_issue_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.issue_details_issue_detail_id_seq OWNER TO postgres;

--
-- Name: issue_details_issue_detail_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.issue_details_issue_detail_id_seq OWNED BY hms.issue_details.issue_detail_id;


--
-- Name: issue_request; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.issue_request (
    request_id integer NOT NULL,
    request_number character varying(50),
    department_id integer,
    request_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(30),
    requested_by integer,
    approved_by integer
);


ALTER TABLE hms.issue_request OWNER TO postgres;

--
-- Name: issue_request_request_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.issue_request_request_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.issue_request_request_id_seq OWNER TO postgres;

--
-- Name: issue_request_request_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.issue_request_request_id_seq OWNED BY hms.issue_request.request_id;


--
-- Name: item; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.item (
    item_id integer NOT NULL,
    item_code character varying(50),
    item_name character varying(150),
    unit character varying(30),
    unit_price numeric(10,2),
    expiry_applicable boolean,
    minimum_stock_level integer,
    reorder_level integer,
    category_id integer,
    status hms.inventory_status_enum
);


ALTER TABLE hms.item OWNER TO postgres;

--
-- Name: item_item_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.item_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.item_item_id_seq OWNER TO postgres;

--
-- Name: item_item_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.item_item_id_seq OWNED BY hms.item.item_id;


--
-- Name: journal_entry; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.journal_entry (
    journal_id integer NOT NULL,
    journal_number character varying(50),
    journal_date date,
    reference_type character varying(50),
    reference_id integer,
    description text,
    posted_status boolean,
    created_by integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.journal_entry OWNER TO postgres;

--
-- Name: journal_entry_journal_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.journal_entry_journal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.journal_entry_journal_id_seq OWNER TO postgres;

--
-- Name: journal_entry_journal_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.journal_entry_journal_id_seq OWNED BY hms.journal_entry.journal_id;


--
-- Name: journal_line; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.journal_line (
    journal_line_id integer NOT NULL,
    journal_id integer,
    account_id integer,
    debit_amount numeric(12,2),
    credit_amount numeric(12,2),
    description text
);


ALTER TABLE hms.journal_line OWNER TO postgres;

--
-- Name: journal_line_journal_line_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.journal_line_journal_line_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.journal_line_journal_line_id_seq OWNER TO postgres;

--
-- Name: journal_line_journal_line_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.journal_line_journal_line_id_seq OWNED BY hms.journal_line.journal_line_id;


--
-- Name: lab; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab (
    lab_id integer NOT NULL,
    lab_name character varying(100),
    lab_code character varying(50),
    phone_number character varying(20),
    email character varying(100),
    address text,
    is_active boolean DEFAULT true,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.lab OWNER TO postgres;

--
-- Name: lab_lab_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_lab_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_lab_id_seq OWNER TO postgres;

--
-- Name: lab_lab_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_lab_id_seq OWNED BY hms.lab.lab_id;


--
-- Name: lab_order; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_order (
    lab_order_id integer NOT NULL,
    patient_id integer,
    doctor_id integer,
    record_id integer,
    order_datetime timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    priority hms.lab_priority_enum,
    status hms.lab_status_enum,
    clinical_notes text
);


ALTER TABLE hms.lab_order OWNER TO postgres;

--
-- Name: lab_order_lab_order_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_order_lab_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_order_lab_order_id_seq OWNER TO postgres;

--
-- Name: lab_order_lab_order_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_order_lab_order_id_seq OWNED BY hms.lab_order.lab_order_id;


--
-- Name: lab_order_test; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_order_test (
    lab_order_test_id integer NOT NULL,
    lab_order_id integer,
    test_id integer,
    status hms.lab_status_enum
);


ALTER TABLE hms.lab_order_test OWNER TO postgres;

--
-- Name: lab_order_test_lab_order_test_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_order_test_lab_order_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_order_test_lab_order_test_id_seq OWNER TO postgres;

--
-- Name: lab_order_test_lab_order_test_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_order_test_lab_order_test_id_seq OWNED BY hms.lab_order_test.lab_order_test_id;


--
-- Name: lab_report; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_report (
    lab_report_id integer NOT NULL,
    lab_order_id integer,
    report_datetime timestamp without time zone,
    summary text,
    report_file_url text,
    status character varying(30),
    prepared_by integer
);


ALTER TABLE hms.lab_report OWNER TO postgres;

--
-- Name: lab_report_lab_report_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_report_lab_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_report_lab_report_id_seq OWNER TO postgres;

--
-- Name: lab_report_lab_report_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_report_lab_report_id_seq OWNED BY hms.lab_report.lab_report_id;


--
-- Name: lab_result; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_result (
    result_id integer NOT NULL,
    lab_order_test_id integer,
    result_datetime timestamp without time zone,
    result_value text,
    reference_range text,
    abnormal_flag character varying(10),
    remarks text,
    verified_by integer,
    verified_at timestamp without time zone
);


ALTER TABLE hms.lab_result OWNER TO postgres;

--
-- Name: lab_result_result_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_result_result_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_result_result_id_seq OWNER TO postgres;

--
-- Name: lab_result_result_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_result_result_id_seq OWNED BY hms.lab_result.result_id;


--
-- Name: lab_schedule; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_schedule (
    schedule_id integer NOT NULL,
    lab_order_id integer,
    lab_id integer,
    technician_id integer,
    scheduled_datetime timestamp without time zone,
    expected_duration time without time zone,
    sample_type character varying(50),
    schedule_status character varying(30),
    home_collection boolean,
    notes text
);


ALTER TABLE hms.lab_schedule OWNER TO postgres;

--
-- Name: lab_schedule_schedule_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_schedule_schedule_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_schedule_schedule_id_seq OWNER TO postgres;

--
-- Name: lab_schedule_schedule_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_schedule_schedule_id_seq OWNED BY hms.lab_schedule.schedule_id;


--
-- Name: lab_technician; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_technician (
    technician_id integer NOT NULL,
    user_id integer,
    first_name character varying(100),
    last_name character varying(100),
    license_number character varying(50),
    phone_number character varying(20),
    email character varying(100),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.lab_technician OWNER TO postgres;

--
-- Name: lab_technician_technician_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_technician_technician_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_technician_technician_id_seq OWNER TO postgres;

--
-- Name: lab_technician_technician_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_technician_technician_id_seq OWNED BY hms.lab_technician.technician_id;


--
-- Name: lab_test; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.lab_test (
    test_id integer NOT NULL,
    test_name character varying(100),
    test_code character varying(50),
    description text,
    test_cost numeric(10,2),
    fasting_required boolean,
    expected_duration_minutes integer,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.lab_test OWNER TO postgres;

--
-- Name: lab_test_test_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.lab_test_test_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.lab_test_test_id_seq OWNER TO postgres;

--
-- Name: lab_test_test_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.lab_test_test_id_seq OWNED BY hms.lab_test.test_id;


--
-- Name: medical_record; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.medical_record (
    record_id integer NOT NULL,
    patient_id integer,
    doctor_id integer,
    visit_id integer,
    record_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    chief_complaint text,
    history_of_present_illness text,
    past_medical_history text,
    physical_examination text,
    diagnosis text,
    treatment_plan text,
    notes text
);


ALTER TABLE hms.medical_record OWNER TO postgres;

--
-- Name: medical_record_record_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.medical_record_record_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.medical_record_record_id_seq OWNER TO postgres;

--
-- Name: medical_record_record_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.medical_record_record_id_seq OWNED BY hms.medical_record.record_id;


--
-- Name: medicine; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.medicine (
    medicine_id integer NOT NULL,
    medicine_name character varying(150),
    generic_name character varying(150),
    strength character varying(50),
    form character varying(50),
    shelf_location character varying(50),
    unit_price numeric(10,2),
    is_active boolean DEFAULT true,
    min_quantity integer,
    reorder_level integer
);


ALTER TABLE hms.medicine OWNER TO postgres;

--
-- Name: medicine_batch; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.medicine_batch (
    batch_id integer NOT NULL,
    medicine_id integer,
    batch_number character varying(50),
    quantity_in_stock integer,
    manufacture_date date,
    expiry_date date,
    purchase_price numeric(10,2),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.medicine_batch OWNER TO postgres;

--
-- Name: medicine_batch_batch_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.medicine_batch_batch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.medicine_batch_batch_id_seq OWNER TO postgres;

--
-- Name: medicine_batch_batch_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.medicine_batch_batch_id_seq OWNED BY hms.medicine_batch.batch_id;


--
-- Name: medicine_medicine_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.medicine_medicine_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.medicine_medicine_id_seq OWNER TO postgres;

--
-- Name: medicine_medicine_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.medicine_medicine_id_seq OWNED BY hms.medicine.medicine_id;


--
-- Name: patient; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.patient (
    patient_id integer NOT NULL,
    hospital_id character varying(50) NOT NULL,
    first_name character varying(100),
    last_name character varying(100),
    date_of_birth date,
    gender hms.gender_enum,
    blood_group character varying(10),
    phone_number character varying(20),
    email character varying(100),
    marital_status character varying(20),
    emergency_contact_name character varying(100),
    emergency_contact_phone character varying(20),
    registration_date timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    patient_type character varying(30),
    medical_record_number character varying(50),
    user_id integer,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.patient OWNER TO postgres;

--
-- Name: patient_patient_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.patient_patient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.patient_patient_id_seq OWNER TO postgres;

--
-- Name: patient_patient_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.patient_patient_id_seq OWNED BY hms.patient.patient_id;


--
-- Name: payment; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.payment (
    payment_id integer NOT NULL,
    invoice_id integer,
    payment_datetime timestamp without time zone,
    amount_paid numeric(10,2),
    payment_mode character varying(30),
    transaction_ref character varying(100),
    status hms.payment_status_enum
);


ALTER TABLE hms.payment OWNER TO postgres;

--
-- Name: payment_payment_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.payment_payment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.payment_payment_id_seq OWNER TO postgres;

--
-- Name: payment_payment_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.payment_payment_id_seq OWNED BY hms.payment.payment_id;


--
-- Name: pharmacist; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.pharmacist (
    pharmacist_id integer NOT NULL,
    user_id integer,
    first_name character varying(100),
    last_name character varying(100),
    employee_code character varying(50),
    license_number character varying(50),
    phone_number character varying(20),
    email character varying(100),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.pharmacist OWNER TO postgres;

--
-- Name: pharmacist_pharmacist_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.pharmacist_pharmacist_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.pharmacist_pharmacist_id_seq OWNER TO postgres;

--
-- Name: pharmacist_pharmacist_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.pharmacist_pharmacist_id_seq OWNED BY hms.pharmacist.pharmacist_id;


--
-- Name: prescription; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.prescription (
    prescription_id integer NOT NULL,
    record_id integer,
    patient_id integer,
    doctor_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    status character varying(30),
    notes text
);


ALTER TABLE hms.prescription OWNER TO postgres;

--
-- Name: prescription_item; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.prescription_item (
    prescription_item_id integer NOT NULL,
    prescription_id integer,
    medicine_id integer,
    prescribed_quantity integer,
    dosage character varying(50),
    frequency character varying(50),
    duration_days integer,
    instructions text
);


ALTER TABLE hms.prescription_item OWNER TO postgres;

--
-- Name: prescription_item_prescription_item_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.prescription_item_prescription_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.prescription_item_prescription_item_id_seq OWNER TO postgres;

--
-- Name: prescription_item_prescription_item_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.prescription_item_prescription_item_id_seq OWNED BY hms.prescription_item.prescription_item_id;


--
-- Name: prescription_prescription_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.prescription_prescription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.prescription_prescription_id_seq OWNER TO postgres;

--
-- Name: prescription_prescription_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.prescription_prescription_id_seq OWNED BY hms.prescription.prescription_id;


--
-- Name: purchase_order; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.purchase_order (
    purchase_id integer NOT NULL,
    po_number character varying(50),
    order_date date,
    supplier_id integer,
    total_amount numeric(12,2),
    status character varying(30),
    created_by integer,
    expected_delivery_date date
);


ALTER TABLE hms.purchase_order OWNER TO postgres;

--
-- Name: purchase_order_item; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.purchase_order_item (
    po_item_id integer NOT NULL,
    purchase_id integer,
    item_id integer,
    ordered_quantity integer,
    received_quantity integer,
    unit_price numeric(10,2),
    line_total numeric(10,2),
    expiry_date date
);


ALTER TABLE hms.purchase_order_item OWNER TO postgres;

--
-- Name: purchase_order_item_po_item_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.purchase_order_item_po_item_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.purchase_order_item_po_item_id_seq OWNER TO postgres;

--
-- Name: purchase_order_item_po_item_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.purchase_order_item_po_item_id_seq OWNED BY hms.purchase_order_item.po_item_id;


--
-- Name: purchase_order_purchase_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.purchase_order_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.purchase_order_purchase_id_seq OWNER TO postgres;

--
-- Name: purchase_order_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.purchase_order_purchase_id_seq OWNED BY hms.purchase_order.purchase_id;


--
-- Name: report; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.report (
    report_id integer NOT NULL,
    record_id integer,
    report_type character varying(50),
    report_date date,
    findings text,
    file_url text
);


ALTER TABLE hms.report OWNER TO postgres;

--
-- Name: report_report_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.report_report_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.report_report_id_seq OWNER TO postgres;

--
-- Name: report_report_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.report_report_id_seq OWNED BY hms.report.report_id;


--
-- Name: role; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.role (
    role_id integer NOT NULL,
    role_name character varying(50) NOT NULL,
    description text
);


ALTER TABLE hms.role OWNER TO postgres;

--
-- Name: role_role_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.role_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.role_role_id_seq OWNER TO postgres;

--
-- Name: role_role_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.role_role_id_seq OWNED BY hms.role.role_id;


--
-- Name: service_master; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.service_master (
    service_id integer NOT NULL,
    service_code character varying(50),
    service_name character varying(150),
    category character varying(50),
    standard_price numeric(10,2),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.service_master OWNER TO postgres;

--
-- Name: service_master_service_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.service_master_service_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.service_master_service_id_seq OWNER TO postgres;

--
-- Name: service_master_service_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.service_master_service_id_seq OWNED BY hms.service_master.service_id;


--
-- Name: specialization; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.specialization (
    specialization_id integer NOT NULL,
    specialization_name character varying(100),
    description text,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.specialization OWNER TO postgres;

--
-- Name: specialization_specialization_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.specialization_specialization_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.specialization_specialization_id_seq OWNER TO postgres;

--
-- Name: specialization_specialization_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.specialization_specialization_id_seq OWNED BY hms.specialization.specialization_id;


--
-- Name: stock; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.stock (
    stock_id integer NOT NULL,
    item_id integer,
    location_id integer,
    quantity_available integer,
    reserved_quantity integer,
    last_updated timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.stock OWNER TO postgres;

--
-- Name: stock_adjustment; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.stock_adjustment (
    adjustment_id integer NOT NULL,
    adjustment_number character varying(50),
    item_id integer,
    location_id integer,
    adjustment_type character varying(30),
    quantity_before integer,
    quantity_after integer,
    quantity_changed integer,
    reason text,
    adjustment_datetime timestamp without time zone,
    adjusted_by integer
);


ALTER TABLE hms.stock_adjustment OWNER TO postgres;

--
-- Name: stock_adjustment_adjustment_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.stock_adjustment_adjustment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.stock_adjustment_adjustment_id_seq OWNER TO postgres;

--
-- Name: stock_adjustment_adjustment_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.stock_adjustment_adjustment_id_seq OWNED BY hms.stock_adjustment.adjustment_id;


--
-- Name: stock_audit; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.stock_audit (
    audit_id integer NOT NULL,
    audit_number character varying(50),
    location_id integer,
    audit_date date,
    remarks text,
    conducted_by integer,
    status character varying(30)
);


ALTER TABLE hms.stock_audit OWNER TO postgres;

--
-- Name: stock_audit_audit_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.stock_audit_audit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.stock_audit_audit_id_seq OWNER TO postgres;

--
-- Name: stock_audit_audit_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.stock_audit_audit_id_seq OWNED BY hms.stock_audit.audit_id;


--
-- Name: stock_audit_details; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.stock_audit_details (
    audit_detail_id integer NOT NULL,
    audit_id integer,
    item_id integer,
    system_quantity integer,
    physical_quantity integer,
    difference integer,
    remarks text
);


ALTER TABLE hms.stock_audit_details OWNER TO postgres;

--
-- Name: stock_audit_details_audit_detail_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.stock_audit_details_audit_detail_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.stock_audit_details_audit_detail_id_seq OWNER TO postgres;

--
-- Name: stock_audit_details_audit_detail_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.stock_audit_details_audit_detail_id_seq OWNED BY hms.stock_audit_details.audit_detail_id;


--
-- Name: stock_stock_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.stock_stock_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.stock_stock_id_seq OWNER TO postgres;

--
-- Name: stock_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.stock_stock_id_seq OWNED BY hms.stock.stock_id;


--
-- Name: stock_transfer; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.stock_transfer (
    transfer_id integer NOT NULL,
    transfer_number character varying(50),
    item_id integer,
    from_location_id integer,
    to_location_id integer,
    quantity integer,
    transfer_datetime timestamp without time zone,
    initiated_by integer,
    approved_by integer,
    status character varying(30)
);


ALTER TABLE hms.stock_transfer OWNER TO postgres;

--
-- Name: stock_transfer_transfer_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.stock_transfer_transfer_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.stock_transfer_transfer_id_seq OWNER TO postgres;

--
-- Name: stock_transfer_transfer_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.stock_transfer_transfer_id_seq OWNED BY hms.stock_transfer.transfer_id;


--
-- Name: store_location; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.store_location (
    location_id integer NOT NULL,
    location_name character varying(100),
    location_code character varying(50),
    location_type character varying(50),
    is_active boolean DEFAULT true
);


ALTER TABLE hms.store_location OWNER TO postgres;

--
-- Name: store_location_location_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.store_location_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.store_location_location_id_seq OWNER TO postgres;

--
-- Name: store_location_location_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.store_location_location_id_seq OWNED BY hms.store_location.location_id;


--
-- Name: supplier; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.supplier (
    supplier_id integer NOT NULL,
    supplier_name character varying(150),
    supplier_code character varying(50),
    contact_person character varying(100),
    phone_number character varying(20),
    email character varying(100),
    address text,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.supplier OWNER TO postgres;

--
-- Name: supplier_supplier_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.supplier_supplier_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.supplier_supplier_id_seq OWNER TO postgres;

--
-- Name: supplier_supplier_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.supplier_supplier_id_seq OWNED BY hms.supplier.supplier_id;


--
-- Name: tax; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.tax (
    tax_id integer NOT NULL,
    tax_code character varying(30),
    tax_name character varying(100),
    tax_rate numeric(5,2),
    account_id integer,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.tax OWNER TO postgres;

--
-- Name: tax_tax_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.tax_tax_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.tax_tax_id_seq OWNER TO postgres;

--
-- Name: tax_tax_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.tax_tax_id_seq OWNED BY hms.tax.tax_id;


--
-- Name: user_role; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.user_role (
    user_role_id integer NOT NULL,
    user_id integer,
    role_id integer,
    assigned_date date DEFAULT CURRENT_DATE
);


ALTER TABLE hms.user_role OWNER TO postgres;

--
-- Name: user_role_user_role_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.user_role_user_role_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.user_role_user_role_id_seq OWNER TO postgres;

--
-- Name: user_role_user_role_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.user_role_user_role_id_seq OWNED BY hms.user_role.user_role_id;


--
-- Name: users; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.users (
    user_id integer NOT NULL,
    username character varying(50) NOT NULL,
    password_hash text NOT NULL,
    email character varying(100) NOT NULL,
    full_name character varying(150),
    status character varying(30),
    department_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_login timestamp without time zone
);


ALTER TABLE hms.users OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.users_user_id_seq OWNER TO postgres;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.users_user_id_seq OWNED BY hms.users.user_id;


--
-- Name: vendor; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.vendor (
    vendor_id integer NOT NULL,
    vendor_name character varying(150),
    vendor_code character varying(50),
    contact_person character varying(100),
    phone_number character varying(20),
    email character varying(100),
    gst_number character varying(30),
    address text,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.vendor OWNER TO postgres;

--
-- Name: vendor_vendor_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.vendor_vendor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.vendor_vendor_id_seq OWNER TO postgres;

--
-- Name: vendor_vendor_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.vendor_vendor_id_seq OWNED BY hms.vendor.vendor_id;


--
-- Name: visit; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.visit (
    visit_id integer NOT NULL,
    patient_id integer,
    doctor_id integer,
    visit_type hms.visit_type_enum,
    visit_datetime timestamp without time zone,
    chief_complaint text,
    status hms.common_status_enum,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE hms.visit OWNER TO postgres;

--
-- Name: visit_visit_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.visit_visit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.visit_visit_id_seq OWNER TO postgres;

--
-- Name: visit_visit_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.visit_visit_id_seq OWNED BY hms.visit.visit_id;


--
-- Name: waiting_list; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.waiting_list (
    waiting_id integer NOT NULL,
    patient_id integer,
    doctor_id integer,
    preferred_date date,
    preferred_time_start time without time zone,
    preferred_time_end time without time zone,
    reason text,
    status character varying(30),
    added_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    notified_at timestamp without time zone,
    expires_at timestamp without time zone
);


ALTER TABLE hms.waiting_list OWNER TO postgres;

--
-- Name: waiting_list_waiting_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.waiting_list_waiting_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.waiting_list_waiting_id_seq OWNER TO postgres;

--
-- Name: waiting_list_waiting_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.waiting_list_waiting_id_seq OWNED BY hms.waiting_list.waiting_id;


--
-- Name: ward; Type: TABLE; Schema: hms; Owner: postgres
--

CREATE TABLE hms.ward (
    ward_id integer NOT NULL,
    ward_name character varying(100),
    ward_type character varying(50),
    total_beds integer,
    available_beds integer,
    is_active boolean DEFAULT true
);


ALTER TABLE hms.ward OWNER TO postgres;

--
-- Name: ward_ward_id_seq; Type: SEQUENCE; Schema: hms; Owner: postgres
--

CREATE SEQUENCE hms.ward_ward_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE hms.ward_ward_id_seq OWNER TO postgres;

--
-- Name: ward_ward_id_seq; Type: SEQUENCE OWNED BY; Schema: hms; Owner: postgres
--

ALTER SEQUENCE hms.ward_ward_id_seq OWNED BY hms.ward.ward_id;


--
-- Name: account account_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.account ALTER COLUMN account_id SET DEFAULT nextval('hms.account_account_id_seq'::regclass);


--
-- Name: address address_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.address ALTER COLUMN address_id SET DEFAULT nextval('hms.address_address_id_seq'::regclass);


--
-- Name: admission admission_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.admission ALTER COLUMN admission_id SET DEFAULT nextval('hms.admission_admission_id_seq'::regclass);


--
-- Name: appointment appointment_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('hms.appointment_appointment_id_seq'::regclass);


--
-- Name: appointment_history history_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_history ALTER COLUMN history_id SET DEFAULT nextval('hms.appointment_history_history_id_seq'::regclass);


--
-- Name: appointment_reminder reminder_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_reminder ALTER COLUMN reminder_id SET DEFAULT nextval('hms.appointment_reminder_reminder_id_seq'::regclass);


--
-- Name: asset asset_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.asset ALTER COLUMN asset_id SET DEFAULT nextval('hms.asset_asset_id_seq'::regclass);


--
-- Name: audit_log log_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.audit_log ALTER COLUMN log_id SET DEFAULT nextval('hms.audit_log_log_id_seq'::regclass);


--
-- Name: bank_account bank_account_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bank_account ALTER COLUMN bank_account_id SET DEFAULT nextval('hms.bank_account_bank_account_id_seq'::regclass);


--
-- Name: bill bill_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill ALTER COLUMN bill_id SET DEFAULT nextval('hms.bill_bill_id_seq'::regclass);


--
-- Name: bill_line bill_line_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_line ALTER COLUMN bill_line_id SET DEFAULT nextval('hms.bill_line_bill_line_id_seq'::regclass);


--
-- Name: bill_payment bill_payment_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_payment ALTER COLUMN bill_payment_id SET DEFAULT nextval('hms.bill_payment_bill_payment_id_seq'::regclass);


--
-- Name: blocked_slots blocked_slot_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.blocked_slots ALTER COLUMN blocked_slot_id SET DEFAULT nextval('hms.blocked_slots_blocked_slot_id_seq'::regclass);


--
-- Name: budget budget_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget ALTER COLUMN budget_id SET DEFAULT nextval('hms.budget_budget_id_seq'::regclass);


--
-- Name: budget_line budget_line_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget_line ALTER COLUMN budget_line_id SET DEFAULT nextval('hms.budget_line_budget_line_id_seq'::regclass);


--
-- Name: category category_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.category ALTER COLUMN category_id SET DEFAULT nextval('hms.category_category_id_seq'::regclass);


--
-- Name: department department_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.department ALTER COLUMN department_id SET DEFAULT nextval('hms.department_department_id_seq'::regclass);


--
-- Name: depreciation depreciation_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.depreciation ALTER COLUMN depreciation_id SET DEFAULT nextval('hms.depreciation_depreciation_id_seq'::regclass);


--
-- Name: dispense dispense_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense ALTER COLUMN dispense_id SET DEFAULT nextval('hms.dispense_dispense_id_seq'::regclass);


--
-- Name: dispense_item dispense_item_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense_item ALTER COLUMN dispense_item_id SET DEFAULT nextval('hms.dispense_item_dispense_item_id_seq'::regclass);


--
-- Name: doctor doctor_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor ALTER COLUMN doctor_id SET DEFAULT nextval('hms.doctor_doctor_id_seq'::regclass);


--
-- Name: doctor_schedule schedule_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor_schedule ALTER COLUMN schedule_id SET DEFAULT nextval('hms.doctor_schedule_schedule_id_seq'::regclass);


--
-- Name: expense expense_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense ALTER COLUMN expense_id SET DEFAULT nextval('hms.expense_expense_id_seq'::regclass);


--
-- Name: goods_receipt receipt_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.goods_receipt ALTER COLUMN receipt_id SET DEFAULT nextval('hms.goods_receipt_receipt_id_seq'::regclass);


--
-- Name: insurance insurance_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance ALTER COLUMN insurance_id SET DEFAULT nextval('hms.insurance_insurance_id_seq'::regclass);


--
-- Name: insurance_provider provider_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance_provider ALTER COLUMN provider_id SET DEFAULT nextval('hms.insurance_provider_provider_id_seq'::regclass);


--
-- Name: invoice invoice_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice ALTER COLUMN invoice_id SET DEFAULT nextval('hms.invoice_invoice_id_seq'::regclass);


--
-- Name: invoice_line_item line_item_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice_line_item ALTER COLUMN line_item_id SET DEFAULT nextval('hms.invoice_line_item_line_item_id_seq'::regclass);


--
-- Name: issue_details issue_detail_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_details ALTER COLUMN issue_detail_id SET DEFAULT nextval('hms.issue_details_issue_detail_id_seq'::regclass);


--
-- Name: issue_request request_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request ALTER COLUMN request_id SET DEFAULT nextval('hms.issue_request_request_id_seq'::regclass);


--
-- Name: item item_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.item ALTER COLUMN item_id SET DEFAULT nextval('hms.item_item_id_seq'::regclass);


--
-- Name: journal_entry journal_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_entry ALTER COLUMN journal_id SET DEFAULT nextval('hms.journal_entry_journal_id_seq'::regclass);


--
-- Name: journal_line journal_line_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_line ALTER COLUMN journal_line_id SET DEFAULT nextval('hms.journal_line_journal_line_id_seq'::regclass);


--
-- Name: lab lab_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab ALTER COLUMN lab_id SET DEFAULT nextval('hms.lab_lab_id_seq'::regclass);


--
-- Name: lab_order lab_order_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order ALTER COLUMN lab_order_id SET DEFAULT nextval('hms.lab_order_lab_order_id_seq'::regclass);


--
-- Name: lab_order_test lab_order_test_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order_test ALTER COLUMN lab_order_test_id SET DEFAULT nextval('hms.lab_order_test_lab_order_test_id_seq'::regclass);


--
-- Name: lab_report lab_report_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_report ALTER COLUMN lab_report_id SET DEFAULT nextval('hms.lab_report_lab_report_id_seq'::regclass);


--
-- Name: lab_result result_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_result ALTER COLUMN result_id SET DEFAULT nextval('hms.lab_result_result_id_seq'::regclass);


--
-- Name: lab_schedule schedule_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_schedule ALTER COLUMN schedule_id SET DEFAULT nextval('hms.lab_schedule_schedule_id_seq'::regclass);


--
-- Name: lab_technician technician_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_technician ALTER COLUMN technician_id SET DEFAULT nextval('hms.lab_technician_technician_id_seq'::regclass);


--
-- Name: lab_test test_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_test ALTER COLUMN test_id SET DEFAULT nextval('hms.lab_test_test_id_seq'::regclass);


--
-- Name: medical_record record_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medical_record ALTER COLUMN record_id SET DEFAULT nextval('hms.medical_record_record_id_seq'::regclass);


--
-- Name: medicine medicine_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine ALTER COLUMN medicine_id SET DEFAULT nextval('hms.medicine_medicine_id_seq'::regclass);


--
-- Name: medicine_batch batch_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine_batch ALTER COLUMN batch_id SET DEFAULT nextval('hms.medicine_batch_batch_id_seq'::regclass);


--
-- Name: patient patient_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.patient ALTER COLUMN patient_id SET DEFAULT nextval('hms.patient_patient_id_seq'::regclass);


--
-- Name: payment payment_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.payment ALTER COLUMN payment_id SET DEFAULT nextval('hms.payment_payment_id_seq'::regclass);


--
-- Name: pharmacist pharmacist_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.pharmacist ALTER COLUMN pharmacist_id SET DEFAULT nextval('hms.pharmacist_pharmacist_id_seq'::regclass);


--
-- Name: prescription prescription_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription ALTER COLUMN prescription_id SET DEFAULT nextval('hms.prescription_prescription_id_seq'::regclass);


--
-- Name: prescription_item prescription_item_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription_item ALTER COLUMN prescription_item_id SET DEFAULT nextval('hms.prescription_item_prescription_item_id_seq'::regclass);


--
-- Name: purchase_order purchase_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order ALTER COLUMN purchase_id SET DEFAULT nextval('hms.purchase_order_purchase_id_seq'::regclass);


--
-- Name: purchase_order_item po_item_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order_item ALTER COLUMN po_item_id SET DEFAULT nextval('hms.purchase_order_item_po_item_id_seq'::regclass);


--
-- Name: report report_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.report ALTER COLUMN report_id SET DEFAULT nextval('hms.report_report_id_seq'::regclass);


--
-- Name: role role_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.role ALTER COLUMN role_id SET DEFAULT nextval('hms.role_role_id_seq'::regclass);


--
-- Name: service_master service_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.service_master ALTER COLUMN service_id SET DEFAULT nextval('hms.service_master_service_id_seq'::regclass);


--
-- Name: specialization specialization_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.specialization ALTER COLUMN specialization_id SET DEFAULT nextval('hms.specialization_specialization_id_seq'::regclass);


--
-- Name: stock stock_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock ALTER COLUMN stock_id SET DEFAULT nextval('hms.stock_stock_id_seq'::regclass);


--
-- Name: stock_adjustment adjustment_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment ALTER COLUMN adjustment_id SET DEFAULT nextval('hms.stock_adjustment_adjustment_id_seq'::regclass);


--
-- Name: stock_audit audit_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit ALTER COLUMN audit_id SET DEFAULT nextval('hms.stock_audit_audit_id_seq'::regclass);


--
-- Name: stock_audit_details audit_detail_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit_details ALTER COLUMN audit_detail_id SET DEFAULT nextval('hms.stock_audit_details_audit_detail_id_seq'::regclass);


--
-- Name: stock_transfer transfer_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer ALTER COLUMN transfer_id SET DEFAULT nextval('hms.stock_transfer_transfer_id_seq'::regclass);


--
-- Name: store_location location_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.store_location ALTER COLUMN location_id SET DEFAULT nextval('hms.store_location_location_id_seq'::regclass);


--
-- Name: supplier supplier_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.supplier ALTER COLUMN supplier_id SET DEFAULT nextval('hms.supplier_supplier_id_seq'::regclass);


--
-- Name: tax tax_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.tax ALTER COLUMN tax_id SET DEFAULT nextval('hms.tax_tax_id_seq'::regclass);


--
-- Name: user_role user_role_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.user_role ALTER COLUMN user_role_id SET DEFAULT nextval('hms.user_role_user_role_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.users ALTER COLUMN user_id SET DEFAULT nextval('hms.users_user_id_seq'::regclass);


--
-- Name: vendor vendor_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.vendor ALTER COLUMN vendor_id SET DEFAULT nextval('hms.vendor_vendor_id_seq'::regclass);


--
-- Name: visit visit_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.visit ALTER COLUMN visit_id SET DEFAULT nextval('hms.visit_visit_id_seq'::regclass);


--
-- Name: waiting_list waiting_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.waiting_list ALTER COLUMN waiting_id SET DEFAULT nextval('hms.waiting_list_waiting_id_seq'::regclass);


--
-- Name: ward ward_id; Type: DEFAULT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.ward ALTER COLUMN ward_id SET DEFAULT nextval('hms.ward_ward_id_seq'::regclass);


--
-- Name: account account_account_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.account
    ADD CONSTRAINT account_account_code_key UNIQUE (account_code);


--
-- Name: account account_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.account
    ADD CONSTRAINT account_pkey PRIMARY KEY (account_id);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (address_id);


--
-- Name: admission admission_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.admission
    ADD CONSTRAINT admission_pkey PRIMARY KEY (admission_id);


--
-- Name: appointment_history appointment_history_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_history
    ADD CONSTRAINT appointment_history_pkey PRIMARY KEY (history_id);


--
-- Name: appointment appointment_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
-- Name: appointment_reminder appointment_reminder_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_reminder
    ADD CONSTRAINT appointment_reminder_pkey PRIMARY KEY (reminder_id);


--
-- Name: asset asset_asset_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.asset
    ADD CONSTRAINT asset_asset_code_key UNIQUE (asset_code);


--
-- Name: asset asset_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.asset
    ADD CONSTRAINT asset_pkey PRIMARY KEY (asset_id);


--
-- Name: audit_log audit_log_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.audit_log
    ADD CONSTRAINT audit_log_pkey PRIMARY KEY (log_id);


--
-- Name: bank_account bank_account_account_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bank_account
    ADD CONSTRAINT bank_account_account_number_key UNIQUE (account_number);


--
-- Name: bank_account bank_account_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bank_account
    ADD CONSTRAINT bank_account_pkey PRIMARY KEY (bank_account_id);


--
-- Name: bill bill_bill_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill
    ADD CONSTRAINT bill_bill_number_key UNIQUE (bill_number);


--
-- Name: bill_line bill_line_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_line
    ADD CONSTRAINT bill_line_pkey PRIMARY KEY (bill_line_id);


--
-- Name: bill_payment bill_payment_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_payment
    ADD CONSTRAINT bill_payment_pkey PRIMARY KEY (bill_payment_id);


--
-- Name: bill bill_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill
    ADD CONSTRAINT bill_pkey PRIMARY KEY (bill_id);


--
-- Name: blocked_slots blocked_slots_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.blocked_slots
    ADD CONSTRAINT blocked_slots_pkey PRIMARY KEY (blocked_slot_id);


--
-- Name: budget_line budget_line_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget_line
    ADD CONSTRAINT budget_line_pkey PRIMARY KEY (budget_line_id);


--
-- Name: budget budget_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget
    ADD CONSTRAINT budget_pkey PRIMARY KEY (budget_id);


--
-- Name: category category_category_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.category
    ADD CONSTRAINT category_category_name_key UNIQUE (category_name);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.category
    ADD CONSTRAINT category_pkey PRIMARY KEY (category_id);


--
-- Name: department department_department_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.department
    ADD CONSTRAINT department_department_code_key UNIQUE (department_code);


--
-- Name: department department_department_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.department
    ADD CONSTRAINT department_department_name_key UNIQUE (department_name);


--
-- Name: department department_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.department
    ADD CONSTRAINT department_pkey PRIMARY KEY (department_id);


--
-- Name: depreciation depreciation_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.depreciation
    ADD CONSTRAINT depreciation_pkey PRIMARY KEY (depreciation_id);


--
-- Name: dispense_item dispense_item_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense_item
    ADD CONSTRAINT dispense_item_pkey PRIMARY KEY (dispense_item_id);


--
-- Name: dispense dispense_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense
    ADD CONSTRAINT dispense_pkey PRIMARY KEY (dispense_id);


--
-- Name: doctor doctor_license_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor
    ADD CONSTRAINT doctor_license_number_key UNIQUE (license_number);


--
-- Name: doctor doctor_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor
    ADD CONSTRAINT doctor_pkey PRIMARY KEY (doctor_id);


--
-- Name: doctor_schedule doctor_schedule_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor_schedule
    ADD CONSTRAINT doctor_schedule_pkey PRIMARY KEY (schedule_id);


--
-- Name: expense expense_expense_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense
    ADD CONSTRAINT expense_expense_number_key UNIQUE (expense_number);


--
-- Name: expense expense_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense
    ADD CONSTRAINT expense_pkey PRIMARY KEY (expense_id);


--
-- Name: goods_receipt goods_receipt_grn_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.goods_receipt
    ADD CONSTRAINT goods_receipt_grn_number_key UNIQUE (grn_number);


--
-- Name: goods_receipt goods_receipt_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.goods_receipt
    ADD CONSTRAINT goods_receipt_pkey PRIMARY KEY (receipt_id);


--
-- Name: insurance insurance_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance
    ADD CONSTRAINT insurance_pkey PRIMARY KEY (insurance_id);


--
-- Name: insurance insurance_policy_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance
    ADD CONSTRAINT insurance_policy_number_key UNIQUE (policy_number);


--
-- Name: insurance_provider insurance_provider_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance_provider
    ADD CONSTRAINT insurance_provider_pkey PRIMARY KEY (provider_id);


--
-- Name: invoice_line_item invoice_line_item_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice_line_item
    ADD CONSTRAINT invoice_line_item_pkey PRIMARY KEY (line_item_id);


--
-- Name: invoice invoice_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice
    ADD CONSTRAINT invoice_pkey PRIMARY KEY (invoice_id);


--
-- Name: issue_details issue_details_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_details
    ADD CONSTRAINT issue_details_pkey PRIMARY KEY (issue_detail_id);


--
-- Name: issue_request issue_request_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request
    ADD CONSTRAINT issue_request_pkey PRIMARY KEY (request_id);


--
-- Name: issue_request issue_request_request_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request
    ADD CONSTRAINT issue_request_request_number_key UNIQUE (request_number);


--
-- Name: item item_item_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.item
    ADD CONSTRAINT item_item_code_key UNIQUE (item_code);


--
-- Name: item item_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.item
    ADD CONSTRAINT item_pkey PRIMARY KEY (item_id);


--
-- Name: journal_entry journal_entry_journal_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_entry
    ADD CONSTRAINT journal_entry_journal_number_key UNIQUE (journal_number);


--
-- Name: journal_entry journal_entry_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_entry
    ADD CONSTRAINT journal_entry_pkey PRIMARY KEY (journal_id);


--
-- Name: journal_line journal_line_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_line
    ADD CONSTRAINT journal_line_pkey PRIMARY KEY (journal_line_id);


--
-- Name: lab lab_lab_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab
    ADD CONSTRAINT lab_lab_code_key UNIQUE (lab_code);


--
-- Name: lab lab_lab_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab
    ADD CONSTRAINT lab_lab_name_key UNIQUE (lab_name);


--
-- Name: lab_order lab_order_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order
    ADD CONSTRAINT lab_order_pkey PRIMARY KEY (lab_order_id);


--
-- Name: lab_order_test lab_order_test_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order_test
    ADD CONSTRAINT lab_order_test_pkey PRIMARY KEY (lab_order_test_id);


--
-- Name: lab lab_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab
    ADD CONSTRAINT lab_pkey PRIMARY KEY (lab_id);


--
-- Name: lab_report lab_report_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_report
    ADD CONSTRAINT lab_report_pkey PRIMARY KEY (lab_report_id);


--
-- Name: lab_result lab_result_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_result
    ADD CONSTRAINT lab_result_pkey PRIMARY KEY (result_id);


--
-- Name: lab_schedule lab_schedule_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_schedule
    ADD CONSTRAINT lab_schedule_pkey PRIMARY KEY (schedule_id);


--
-- Name: lab_technician lab_technician_license_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_technician
    ADD CONSTRAINT lab_technician_license_number_key UNIQUE (license_number);


--
-- Name: lab_technician lab_technician_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_technician
    ADD CONSTRAINT lab_technician_pkey PRIMARY KEY (technician_id);


--
-- Name: lab_test lab_test_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_test
    ADD CONSTRAINT lab_test_pkey PRIMARY KEY (test_id);


--
-- Name: lab_test lab_test_test_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_test
    ADD CONSTRAINT lab_test_test_code_key UNIQUE (test_code);


--
-- Name: medical_record medical_record_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medical_record
    ADD CONSTRAINT medical_record_pkey PRIMARY KEY (record_id);


--
-- Name: medicine_batch medicine_batch_batch_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine_batch
    ADD CONSTRAINT medicine_batch_batch_number_key UNIQUE (batch_number);


--
-- Name: medicine_batch medicine_batch_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine_batch
    ADD CONSTRAINT medicine_batch_pkey PRIMARY KEY (batch_id);


--
-- Name: medicine medicine_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine
    ADD CONSTRAINT medicine_pkey PRIMARY KEY (medicine_id);


--
-- Name: patient patient_hospital_id_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.patient
    ADD CONSTRAINT patient_hospital_id_key UNIQUE (hospital_id);


--
-- Name: patient patient_medical_record_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.patient
    ADD CONSTRAINT patient_medical_record_number_key UNIQUE (medical_record_number);


--
-- Name: patient patient_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.patient
    ADD CONSTRAINT patient_pkey PRIMARY KEY (patient_id);


--
-- Name: payment payment_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.payment
    ADD CONSTRAINT payment_pkey PRIMARY KEY (payment_id);


--
-- Name: pharmacist pharmacist_employee_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.pharmacist
    ADD CONSTRAINT pharmacist_employee_code_key UNIQUE (employee_code);


--
-- Name: pharmacist pharmacist_license_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.pharmacist
    ADD CONSTRAINT pharmacist_license_number_key UNIQUE (license_number);


--
-- Name: pharmacist pharmacist_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.pharmacist
    ADD CONSTRAINT pharmacist_pkey PRIMARY KEY (pharmacist_id);


--
-- Name: prescription_item prescription_item_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription_item
    ADD CONSTRAINT prescription_item_pkey PRIMARY KEY (prescription_item_id);


--
-- Name: prescription prescription_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription
    ADD CONSTRAINT prescription_pkey PRIMARY KEY (prescription_id);


--
-- Name: purchase_order_item purchase_order_item_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order_item
    ADD CONSTRAINT purchase_order_item_pkey PRIMARY KEY (po_item_id);


--
-- Name: purchase_order purchase_order_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order
    ADD CONSTRAINT purchase_order_pkey PRIMARY KEY (purchase_id);


--
-- Name: purchase_order purchase_order_po_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order
    ADD CONSTRAINT purchase_order_po_number_key UNIQUE (po_number);


--
-- Name: report report_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.report
    ADD CONSTRAINT report_pkey PRIMARY KEY (report_id);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (role_id);


--
-- Name: role role_role_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.role
    ADD CONSTRAINT role_role_name_key UNIQUE (role_name);


--
-- Name: service_master service_master_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.service_master
    ADD CONSTRAINT service_master_pkey PRIMARY KEY (service_id);


--
-- Name: service_master service_master_service_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.service_master
    ADD CONSTRAINT service_master_service_code_key UNIQUE (service_code);


--
-- Name: specialization specialization_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.specialization
    ADD CONSTRAINT specialization_pkey PRIMARY KEY (specialization_id);


--
-- Name: specialization specialization_specialization_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.specialization
    ADD CONSTRAINT specialization_specialization_name_key UNIQUE (specialization_name);


--
-- Name: stock_adjustment stock_adjustment_adjustment_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment
    ADD CONSTRAINT stock_adjustment_adjustment_number_key UNIQUE (adjustment_number);


--
-- Name: stock_adjustment stock_adjustment_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment
    ADD CONSTRAINT stock_adjustment_pkey PRIMARY KEY (adjustment_id);


--
-- Name: stock_audit stock_audit_audit_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit
    ADD CONSTRAINT stock_audit_audit_number_key UNIQUE (audit_number);


--
-- Name: stock_audit_details stock_audit_details_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit_details
    ADD CONSTRAINT stock_audit_details_pkey PRIMARY KEY (audit_detail_id);


--
-- Name: stock_audit stock_audit_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit
    ADD CONSTRAINT stock_audit_pkey PRIMARY KEY (audit_id);


--
-- Name: stock stock_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock
    ADD CONSTRAINT stock_pkey PRIMARY KEY (stock_id);


--
-- Name: stock_transfer stock_transfer_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_pkey PRIMARY KEY (transfer_id);


--
-- Name: stock_transfer stock_transfer_transfer_number_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_transfer_number_key UNIQUE (transfer_number);


--
-- Name: store_location store_location_location_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.store_location
    ADD CONSTRAINT store_location_location_code_key UNIQUE (location_code);


--
-- Name: store_location store_location_location_name_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.store_location
    ADD CONSTRAINT store_location_location_name_key UNIQUE (location_name);


--
-- Name: store_location store_location_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.store_location
    ADD CONSTRAINT store_location_pkey PRIMARY KEY (location_id);


--
-- Name: supplier supplier_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.supplier
    ADD CONSTRAINT supplier_pkey PRIMARY KEY (supplier_id);


--
-- Name: supplier supplier_supplier_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.supplier
    ADD CONSTRAINT supplier_supplier_code_key UNIQUE (supplier_code);


--
-- Name: tax tax_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.tax
    ADD CONSTRAINT tax_pkey PRIMARY KEY (tax_id);


--
-- Name: tax tax_tax_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.tax
    ADD CONSTRAINT tax_tax_code_key UNIQUE (tax_code);


--
-- Name: user_role user_role_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.user_role
    ADD CONSTRAINT user_role_pkey PRIMARY KEY (user_role_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: vendor vendor_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.vendor
    ADD CONSTRAINT vendor_pkey PRIMARY KEY (vendor_id);


--
-- Name: vendor vendor_vendor_code_key; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.vendor
    ADD CONSTRAINT vendor_vendor_code_key UNIQUE (vendor_code);


--
-- Name: visit visit_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.visit
    ADD CONSTRAINT visit_pkey PRIMARY KEY (visit_id);


--
-- Name: waiting_list waiting_list_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.waiting_list
    ADD CONSTRAINT waiting_list_pkey PRIMARY KEY (waiting_id);


--
-- Name: ward ward_pkey; Type: CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.ward
    ADD CONSTRAINT ward_pkey PRIMARY KEY (ward_id);


--
-- Name: account account_parent_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.account
    ADD CONSTRAINT account_parent_account_id_fkey FOREIGN KEY (parent_account_id) REFERENCES hms.account(account_id);


--
-- Name: address address_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.address
    ADD CONSTRAINT address_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id) ON DELETE CASCADE;


--
-- Name: admission admission_visit_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.admission
    ADD CONSTRAINT admission_visit_id_fkey FOREIGN KEY (visit_id) REFERENCES hms.visit(visit_id);


--
-- Name: admission admission_ward_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.admission
    ADD CONSTRAINT admission_ward_id_fkey FOREIGN KEY (ward_id) REFERENCES hms.ward(ward_id);


--
-- Name: appointment appointment_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment
    ADD CONSTRAINT appointment_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: appointment_history appointment_history_appointment_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_history
    ADD CONSTRAINT appointment_history_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES hms.appointment(appointment_id);


--
-- Name: appointment_history appointment_history_changed_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_history
    ADD CONSTRAINT appointment_history_changed_by_fkey FOREIGN KEY (changed_by) REFERENCES hms.users(user_id);


--
-- Name: appointment appointment_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment
    ADD CONSTRAINT appointment_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: appointment_reminder appointment_reminder_appointment_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.appointment_reminder
    ADD CONSTRAINT appointment_reminder_appointment_id_fkey FOREIGN KEY (appointment_id) REFERENCES hms.appointment(appointment_id);


--
-- Name: asset asset_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.asset
    ADD CONSTRAINT asset_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: audit_log audit_log_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.audit_log
    ADD CONSTRAINT audit_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: bank_account bank_account_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bank_account
    ADD CONSTRAINT bank_account_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: bill_line bill_line_bill_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_line
    ADD CONSTRAINT bill_line_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES hms.bill(bill_id);


--
-- Name: bill_line bill_line_expense_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_line
    ADD CONSTRAINT bill_line_expense_account_id_fkey FOREIGN KEY (expense_account_id) REFERENCES hms.account(account_id);


--
-- Name: bill_payment bill_payment_bill_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_payment
    ADD CONSTRAINT bill_payment_bill_id_fkey FOREIGN KEY (bill_id) REFERENCES hms.bill(bill_id);


--
-- Name: bill_payment bill_payment_paid_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill_payment
    ADD CONSTRAINT bill_payment_paid_by_fkey FOREIGN KEY (paid_by) REFERENCES hms.users(user_id);


--
-- Name: bill bill_vendor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.bill
    ADD CONSTRAINT bill_vendor_id_fkey FOREIGN KEY (vendor_id) REFERENCES hms.vendor(vendor_id);


--
-- Name: blocked_slots blocked_slots_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.blocked_slots
    ADD CONSTRAINT blocked_slots_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: blocked_slots blocked_slots_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.blocked_slots
    ADD CONSTRAINT blocked_slots_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: budget budget_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget
    ADD CONSTRAINT budget_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: budget budget_department_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget
    ADD CONSTRAINT budget_department_id_fkey FOREIGN KEY (department_id) REFERENCES hms.department(department_id);


--
-- Name: budget_line budget_line_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget_line
    ADD CONSTRAINT budget_line_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: budget_line budget_line_budget_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.budget_line
    ADD CONSTRAINT budget_line_budget_id_fkey FOREIGN KEY (budget_id) REFERENCES hms.budget(budget_id);


--
-- Name: depreciation depreciation_asset_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.depreciation
    ADD CONSTRAINT depreciation_asset_id_fkey FOREIGN KEY (asset_id) REFERENCES hms.asset(asset_id);


--
-- Name: depreciation depreciation_journal_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.depreciation
    ADD CONSTRAINT depreciation_journal_id_fkey FOREIGN KEY (journal_id) REFERENCES hms.journal_entry(journal_id);


--
-- Name: dispense dispense_invoice_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense
    ADD CONSTRAINT dispense_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES hms.invoice(invoice_id);


--
-- Name: dispense_item dispense_item_batch_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense_item
    ADD CONSTRAINT dispense_item_batch_id_fkey FOREIGN KEY (batch_id) REFERENCES hms.medicine_batch(batch_id);


--
-- Name: dispense_item dispense_item_dispense_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense_item
    ADD CONSTRAINT dispense_item_dispense_id_fkey FOREIGN KEY (dispense_id) REFERENCES hms.dispense(dispense_id);


--
-- Name: dispense_item dispense_item_prescription_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense_item
    ADD CONSTRAINT dispense_item_prescription_item_id_fkey FOREIGN KEY (prescription_item_id) REFERENCES hms.prescription_item(prescription_item_id);


--
-- Name: dispense dispense_pharmacist_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense
    ADD CONSTRAINT dispense_pharmacist_id_fkey FOREIGN KEY (pharmacist_id) REFERENCES hms.pharmacist(pharmacist_id);


--
-- Name: dispense dispense_prescription_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.dispense
    ADD CONSTRAINT dispense_prescription_id_fkey FOREIGN KEY (prescription_id) REFERENCES hms.prescription(prescription_id);


--
-- Name: doctor_schedule doctor_schedule_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor_schedule
    ADD CONSTRAINT doctor_schedule_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: doctor doctor_specialization_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor
    ADD CONSTRAINT doctor_specialization_id_fkey FOREIGN KEY (specialization_id) REFERENCES hms.specialization(specialization_id);


--
-- Name: doctor doctor_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.doctor
    ADD CONSTRAINT doctor_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: expense expense_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense
    ADD CONSTRAINT expense_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: expense expense_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense
    ADD CONSTRAINT expense_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: expense expense_department_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.expense
    ADD CONSTRAINT expense_department_id_fkey FOREIGN KEY (department_id) REFERENCES hms.department(department_id);


--
-- Name: goods_receipt goods_receipt_purchase_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.goods_receipt
    ADD CONSTRAINT goods_receipt_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES hms.purchase_order(purchase_id);


--
-- Name: goods_receipt goods_receipt_received_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.goods_receipt
    ADD CONSTRAINT goods_receipt_received_by_fkey FOREIGN KEY (received_by) REFERENCES hms.users(user_id);


--
-- Name: insurance insurance_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance
    ADD CONSTRAINT insurance_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: insurance insurance_provider_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.insurance
    ADD CONSTRAINT insurance_provider_id_fkey FOREIGN KEY (provider_id) REFERENCES hms.insurance_provider(provider_id);


--
-- Name: invoice invoice_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice
    ADD CONSTRAINT invoice_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: invoice_line_item invoice_line_item_invoice_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice_line_item
    ADD CONSTRAINT invoice_line_item_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES hms.invoice(invoice_id);


--
-- Name: invoice_line_item invoice_line_item_service_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice_line_item
    ADD CONSTRAINT invoice_line_item_service_id_fkey FOREIGN KEY (service_id) REFERENCES hms.service_master(service_id);


--
-- Name: invoice invoice_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.invoice
    ADD CONSTRAINT invoice_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: issue_details issue_details_issued_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_details
    ADD CONSTRAINT issue_details_issued_by_fkey FOREIGN KEY (issued_by) REFERENCES hms.users(user_id);


--
-- Name: issue_details issue_details_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_details
    ADD CONSTRAINT issue_details_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: issue_details issue_details_request_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_details
    ADD CONSTRAINT issue_details_request_id_fkey FOREIGN KEY (request_id) REFERENCES hms.issue_request(request_id);


--
-- Name: issue_request issue_request_approved_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request
    ADD CONSTRAINT issue_request_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES hms.users(user_id);


--
-- Name: issue_request issue_request_department_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request
    ADD CONSTRAINT issue_request_department_id_fkey FOREIGN KEY (department_id) REFERENCES hms.department(department_id);


--
-- Name: issue_request issue_request_requested_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.issue_request
    ADD CONSTRAINT issue_request_requested_by_fkey FOREIGN KEY (requested_by) REFERENCES hms.users(user_id);


--
-- Name: item item_category_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.item
    ADD CONSTRAINT item_category_id_fkey FOREIGN KEY (category_id) REFERENCES hms.category(category_id);


--
-- Name: journal_entry journal_entry_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_entry
    ADD CONSTRAINT journal_entry_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: journal_line journal_line_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_line
    ADD CONSTRAINT journal_line_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: journal_line journal_line_journal_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.journal_line
    ADD CONSTRAINT journal_line_journal_id_fkey FOREIGN KEY (journal_id) REFERENCES hms.journal_entry(journal_id);


--
-- Name: lab_order lab_order_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order
    ADD CONSTRAINT lab_order_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: lab_order lab_order_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order
    ADD CONSTRAINT lab_order_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: lab_order lab_order_record_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order
    ADD CONSTRAINT lab_order_record_id_fkey FOREIGN KEY (record_id) REFERENCES hms.medical_record(record_id);


--
-- Name: lab_order_test lab_order_test_lab_order_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order_test
    ADD CONSTRAINT lab_order_test_lab_order_id_fkey FOREIGN KEY (lab_order_id) REFERENCES hms.lab_order(lab_order_id);


--
-- Name: lab_order_test lab_order_test_test_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_order_test
    ADD CONSTRAINT lab_order_test_test_id_fkey FOREIGN KEY (test_id) REFERENCES hms.lab_test(test_id);


--
-- Name: lab_report lab_report_lab_order_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_report
    ADD CONSTRAINT lab_report_lab_order_id_fkey FOREIGN KEY (lab_order_id) REFERENCES hms.lab_order(lab_order_id);


--
-- Name: lab_report lab_report_prepared_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_report
    ADD CONSTRAINT lab_report_prepared_by_fkey FOREIGN KEY (prepared_by) REFERENCES hms.users(user_id);


--
-- Name: lab_result lab_result_lab_order_test_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_result
    ADD CONSTRAINT lab_result_lab_order_test_id_fkey FOREIGN KEY (lab_order_test_id) REFERENCES hms.lab_order_test(lab_order_test_id);


--
-- Name: lab_result lab_result_verified_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_result
    ADD CONSTRAINT lab_result_verified_by_fkey FOREIGN KEY (verified_by) REFERENCES hms.users(user_id);


--
-- Name: lab_schedule lab_schedule_lab_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_schedule
    ADD CONSTRAINT lab_schedule_lab_id_fkey FOREIGN KEY (lab_id) REFERENCES hms.lab(lab_id);


--
-- Name: lab_schedule lab_schedule_lab_order_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_schedule
    ADD CONSTRAINT lab_schedule_lab_order_id_fkey FOREIGN KEY (lab_order_id) REFERENCES hms.lab_order(lab_order_id);


--
-- Name: lab_schedule lab_schedule_technician_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_schedule
    ADD CONSTRAINT lab_schedule_technician_id_fkey FOREIGN KEY (technician_id) REFERENCES hms.lab_technician(technician_id);


--
-- Name: lab_technician lab_technician_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.lab_technician
    ADD CONSTRAINT lab_technician_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: medical_record medical_record_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medical_record
    ADD CONSTRAINT medical_record_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: medical_record medical_record_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medical_record
    ADD CONSTRAINT medical_record_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: medical_record medical_record_visit_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medical_record
    ADD CONSTRAINT medical_record_visit_id_fkey FOREIGN KEY (visit_id) REFERENCES hms.visit(visit_id);


--
-- Name: medicine_batch medicine_batch_medicine_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.medicine_batch
    ADD CONSTRAINT medicine_batch_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES hms.medicine(medicine_id);


--
-- Name: patient patient_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.patient
    ADD CONSTRAINT patient_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: payment payment_invoice_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.payment
    ADD CONSTRAINT payment_invoice_id_fkey FOREIGN KEY (invoice_id) REFERENCES hms.invoice(invoice_id);


--
-- Name: pharmacist pharmacist_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.pharmacist
    ADD CONSTRAINT pharmacist_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: prescription prescription_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription
    ADD CONSTRAINT prescription_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: prescription_item prescription_item_medicine_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription_item
    ADD CONSTRAINT prescription_item_medicine_id_fkey FOREIGN KEY (medicine_id) REFERENCES hms.medicine(medicine_id);


--
-- Name: prescription_item prescription_item_prescription_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription_item
    ADD CONSTRAINT prescription_item_prescription_id_fkey FOREIGN KEY (prescription_id) REFERENCES hms.prescription(prescription_id);


--
-- Name: prescription prescription_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription
    ADD CONSTRAINT prescription_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: prescription prescription_record_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.prescription
    ADD CONSTRAINT prescription_record_id_fkey FOREIGN KEY (record_id) REFERENCES hms.medical_record(record_id);


--
-- Name: purchase_order purchase_order_created_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order
    ADD CONSTRAINT purchase_order_created_by_fkey FOREIGN KEY (created_by) REFERENCES hms.users(user_id);


--
-- Name: purchase_order_item purchase_order_item_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order_item
    ADD CONSTRAINT purchase_order_item_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: purchase_order_item purchase_order_item_purchase_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order_item
    ADD CONSTRAINT purchase_order_item_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES hms.purchase_order(purchase_id);


--
-- Name: purchase_order purchase_order_supplier_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.purchase_order
    ADD CONSTRAINT purchase_order_supplier_id_fkey FOREIGN KEY (supplier_id) REFERENCES hms.supplier(supplier_id);


--
-- Name: report report_record_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.report
    ADD CONSTRAINT report_record_id_fkey FOREIGN KEY (record_id) REFERENCES hms.medical_record(record_id);


--
-- Name: stock_adjustment stock_adjustment_adjusted_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment
    ADD CONSTRAINT stock_adjustment_adjusted_by_fkey FOREIGN KEY (adjusted_by) REFERENCES hms.users(user_id);


--
-- Name: stock_adjustment stock_adjustment_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment
    ADD CONSTRAINT stock_adjustment_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: stock_adjustment stock_adjustment_location_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_adjustment
    ADD CONSTRAINT stock_adjustment_location_id_fkey FOREIGN KEY (location_id) REFERENCES hms.store_location(location_id);


--
-- Name: stock_audit stock_audit_conducted_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit
    ADD CONSTRAINT stock_audit_conducted_by_fkey FOREIGN KEY (conducted_by) REFERENCES hms.users(user_id);


--
-- Name: stock_audit_details stock_audit_details_audit_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit_details
    ADD CONSTRAINT stock_audit_details_audit_id_fkey FOREIGN KEY (audit_id) REFERENCES hms.stock_audit(audit_id);


--
-- Name: stock_audit_details stock_audit_details_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit_details
    ADD CONSTRAINT stock_audit_details_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: stock_audit stock_audit_location_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_audit
    ADD CONSTRAINT stock_audit_location_id_fkey FOREIGN KEY (location_id) REFERENCES hms.store_location(location_id);


--
-- Name: stock stock_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock
    ADD CONSTRAINT stock_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: stock stock_location_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock
    ADD CONSTRAINT stock_location_id_fkey FOREIGN KEY (location_id) REFERENCES hms.store_location(location_id);


--
-- Name: stock_transfer stock_transfer_approved_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_approved_by_fkey FOREIGN KEY (approved_by) REFERENCES hms.users(user_id);


--
-- Name: stock_transfer stock_transfer_from_location_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_from_location_id_fkey FOREIGN KEY (from_location_id) REFERENCES hms.store_location(location_id);


--
-- Name: stock_transfer stock_transfer_initiated_by_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_initiated_by_fkey FOREIGN KEY (initiated_by) REFERENCES hms.users(user_id);


--
-- Name: stock_transfer stock_transfer_item_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_item_id_fkey FOREIGN KEY (item_id) REFERENCES hms.item(item_id);


--
-- Name: stock_transfer stock_transfer_to_location_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.stock_transfer
    ADD CONSTRAINT stock_transfer_to_location_id_fkey FOREIGN KEY (to_location_id) REFERENCES hms.store_location(location_id);


--
-- Name: tax tax_account_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.tax
    ADD CONSTRAINT tax_account_id_fkey FOREIGN KEY (account_id) REFERENCES hms.account(account_id);


--
-- Name: user_role user_role_role_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.user_role
    ADD CONSTRAINT user_role_role_id_fkey FOREIGN KEY (role_id) REFERENCES hms.role(role_id);


--
-- Name: user_role user_role_user_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.user_role
    ADD CONSTRAINT user_role_user_id_fkey FOREIGN KEY (user_id) REFERENCES hms.users(user_id);


--
-- Name: users users_department_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.users
    ADD CONSTRAINT users_department_id_fkey FOREIGN KEY (department_id) REFERENCES hms.department(department_id);


--
-- Name: visit visit_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.visit
    ADD CONSTRAINT visit_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: visit visit_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.visit
    ADD CONSTRAINT visit_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- Name: waiting_list waiting_list_doctor_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.waiting_list
    ADD CONSTRAINT waiting_list_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES hms.doctor(doctor_id);


--
-- Name: waiting_list waiting_list_patient_id_fkey; Type: FK CONSTRAINT; Schema: hms; Owner: postgres
--

ALTER TABLE ONLY hms.waiting_list
    ADD CONSTRAINT waiting_list_patient_id_fkey FOREIGN KEY (patient_id) REFERENCES hms.patient(patient_id);


--
-- PostgreSQL database dump complete
--

\unrestrict 9UTpp3XxQ7mrpDbZjOdjnfflvP0WHalJfkNs4Us6FvbrmZyVt1Rj06h7dMsYQvI

