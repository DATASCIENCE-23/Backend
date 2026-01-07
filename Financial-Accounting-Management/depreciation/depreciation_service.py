from sqlalchemy.orm import Session
from depreciation.depreciation_models import Depreciation
from depreciation.depreciation_repository import DepreciationRepository
from depreciation.depreciation_schema import DepreciationCreate

class DepreciationService:

    @staticmethod
    def create_depreciation(db: Session, data: DepreciationCreate):
        if data.amount <= 0:
            raise ValueError("Depreciation amount must be positive")

        depreciation = Depreciation(**data.dict())
        return DepreciationRepository.create(db, depreciation)

    @staticmethod
    def get_depreciation(db: Session, depreciation_id: int):
        return DepreciationRepository.get_by_id(db, depreciation_id)

    @staticmethod
    def get_depreciation_by_asset(db: Session, asset_id: int):
        return DepreciationRepository.get_by_asset(db, asset_id)

    @staticmethod
    def get_all_depreciations(db: Session):
        return DepreciationRepository.get_all(db)

    @staticmethod
    def update_depreciation(db: Session, depreciation_id: int, data: dict):
        depreciation = DepreciationRepository.get_by_id(db, depreciation_id)
        if not depreciation:
            raise ValueError("Depreciation record not found")

        return DepreciationRepository.update(db, depreciation, data)

    @staticmethod
    def delete_depreciation(db: Session, depreciation_id: int):
        depreciation = DepreciationRepository.get_by_id(db, depreciation_id)
        if not depreciation:
            raise ValueError("Depreciation record not found")

        return DepreciationRepository.delete(db, depreciation)
