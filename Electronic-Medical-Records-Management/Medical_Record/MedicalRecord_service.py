from sqlalchemy.orm import Session
from .MedicalRecord_repository import MedicalRecordRepository
from ..User.User_service import UserService  # To check roles if needed later

class MedicalRecordService:
    def __init__(self, db: Session):
        self.db = db

    def create_record(self, current_user_id: int, patient_id: int, payload: dict):
        # Basic validation
        if not patient_id:
            raise ValueError("patient_id is required")
        payload["patient_id"] = patient_id
        payload["doctor_id"] = current_user_id  # Assume creator is the doctor
        return MedicalRecordRepository.create_record(self.db, patient_id, current_user_id, payload)

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