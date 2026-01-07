from repositories.vendor_repository import VendorRepository

class VendorService:
    def __init__(self):
        self.repo = VendorRepository()

    def get_all_vendors(self):
        vendors = self.repo.get_all()
        return [v.to_dict() for v in vendors]

    def get_vendor(self, vendor_id):
        vendor = self.repo.get_by_id(vendor_id)
        return vendor.to_dict() if vendor else None

    def create_vendor(self, data):
        # Add any business validation here
        vendor = self.repo.create(
            vendor_name=data["vendor_name"],
            contact_info=data.get("contact_info"),
            gst_number=data.get("gst_number")
        )
        return vendor.to_dict()

    def update_vendor(self, vendor_id, data):
        vendor = self.repo.update(vendor_id, **data)
        return vendor.to_dict() if vendor else None

    def delete_vendor(self, vendor_id):
        return self.repo.delete(vendor_id) is not None