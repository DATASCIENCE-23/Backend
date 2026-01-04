from .Medical_Record_repository import MedicalRecordRepository
from .Medical_Record_model import MedicalRecord

class MedicalRecordService:
    def __init__(self, repository: MedicalRecordRepository):
        self.repository = repository

    def create_record(self, doctor_id: int, data: dict):
        record = MedicalRecord(
            doctor_id=doctor_id,
            **data
        )
        return self.repository.create_record(record)

    def get_record(self, record_id: int):
        return self.repository.get_by_id(record_id)

    def get_patient_history(self, patient_id: int):
        return self.repository.get_by_patient(patient_id)

    def update_record(self, record_id: int, data: dict):
        return self.repository.update_record(record_id, data)

    def delete_record(self, record_id: int):
        return self.repository.delete_record(record_id)
    def get_all_records(self):
        return self.repository.get_all_records()
