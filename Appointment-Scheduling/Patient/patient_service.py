from patient_repository import PatientRepository
from patient_model import Patient


class PatientService:

    def __init__(self, repository: PatientRepository):
        self.repository = repository

    def create_patient(self, data: dict):
        patient = Patient(**data)
        return self.repository.create_patient(patient)

    def get_patient(self, patient_id: int):
        return self.repository.get_patient_by_id(patient_id)

    def get_all_patients(self):
        return self.repository.get_all_patients()

    def update_patient(self, patient_id: int, data: dict):
        return self.repository.update_patient(patient_id, data)

    def delete_patient(self, patient_id: int):
        return self.repository.delete_patient(patient_id)
