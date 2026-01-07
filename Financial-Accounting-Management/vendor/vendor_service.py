from sqlalchemy.orm import Session
from vendor.vendor_models import Vendor
from vendor.vendor_repository import VendorRepository
from vendor.vendor_schema import VendorCreate

class VendorService:

    @staticmethod
    def create_vendor(db: Session, data: VendorCreate):
        vendor = Vendor(**data.dict())
        return VendorRepository.create(db, vendor)

    @staticmethod
    def get_vendor(db: Session, vendor_id: int):
        return VendorRepository.get_by_id(db, vendor_id)

    @staticmethod
    def get_all_vendors(db: Session):
        return VendorRepository.get_all(db)

    @staticmethod
    def update_vendor(db: Session, vendor_id: int, data: dict):
        vendor = VendorRepository.get_by_id(db, vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")

        return VendorRepository.update(db, vendor, data)

    @staticmethod
    def delete_vendor(db: Session, vendor_id: int):
        vendor = VendorRepository.get_by_id(db, vendor_id)
        if not vendor:
            raise ValueError("Vendor not found")

        return VendorRepository.delete(db, vendor)
