from sqlalchemy import Column, Integer, String, DateTime, Text, Numeric
from database import Base

class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    phone_number = Column(String)

class Visit(Base):
    __tablename__ = "visit"
    visit_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    visit_datetime = Column(DateTime)
    chief_complaint = Column(Text)

class Invoice(Base):
    __tablename__ = "invoice"
    invoice_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    grand_total = Column(Numeric)

class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer)
    amount_paid = Column(Numeric)

class LabTest(Base):
    __tablename__ = "lab_test"

    test_id = Column(Integer, primary_key=True)
    test_name = Column(String)
    test_code = Column(String)


class LabResult(Base):
    __tablename__ = "lab_result"

    result_id = Column(Integer, primary_key=True)
    lab_order_id = Column(Integer)
    test_id = Column(Integer)
    result_value = Column(Text)
    reference_range = Column(Text)
    abnormal_flag = Column(String)

class Medicine(Base):
    __tablename__ = "medicine"

    medicine_id = Column(Integer, primary_key=True)
    medicine_name = Column(String)
    form = Column(String)


class Prescription(Base):
    __tablename__ = "prescription"

    prescription_id = Column(Integer, primary_key=True)
    patient_id = Column(Integer)
    visit_id = Column(Integer)
    created_at = Column(DateTime)


class PrescriptionItem(Base):
    __tablename__ = "prescription_item"

    prescription_item_id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer)
    medicine_id = Column(Integer)
    dosage = Column(String)
    frequency = Column(String)
    duration_days = Column(Integer)


class Dispense(Base):
    __tablename__ = "dispense"

    dispense_id = Column(Integer, primary_key=True)
    prescription_id = Column(Integer)
    dispensed_at = Column(DateTime)
