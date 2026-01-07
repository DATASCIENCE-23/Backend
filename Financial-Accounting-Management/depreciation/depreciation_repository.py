from sqlalchemy.orm import Session
from depreciation.depreciation_models import Depreciation

class DepreciationRepository:

    @staticmethod
    def create(db: Session, depreciation: Depreciation):
        db.add(depreciation)
        db.commit()
        db.refresh(depreciation)
        return depreciation

    @staticmethod
    def get_by_id(db: Session, depreciation_id: int):
        return db.query(Depreciation).filter(
            Depreciation.depreciation_id == depreciation_id
        ).first()

    @staticmethod
    def get_by_asset(db: Session, asset_id: int):
        return db.query(Depreciation).filter(
            Depreciation.asset_id == asset_id
        ).all()

    @staticmethod
    def get_all(db: Session):
        return db.query(Depreciation).all()

    @staticmethod
    def update(db: Session, depreciation: Depreciation, data: dict):
        for key, value in data.items():
            setattr(depreciation, key, value)
        db.commit()
        db.refresh(depreciation)
        return depreciation

    @staticmethod
    def delete(db: Session, depreciation: Depreciation):
        db.delete(depreciation)
        db.commit()
