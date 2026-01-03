from sqlalchemy.orm import Session
from .admission_model import Admission

class AdmissionRepository:

    @staticmethod
    def get_by_id(db: Session, admission_id: int):
        return db.query(Admission).filter(
            Admission.admission_id == admission_id
        ).first()

    @staticmethod
    def get_by_appointment_id(db: Session, appointment_id: int):
        return db.query(Admission).filter(
            Admission.appointment_id == appointment_id
        ).first()

    @staticmethod
    def get_active_admissions(db: Session):
        return db.query(Admission).filter(
            Admission.status == "ADMITTED",
            Admission.discharge_datetime.is_(None)
        ).all()

    @staticmethod
    def create(db: Session, admission: Admission):
        db.add(admission)
        db.commit()
        db.refresh(admission)
        return admission

    @staticmethod
    def update(db: Session, admission: Admission):
        db.commit()
        db.refresh(admission)
        return admission

    @staticmethod
    def delete(db: Session, admission: Admission):
        db.delete(admission)
        db.commit()
