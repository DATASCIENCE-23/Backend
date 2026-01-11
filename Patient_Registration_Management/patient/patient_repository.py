from sqlalchemy.orm import Session
from Patient_Registration_Management.patient.patient_model import Patient


class PatientRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_patient(self, patient: Patient):
        self.db.add(patient)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def get_patient_by_id(self, patient_id: int):
        return self.db.query(Patient).filter(Patient.patient_id == patient_id).first()

    def get_all_patients(self):
        return self.db.query(Patient).all()

    def update_patient(self, patient_id: int, data: dict):
        patient = self.get_patient_by_id(patient_id)
        if not patient:
            return None
        for key, value in data.items():
            setattr(patient, key, value)
        self.db.commit()
        self.db.refresh(patient)
        return patient

    def delete_patient(self, patient_id: int):
        patient = self.get_patient_by_id(patient_id)
        if patient:
            self.db.delete(patient)
            self.db.commit()
        return patient
