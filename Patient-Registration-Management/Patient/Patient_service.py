from sqlalchemy.orm import Session
from Model.Patient import Patient
from Repository.Patient_repository import PatientRepository

class PatientService:

    @staticmethod
    def create_patient(db: Session, data: dict):
        if PatientRepository.get_by_phone(db, data["phone"]):
            raise ValueError("Patient with this phone already exists")

        patient = Patient(**data)
        return PatientRepository.create(db, patient)

    @staticmethod
    def get_patient(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError("Patient not found")
        return patient

    @staticmethod
    def list_patients(db: Session):
        return PatientRepository.get_all(db)

    @staticmethod
    def update_patient(db: Session, patient_id: int, data: dict):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError("Patient not found")

        for key, value in data.items():
            setattr(patient, key, value)

        return PatientRepository.update(db, patient)

    @staticmethod
    def delete_patient(db: Session, patient_id: int):
        patient = PatientRepository.get_by_id(db, patient_id)
        if not patient:
            raise ValueError("Patient not found")

        PatientRepository.delete(db, patient)
