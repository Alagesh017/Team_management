from flask import Blueprint
from src.controllers.task_status_controller import (
    create_task_status,
    get_all_task_statuses,
    get_task_status_by_id,
    update_task_status,
    delete_task_status,
    reorder_task_statuses,
)
from src.utils.jwt import token_required

task_status_bp = Blueprint("task_status", __name__, url_prefix="/api/v1/task-statuses")

@task_status_bp.route("/", methods=["POST"])
# @token_required
def create_task_status_route():
    return create_task_status()

@task_status_bp.route("/", methods=["GET"])
# @token_required
def get_task_statuses_route():
    return get_all_task_statuses()

@task_status_bp.route("/reorder", methods=["PUT"])
# @token_required
def reorder_task_statuses_route():
    return reorder_task_statuses()

@task_status_bp.route("/<int:status_id>", methods=["GET"])
# @token_required
def get_task_status_by_id_route(status_id):
    return get_task_status_by_id(status_id)

@task_status_bp.route("/<int:status_id>", methods=["PUT"])
# @token_required
def update_task_status_route(status_id):
    return update_task_status(status_id)

@task_status_bp.route("/<int:status_id>", methods=["DELETE"])
# @token_required
def delete_task_status_route(status_id):
    return delete_task_status(status_id)
