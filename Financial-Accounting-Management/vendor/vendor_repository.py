from sqlalchemy.orm import Session
from vendor.vendor_models import Vendor

class VendorRepository:

    @staticmethod
    def create(db: Session, vendor: Vendor):
        db.add(vendor)
        db.commit()
        db.refresh(vendor)
        return vendor

    @staticmethod
    def get_by_id(db: Session, vendor_id: int):
        return db.query(Vendor).filter(
            Vendor.vendor_id == vendor_id
        ).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Vendor).all()

    @staticmethod
    def update(db: Session, vendor: Vendor, data: dict):
        for key, value in data.items():
            setattr(vendor, key, value)
        db.commit()
        db.refresh(vendor)
        return vendor

    @staticmethod
    def delete(db: Session, vendor: Vendor):
        db.delete(vendor)
        db.commit()
