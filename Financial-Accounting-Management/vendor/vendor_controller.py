from sqlalchemy.orm import Session
from vendor.vendor_service import VendorService
from vendor.vendor_schema import VendorCreate

class VendorController:

    @staticmethod
    def create(db: Session, data: VendorCreate):
        return VendorService.create_vendor(db, data)

    @staticmethod
    def get(db: Session, vendor_id: int):
        return VendorService.get_vendor(db, vendor_id)

    @staticmethod
    def get_all(db: Session):
        return VendorService.get_all_vendors(db)

    @staticmethod
    def update(db: Session, vendor_id: int, data: dict):
        return VendorService.update_vendor(db, vendor_id, data)

    @staticmethod
    def delete(db: Session, vendor_id: int):
        return VendorService.delete_vendor(db, vendor_id)
