from sqlalchemy.orm import Session
from .Medical_Record_model import MedicalRecord

class MedicalRecordRepository:

    @staticmethod
    def create_record(db: Session, patient_id: int, doctor_id: int, data: dict):

        allowed_fields = {
            "visit_id",
            "chief_complaint",
            "history_of_present_illness",
            "past_medical_history",
            "physical_examination",
            "diagnosis",          # ✅ CORRECT
            "treatment_plan",
            "notes",
        }

        filtered_data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        record = MedicalRecord(
            patient_id=patient_id,
            doctor_id=doctor_id,
            **filtered_data
        )

        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    @staticmethod
    def get_record_by_id(db: Session, record_id: int):
        return db.query(MedicalRecord).filter(
            MedicalRecord.record_id == record_id
        ).first()

    @staticmethod
    def get_records_by_patient(db: Session, patient_id: int):
        return (
            db.query(MedicalRecord)
            .filter(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.record_date.desc())
            .all()
        )

    @staticmethod
    def get_all_records(db: Session):
        return (
            db.query(MedicalRecord)
            .order_by(MedicalRecord.record_date.desc())
            .all()
        )

    @staticmethod
    def update_record(db: Session, record_id: int, updates: dict):
        record = db.query(MedicalRecord).filter(
            MedicalRecord.record_id == record_id
        ).first()

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
        record = db.query(MedicalRecord).filter(
            MedicalRecord.record_id == record_id
        ).first()

        if not record:
            raise ValueError("Medical record not found")

        db.delete(record)
        db.commit()
