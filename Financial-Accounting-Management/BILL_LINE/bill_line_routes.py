from flask import Blueprint
from controllers.bill_line_controller import BillLineController

bill_line_bp = Blueprint("bill_line", __name__, url_prefix="/api/bill-lines")
controller = BillLineController()

bill_line_bp.route("/", methods=["GET"])(controller.get_all)
bill_line_bp.route("/bill/<int:bill_id>", methods=["GET"])(controller.get_by_bill)
bill_line_bp.route("/<int:bill_line_id>", methods=["GET"])(controller.get)
bill_line_bp.route("/", methods=["POST"])(controller.create)
bill_line_bp.route("/<int:bill_line_id>", methods=["PUT"])(controller.update)
bill_line_bp.route("/<int:bill_line_id>", methods=["DELETE"])(controller.delete)