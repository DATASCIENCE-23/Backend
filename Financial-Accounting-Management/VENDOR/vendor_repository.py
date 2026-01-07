from database import db
from models.vendor_model import Vendor

class VendorRepository:
    def get_all(self):
        return Vendor.query.all()

    def get_by_id(self, vendor_id):
        return Vendor.query.get(vendor_id)

    def create(self, vendor_name, contact_info=None, gst_number=None):
        vendor = Vendor(vendor_name=vendor_name, contact_info=contact_info, gst_number=gst_number)
        db.session.add(vendor)
        db.session.commit()
        return vendor

    def update(self, vendor_id, **kwargs):
        vendor = self.get_by_id(vendor_id)
        if vendor:
            for key, value in kwargs.items():
                setattr(vendor, key, value)
            db.session.commit()
        return vendor

    def delete(self, vendor_id):
        vendor = self.get_by_id(vendor_id)
        if vendor:
            db.session.delete(vendor)
            db.session.commit()
        return vendor