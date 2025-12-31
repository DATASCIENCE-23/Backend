from sqlalchemy.orm import Session
from Depreciation.Depreciation_model import Depreciation

class DepreciationRepository:

    @staticmethod
    def get_by_id(db: Session, depreciation_id: int):
        return db.query(Depreciation).filter(Depreciation.id == depreciation_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Depreciation).all()

    @staticmethod
    def create(db: Session, depreciation: Depreciation):
        db.add(depreciation)
        db.commit()
        db.refresh(depreciation)
        return depreciation
