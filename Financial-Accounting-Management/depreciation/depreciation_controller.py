from sqlalchemy.orm import Session
from depreciation.depreciation_service import DepreciationService
from depreciation.depreciation_schema import DepreciationCreate

class DepreciationController:

    @staticmethod
    def create(db: Session, data: DepreciationCreate):
        return DepreciationService.create_depreciation(db, data)

    @staticmethod
    def get(db: Session, depreciation_id: int):
        return DepreciationService.get_depreciation(db, depreciation_id)

    @staticmethod
    def get_all(db: Session):
        return DepreciationService.get_all_depreciations(db)

    @staticmethod
    def get_by_asset(db: Session, asset_id: int):
        return DepreciationService.get_depreciation_by_asset(db, asset_id)

    @staticmethod
    def update(db: Session, depreciation_id: int, data: dict):
        return DepreciationService.update_depreciation(db, depreciation_id, data)

    @staticmethod
    def delete(db: Session, depreciation_id: int):
        return DepreciationService.delete_depreciation(db, depreciation_id)
