from flask import Blueprint
from src.controllers.task_controller import (
    create_task,
    get_all_tasks,
    get_tasks_by_project,
    get_task_by_id,
    update_task,
    delete_task,
)
from src.utils.jwt import token_required

task_bp = Blueprint("task", __name__, url_prefix="/api/v1/tasks")

@task_bp.route("/", methods=["POST"])
def create_task_route():
    return create_task()

@task_bp.route("/", methods=["GET"])
def get_tasks_route():
    return get_all_tasks()

@task_bp.route("/project/<int:project_id>", methods=["GET"])
def get_tasks_by_project_route(project_id):
    return get_tasks_by_project(project_id)

@task_bp.route("/<int:task_id>", methods=["GET"])
def get_task_by_id_route(task_id):
    return get_task_by_id(task_id)

@task_bp.route("/<int:task_id>", methods=["PUT"])
def update_task_route(task_id):
    return update_task(task_id)

@task_bp.route("/<int:task_id>", methods=["DELETE"])
def delete_task_route(task_id):
    return delete_task(task_id)
