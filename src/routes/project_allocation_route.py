from flask import Blueprint
from src.controllers.project_allocation_controller import (
    create_allocation,
    get_all_allocations,
    get_allocation_by_id,
    get_allocation_by_project_id,
    update_allocation,
    update_allocation_members,
    delete_allocation,
)
from src.utils.jwt import token_required

project_allocation_bp = Blueprint("project_allocation", __name__, url_prefix="/api/v1/project-allocations")

@project_allocation_bp.route("/", methods=["POST"])
# @token_required
def create_allocation_route():
    return create_allocation()

@project_allocation_bp.route("/", methods=["GET"])
# @token_required
def get_allocations_route():
    return get_all_allocations()

@project_allocation_bp.route("/<int:allocation_id>", methods=["GET"])
def get_allocation_by_id_route(allocation_id):
    return get_allocation_by_id(allocation_id)

@project_allocation_bp.route("/project/<int:project_id>", methods=["GET"])
def get_allocation_by_project_id_route(project_id):
    return get_allocation_by_project_id(project_id)

@project_allocation_bp.route("/<int:allocation_id>", methods=["PUT"])
def update_allocation_route(allocation_id):
    return update_allocation(allocation_id)

@project_allocation_bp.route("/<int:allocation_id>/members", methods=["PUT"])
# @token_required
def update_allocation_members_route(allocation_id):
    return update_allocation_members(allocation_id)

@project_allocation_bp.route("/<int:allocation_id>", methods=["DELETE"])
# @token_required
def delete_allocation_route(allocation_id):
    return delete_allocation(allocation_id)
