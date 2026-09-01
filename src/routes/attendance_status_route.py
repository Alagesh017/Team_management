from flask import Blueprint
from src.controllers.attendance_status_controller import (
    create_attendance_status,
    get_all_attendance_statuses,
    get_attendance_status_by_id,
    update_attendance_status,
    delete_attendance_status,
)
from src.utils.jwt import token_required

attendance_status_bp = Blueprint("attendance_status", __name__, url_prefix="/api/v1/attendance-statuses")

@attendance_status_bp.route("/", methods=["POST"])
@token_required
def create_attendance_status_route(decoded_payload):
    return create_attendance_status(decoded_payload)

@attendance_status_bp.route("/", methods=["GET"])
@token_required
def get_attendance_statuses_route(decoded_payload):
    return get_all_attendance_statuses(decoded_payload)

@attendance_status_bp.route("/<int:status_id>", methods=["GET"])
@token_required
def get_attendance_status_by_id_route(decoded_payload, status_id):
    return get_attendance_status_by_id(status_id, decoded_payload)

@attendance_status_bp.route("/<int:status_id>", methods=["PUT"])
@token_required
def update_attendance_status_route(decoded_payload, status_id):
    return update_attendance_status(status_id, decoded_payload)

@attendance_status_bp.route("/<int:status_id>", methods=["DELETE"])
@token_required
def delete_attendance_status_route(decoded_payload, status_id):    
    return delete_attendance_status(status_id, decoded_payload)
