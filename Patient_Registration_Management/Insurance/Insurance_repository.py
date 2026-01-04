from sqlalchemy.orm import Session
from Insurance_model import Insurance


class InsuranceRepository:

    @staticmethod
    def get_by_id(db: Session, insurance_id: int):
        return db.query(Insurance).filter(Insurance.insurance_id == insurance_id).first()


    @staticmethod
    def get_by_policy_number(db: Session, policy_number: str):
        return db.query(Insurance).filter(
            Insurance.policy_number == policy_number
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Insurance).all()

    @staticmethod
    def get_by_patient_id(db: Session, patient_id: int):
        return db.query(Insurance).filter(
            Insurance.patient_id == patient_id
        ).all()

    @staticmethod
    def create(db: Session, insurance: Insurance):
        db.add(insurance)
        db.commit()
        db.refresh(insurance)
        return insurance

    @staticmethod
    def update(db: Session, insurance: Insurance):
        db.commit()
        db.refresh(insurance)
        return insurance

    @staticmethod
    def delete(db: Session, insurance: Insurance):
        db.delete(insurance)
        db.commit()
