from sqlalchemy.orm import Session
from Patient.Patient_model import Patient

class PatientRepository:

    @staticmethod
    def get_by_id(db: Session, patient_id: int):
        return db.query(Patient).filter(Patient.id == patient_id).first()

    @staticmethod
    def get_by_phone(db: Session, phone: str):
        return db.query(Patient).filter(Patient.phone == phone).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Patient).all()

    @staticmethod
    def create(db: Session, patient: Patient):
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def update(db: Session, patient: Patient):
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def delete(db: Session, patient: Patient):
        db.delete(patient)
        db.commit()
