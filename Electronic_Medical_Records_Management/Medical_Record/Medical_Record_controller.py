from .Medical_Record_service import MedicalRecordService

class MedicalRecordController:
    def __init__(self, service: MedicalRecordService):
        self.service = service

    def create_medical_record(self, doctor_id: int, payload: dict):
        return self.service.create_record(
            doctor_id=doctor_id,
            data=payload
        )

    def get_medical_record(self, record_id: int):
        return self.service.get_record(record_id)

    def get_patient_medical_history(self, patient_id: int):
        return self.service.get_patient_history(patient_id)

    def update_medical_record(self, record_id: int, payload: dict):
        return self.service.update_record(record_id, payload)

    def delete_medical_record(self, record_id: int):
        return self.service.delete_record(record_id)
