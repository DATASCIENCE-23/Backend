from sqlalchemy.orm import Session
from asset.asset_models import Asset

class AssetRepository:

    @staticmethod
    def create(db: Session, asset: Asset):
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def get_by_id(db: Session, asset_id: int):
        return db.query(Asset).filter(Asset.asset_id == asset_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Asset).all()

    @staticmethod
    def update(db: Session, asset: Asset, data: dict):
        for key, value in data.items():
            setattr(asset, key, value)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete(db: Session, asset: Asset):
        db.delete(asset)
        db.commit()
