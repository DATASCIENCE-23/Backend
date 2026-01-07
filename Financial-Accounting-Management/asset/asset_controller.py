from sqlalchemy.orm import Session
from asset.asset_service import AssetService
from asset.asset_schema import AssetCreate

class AssetController:

    @staticmethod
    def create(db: Session, data: AssetCreate):
        return AssetService.create_asset(db, data)

    @staticmethod
    def get(db: Session, asset_id: int):
        return AssetService.get_asset(db, asset_id)

    @staticmethod
    def get_all(db: Session):
        return AssetService.get_all_assets(db)

    @staticmethod
    def update(db: Session, asset_id: int, data: dict):
        return AssetService.update_asset(db, asset_id, data)

    @staticmethod
    def delete(db: Session, asset_id: int):
        return AssetService.delete_asset(db, asset_id)
