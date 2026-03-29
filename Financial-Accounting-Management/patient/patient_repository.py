from sqlalchemy.orm import Session
from sqlalchemy import or_
from PATIENT.patient_model import Patient


class PatientRepository:

    @staticmethod
    def create(db: Session, patient: Patient) -> Patient:
        db.add(patient)
        db.commit()
        db.refresh(patient)
        return patient

    @staticmethod
    def get_by_id(db: Session, patient_id: int) -> Patient | None:
        return (
            db.query(Patient)
            .filter(Patient.patient_id == patient_id)
            .first()
        )

    @staticmethod
    def list_all(db: Session) -> list[Patient]:
        return db.query(Patient).all()

    @staticmethod
    def search(
        db: Session,
        name: str | None = None,
        contact: str | None = None
    ) -> list[Patient]:
        query = db.query(Patient)

        if name:
            query = query.filter(Patient.patient_name.ilike(f"%{name}%"))

        if contact:
            query = query.filter(Patient.contact_details.ilike(f"%{contact}%"))

        return query.all()

    @staticmethod
    def delete(db: Session, patient: Patient) -> None:
        db.delete(patient)
        db.commit()
