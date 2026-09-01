from flask import Blueprint
from src.controllers.attendance_setting_controller import get_attendance_settings, save_attendance_settings
from src.utils.jwt import token_required

attendance_setting_bp = Blueprint("attendance_setting", __name__, url_prefix="/api/v1/attendance-settings")

@attendance_setting_bp.route("/", methods=["GET"])
@token_required
def get_settings_route(decoded_payload):
    return get_attendance_settings(decoded_payload)

@attendance_setting_bp.route("/", methods=["POST"])
@token_required
def save_settings_route(decoded_payload):
    return save_attendance_settings(decoded_payload)