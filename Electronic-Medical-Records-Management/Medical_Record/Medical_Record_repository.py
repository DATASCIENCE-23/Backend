from sqlalchemy.orm import Session
from .Medical_Record_model import MedicalRecord

class MedicalRecordRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, record: MedicalRecord):
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_by_id(self, record_id: int):
        return self.db.query(MedicalRecord).filter(
            MedicalRecord.record_id == record_id
        ).first()

    def get_by_patient(self, patient_id: int):
        return (
            self.db.query(MedicalRecord)
            .filter(MedicalRecord.patient_id == patient_id)
            .order_by(MedicalRecord.record_date.desc())
            .all()
        )

    def update_record(self, record_id: int, data: dict):
        record = self.get_by_id(record_id)
        if not record:
            return None

        for key, value in data.items():
            setattr(record, key, value)

        self.db.commit()
        self.db.refresh(record)
        return record

    def delete_record(self, record_id: int):
        record = self.get_by_id(record_id)
        if record:
            self.db.delete(record)
            self.db.commit()
        return record
    def get_all_records(self):
        return (
            self.db.query(MedicalRecord)
            .order_by(MedicalRecord.record_date.desc())
            .all()
        )
