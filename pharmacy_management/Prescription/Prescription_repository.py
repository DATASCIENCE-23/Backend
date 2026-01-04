# Prescription/Prescription_repository.py
from sqlalchemy.orm import Session
from .Prescription_model import Prescription

class PrescriptionRepository:

    @staticmethod
    def create(db: Session, record_id: int, patient_id: int, doctor_id: int, notes=None):
        prescription = Prescription(
            record_id=record_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=notes
        )
        db.add(prescription)
        db.commit()
        db.refresh(prescription)
        return prescription

    @staticmethod
    def get_by_id(db: Session, prescription_id: int):
        return db.query(Prescription).filter_by(
            prescription_id=prescription_id
        ).first()

    @staticmethod
    def get_by_patient(db: Session, patient_id: int):
        return db.query(Prescription).filter_by(
            patient_id=patient_id
        ).order_by(Prescription.created_at.desc()).all()

    @staticmethod
    def get_by_record(db: Session, record_id: int):
        return db.query(Prescription).filter_by(
            record_id=record_id
        ).all()

    @staticmethod
    def update(db: Session, prescription_id: int, updates: dict):
        prescription = db.query(Prescription).filter_by(
            prescription_id=prescription_id
        ).first()

        if not prescription:
            raise ValueError("Prescription not found")

        for key, value in updates.items():
            if hasattr(prescription, key):
                setattr(prescription, key, value)

        db.commit()
        db.refresh(prescription)
        return prescription
    @staticmethod
    def update_prescription(db: Session, prescription_id: int, payload: dict):
        prescription = db.query(Prescription).filter_by(
            prescription_id=prescription_id
        ).first()

        if not prescription:
            raise ValueError("Prescription not found")

        for key, value in payload.items():
            if hasattr(prescription, key):
                setattr(prescription, key, value)

        db.commit()
        db.refresh(prescription)
        return prescription
    def delete_prescription(db, prescription_id):
        prescription = db.query(Prescription).filter(
            Prescription.prescription_id == prescription_id
        ).first()

        if not prescription:
            raise ValueError("Prescription not found")

        db.delete(prescription)
        db.commit()
