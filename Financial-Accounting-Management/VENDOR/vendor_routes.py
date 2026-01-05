from flask import Blueprint
from controllers.vendor_controller import VendorController

vendor_bp = Blueprint("vendor", __name__, url_prefix="/api/vendors")
controller = VendorController()

vendor_bp.route("/", methods=["GET"])(controller.get_all)
vendor_bp.route("/<int:vendor_id>", methods=["GET"])(controller.get)
vendor_bp.route("/", methods=["POST"])(controller.create)
vendor_bp.route("/<int:vendor_id>", methods=["PUT"])(controller.update)
vendor_bp.route("/<int:vendor_id>", methods=["DELETE"])(controller.delete)