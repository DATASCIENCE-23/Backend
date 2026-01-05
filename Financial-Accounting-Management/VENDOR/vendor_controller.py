from flask import jsonify, request
from services.vendor_service import VendorService

class VendorController:
    def __init__(self):
        self.service = VendorService()

    def get_all(self):
        vendors = self.service.get_all_vendors()
        return jsonify(vendors), 200

    def get(self, vendor_id):
        vendor = self.service.get_vendor(vendor_id)
        if vendor:
            return jsonify(vendor), 200
        return jsonify({"error": "Vendor not found"}), 404

    def create(self):
        data = request.get_json()
        vendor = self.service.create_vendor(data)
        return jsonify(vendor), 201

    def update(self, vendor_id):
        data = request.get_json()
        vendor = self.service.update_vendor(vendor_id, data)
        if vendor:
            return jsonify(vendor), 200
        return jsonify({"error": "Vendor not found"}), 404

    def delete(self, vendor_id):
        success = self.service.delete_vendor(vendor_id)
        if success:
            return jsonify({"message": "Deleted"}), 200
        return jsonify({"error": "Vendor not found"}), 404