from flask import Blueprint
from src.controllers.task_controller import (
    create_task,
    get_all_tasks,
    get_task_by_id,
    update_task,
    delete_task,
)
from src.utils.jwt import token_required

task_bp = Blueprint("task", __name__, url_prefix="/api/v1/tasks")

@task_bp.route("/", methods=["POST"])
@token_required
def create_task_route(decoded_payload):
    return create_task(decoded_payload)

@task_bp.route("/", methods=["GET"])
@token_required
def get_tasks_route(decoded_payload):
    return get_all_tasks()

@task_bp.route("/<int:task_id>", methods=["GET"])
@token_required
def get_task_by_id_route(decoded_payload, task_id):
    return get_task_by_id(task_id)

@task_bp.route("/<int:task_id>", methods=["PUT"])
@token_required
def update_task_route(decoded_payload, task_id):
    return update_task(task_id)

@task_bp.route("/<int:task_id>", methods=["DELETE"])
@token_required
def delete_task_route(decoded_payload, task_id):
    return delete_task(task_id)
