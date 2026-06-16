from flask import Blueprint
from src.controllers.project_controller import (
    create_project,
    get_all_projects,
    get_project_by_id,
    update_project,
    delete_project,
)
from src.utils.jwt import token_required

project_bp = Blueprint("project", __name__, url_prefix="/api/v1/projects")

@project_bp.route("/", methods=["POST"])
@token_required
def create_project_route():
    return create_project()

@project_bp.route("/", methods=["GET"])
@token_required
def get_projects_route():
    return get_all_projects()

@project_bp.route("/<int:project_id>", methods=["GET"])
@token_required
def get_project_by_id_route(project_id):
    return get_project_by_id(project_id)

@project_bp.route("/<int:project_id>", methods=["PUT"])
@token_required
def update_project_route(project_id):
    return update_project(project_id)

@project_bp.route("/<int:project_id>", methods=["DELETE"])
@token_required
def delete_project_route(project_id):
    return delete_project(project_id)
