from sqlalchemy.orm import Session
from .MedicalRecord_model import MedicalRecord

class MedicalRecordRepository:
    @staticmethod
    def create_record(db: Session, patient_id: int, doctor_id: int, data: dict):
        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=doctor_id,
            visit_id=data.get("visit_id"),
            chief_complaint=data.get("chief_complaint"),
            history_of_present_illness=data.get("history_of_present_illness"),
            past_medical_history=data.get("past_medical_history"),
            physical_examination=data.get("physical_examination"),
            diagnosis=data.get("diagnosis"),
            treatment_plan=data.get("treatment_plan"),
            clinical_notes=data.get("clinical_notes"),
            vital_signs=data.get("vital_signs"),
            medication_orders=data.get("medication_orders"),
            allergies_notified=data.get("allergies_notified"),
            notes=data.get("notes"),
        )
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_record_by_id(db: Session, record_id: int):
        return db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()

    @staticmethod
    def get_records_by_patient(db: Session, patient_id: int, limit: int = 50):
        return (
            db.query(MedicalRecord)
            .filter(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.record_date.desc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def get_all_records(db: Session):
        return db.query(MedicalRecord).order_by(MedicalRecord.record_date.desc()).all()

    @staticmethod
    def update_record(db: Session, record_id: int, updates: dict):
        record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
        if not record:
            raise ValueError("Medical record not found")
        for key, value in updates.items():
            if hasattr(record, key):
                setattr(record, key, value)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def delete_record(db: Session, record_id: int):
        record = db.query(MedicalRecord).filter(MedicalRecord.record_id == record_id).first()
        if not record:
            raise ValueError("Medical record not found")
        db.delete(record)
        db.commit()