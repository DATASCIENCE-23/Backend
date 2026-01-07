from sqlalchemy.orm import Session
from Asset.Asset_model import Asset

class AssetRepository:

    @staticmethod
    def get_by_id(db: Session, asset_id: int):
        return db.query(Asset).filter(Asset.id == asset_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Asset).all()

    @staticmethod
    def create(db: Session, asset: Asset):
        db.add(asset)
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def update(db: Session, asset: Asset):
        db.commit()
        db.refresh(asset)
        return asset

    @staticmethod
    def delete(db: Session, asset: Asset):
        db.delete(asset)
        db.commit()
