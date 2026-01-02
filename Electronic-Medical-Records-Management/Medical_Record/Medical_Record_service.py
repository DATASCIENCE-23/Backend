from sqlalchemy.orm import Session
from .Medical_Record_repository import MedicalRecordRepository
from User.User_model import User   # ✅ Use USERS instead


class MedicalRecordService:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, user_id: int, patient_id: int, payload: dict):
        """
        Create medical record.
        Assumes doctor_id refers to users.user_id (no Doctor module yet)
        """

        # ✅ Validate user exists
        user = self.db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise ValueError("Invalid user")

        return MedicalRecordRepository.create_record(
            self.db,
            patient_id=patient_id,
            doctor_id=user.user_id,   # ✅ doctor_id = user_id
            data=payload
        )

    def get_record(self, record_id: int):
        record = MedicalRecordRepository.get_record_by_id(self.db, record_id)
        if not record:
            raise ValueError("Medical record not found")
        return record

    def get_patient_history(self, patient_id: int):
        return MedicalRecordRepository.get_records_by_patient(self.db, patient_id)

    def list_all_records(self):
        return MedicalRecordRepository.get_all_records(self.db)

    def update_record(self, record_id: int, payload: dict):
        return MedicalRecordRepository.update_record(self.db, record_id, payload)

    def delete_record(self, record_id: int):
        MedicalRecordRepository.delete_record(self.db, record_id)
