from flask import Blueprint
from controllers.insurance_controller import InsuranceController

insurance_bp = Blueprint("insurance", __name__, url_prefix="/api/insurances")
controller = InsuranceController()

insurance_bp.route("/", methods=["GET"])(controller.get_all)
insurance_bp.route("/<int:insurance_id>", methods=["GET"])(controller.get)
insurance_bp.route("/", methods=["POST"])(controller.create)
insurance_bp.route("/<int:insurance_id>", methods=["PUT"])(controller.update)
insurance_bp.route("/<int:insurance_id>", methods=["DELETE"])(controller.delete)