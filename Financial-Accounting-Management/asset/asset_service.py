from sqlalchemy.orm import Session
from asset.asset_models import Asset
from asset.asset_repository import AssetRepository
from asset.asset_schema import AssetCreate

class AssetService:

    @staticmethod
    def create_asset(db: Session, data: AssetCreate):
        if data.useful_life_years <= 0:
            raise ValueError("Useful life must be greater than zero")

        asset = Asset(**data.dict())
        return AssetRepository.create(db, asset)

    @staticmethod
    def get_asset(db: Session, asset_id: int):
        return AssetRepository.get_by_id(db, asset_id)

    @staticmethod
    def get_all_assets(db: Session):
        return AssetRepository.get_all(db)

    @staticmethod
    def update_asset(db: Session, asset_id: int, data: dict):
        asset = AssetRepository.get_by_id(db, asset_id)
        if not asset:
            raise ValueError("Asset not found")

        return AssetRepository.update(db, asset, data)

    @staticmethod
    def delete_asset(db: Session, asset_id: int):
        asset = AssetRepository.get_by_id(db, asset_id)
        if not asset:
            raise ValueError("Asset not found")

        return AssetRepository.delete(db, asset)
