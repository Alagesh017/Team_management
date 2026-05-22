from flask import Blueprint
from src.controllers.project_task_controller import get_project_task_data
from src.utils.jwt import token_required

project_task_bp = Blueprint("project_task", __name__, url_prefix="/api/v1/project-tasks")

@project_task_bp.route("/project/<int:project_id>", methods=["GET"])
@token_required
def get_project_task_data_route(decoded_payload, project_id):
    return get_project_task_data(project_id)
