from sqlalchemy.orm import Session
from Asset.Asset_model import Asset
from Asset.Asset_repository import AssetRepository

class AssetService:

    @staticmethod
    def create_asset(db: Session, data: dict):
        asset = Asset(**data)
        return AssetRepository.create(db, asset)

    @staticmethod
    def get_asset(db: Session, asset_id: int):
        asset = AssetRepository.get_by_id(db, asset_id)
        if not asset:
            raise ValueError("Asset not found")
        return asset

    @staticmethod
    def list_assets(db: Session):
        return AssetRepository.get_all(db)

    @staticmethod
    def update_asset(db: Session, asset_id: int, data: dict):
        asset = AssetRepository.get_by_id(db, asset_id)
        if not asset:
            raise ValueError("Asset not found")

        for key, value in data.items():
            setattr(asset, key, value)

        return AssetRepository.update(db, asset)

    @staticmethod
    def delete_asset(db: Session, asset_id: int):
        asset = AssetRepository.get_by_id(db, asset_id)
        if not asset:
            raise ValueError("Asset not found")

        AssetRepository.delete(db, asset)
