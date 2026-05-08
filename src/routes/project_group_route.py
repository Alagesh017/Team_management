from flask import Blueprint
from src.controllers.project_group_controller import (
    create_project_group,
    get_all_project_groups,
    get_project_group_by_id,
    update_project_group,
    delete_project_group,
    add_projects_to_group
)

project_group_bp = Blueprint("project_group", __name__, url_prefix="/api/v1/project-groups")

@project_group_bp.route("/", methods=["POST"])
def create_group_route():
    return create_project_group()

@project_group_bp.route("/", methods=["GET"])
def get_groups_route():
    return get_all_project_groups()

@project_group_bp.route("/<int:group_id>", methods=["GET"])
def get_group_by_id_route(group_id):
    return get_project_group_by_id(group_id)

@project_group_bp.route("/<int:group_id>", methods=["PUT"])
def update_group_route(group_id):
    return update_project_group(group_id)

@project_group_bp.route("/<int:group_id>", methods=["DELETE"])
def delete_group_route(group_id):
    return delete_project_group(group_id)

@project_group_bp.route("/<int:group_id>/add-projects", methods=["POST"])
def add_projects_route(group_id):
    return add_projects_to_group(group_id)
