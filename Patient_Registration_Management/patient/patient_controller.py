from sqlalchemy.orm import Session
from Patient_Registration_Management.patient.patient_service import PatientService
from Patient_Registration_Management.patient.patient_repository import PatientRepository



class PatientController:

    def __init__(self, db: Session):
        self.service = PatientService(PatientRepository(db))

    def create_patient(self, data: dict):
        return self.service.create_patient(data)

    def get_patient(self, patient_id: int):
        return self.service.get_patient(patient_id)

    def get_all_patients(self):
        return self.service.get_all_patients()

    def update_patient(self, patient_id: int, data: dict):
        return self.service.update_patient(patient_id, data)

    def delete_patient(self, patient_id: int):
        return self.service.delete_patient(patient_id)
