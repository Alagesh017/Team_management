from flask import Blueprint
from src.controllers.leave_request_controller import (
    create_leave_request,
    get_all_leave_requests,
    get_my_leave_requests,
    review_leave_request,
    delete_leave_request,
)
from src.utils.jwt import token_required

leave_request_bp = Blueprint("leave_request", __name__, url_prefix="/api/v1/leave_requests")

@leave_request_bp.route("/", methods=["POST"])
@token_required
def create_leave_request_route(decoded_payload):
    return create_leave_request(decoded_payload)

@leave_request_bp.route("/", methods=["GET"])
@token_required
def get_all_leaves_route(decoded_payload):
    return get_all_leave_requests()

@leave_request_bp.route("/my", methods=["GET"])
@token_required
def get_my_leaves_route(decoded_payload):
    return get_my_leave_requests(decoded_payload)

@leave_request_bp.route("/review/<int:leave_id>", methods=["PUT"])
@token_required
def review_leave_route(decoded_payload, leave_id):
    return review_leave_request(leave_id, decoded_payload)

@leave_request_bp.route("/<int:leave_id>", methods=["DELETE"])
@token_required
def delete_leave_route(decoded_payload, leave_id):
    return delete_leave_request(leave_id, decoded_payload)
