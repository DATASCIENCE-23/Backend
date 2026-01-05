from flask import jsonify, request
from services.bill_line_service import BillLineService

class BillLineController:
    def __init__(self):
        self.service = BillLineService()

    def get_all(self):
        lines = self.service.get_all_lines()
        return jsonify(lines), 200

    def get(self, bill_line_id):
        line = self.service.get_line(bill_line_id)
        if line:
            return jsonify(line), 200
        return jsonify({"error": "Bill line not found"}), 404

    def get_by_bill(self, bill_id):
        lines = self.service.get_lines_by_bill(bill_id)
        return jsonify(lines), 200

    def create(self):
        data = request.get_json()
        line = self.service.create_line(data)
        return jsonify(line), 201

    def update(self, bill_line_id):
        data = request.get_json()
        line = self.service.update_line(bill_line_id, data)
        if line:
            return jsonify(line), 200
        return jsonify({"error": "Bill line not found"}), 404

    def delete(self, bill_line_id):
        success = self.service.delete_line(bill_line_id)
        if success:
            return jsonify({"message": "Bill line deleted"}), 200
        return jsonify({"error": "Bill line not found"}), 404