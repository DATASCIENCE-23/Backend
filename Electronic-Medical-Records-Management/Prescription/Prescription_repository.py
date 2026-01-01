from sqlalchemy.orm import Session
from .Prescription_model import Prescription, PrescriptionStatus

class PrescriptionRepository:
    @staticmethod
    def create_prescription(db: Session, record_id: int, patient_id: int, doctor_id: int, notes: str = None, status: str = "Active"):
        prescription = Prescription(
            record_id=record_id,
            patient_id=patient_id,
            doctor_id=doctor_id,
            notes=notes,
            status=PrescriptionStatus(status)
        )
        db.add(prescription)
        db.commit()
        db.refresh(prescription)
        return prescription

    @staticmethod
    def get_prescription_by_id(db: Session, prescription_id: int):
        return db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()

    @staticmethod
    def get_prescriptions_by_patient(db: Session, patient_id: int):
        return (
            db.query(Prescription)
            .filter(Prescription.patient_id == patient_id)
            .order_by(Prescription.created_at.desc())
            .all()
        )

    @staticmethod
    def get_prescriptions_by_record(db: Session, record_id: int):
        return db.query(Prescription).filter(Prescription.record_id == record_id).all()

    @staticmethod
    def update_prescription(db: Session, prescription_id: int, updates: dict):
        prescription = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
        if not prescription:
            raise ValueError("Prescription not found")
        for key, value in updates.items():
            if key == "status" and value:
                setattr(prescription, key, PrescriptionStatus(value))
            elif hasattr(prescription, key):
                setattr(prescription, key, value)
        db.commit()
        db.refresh(prescription)
        return prescription

    @staticmethod
    def delete_prescription(db: Session, prescription_id: int):
        prescription = db.query(Prescription).filter(Prescription.prescription_id == prescription_id).first()
        if not prescription:
            raise ValueError("Prescription not found")
        db.delete(prescription)
        db.commit()