from flask import Blueprint
from src.controllers.project_member_controller import get_project_members
from src.utils.jwt import token_required

project_member_bp = Blueprint("project_member", __name__, url_prefix="/api/v1/project-members")

@project_member_bp.route("/project/<int:project_id>", methods=["GET"])
@token_required
def get_project_members_route(decoded_payload, project_id):
    return get_project_members(project_id)
