from flask import Blueprint
from src.controllers.worker_controller import (
    create_worker,
    get_all_workers,
    get_worker_by_id,
    update_worker,
    delete_worker,
)
from src.utils.jwt import token_required

worker_bp = Blueprint("worker", __name__, url_prefix="/api/v1/workers")

@worker_bp.route("/", methods=["POST"])
@token_required
def create_worker_route():
    return create_worker()

@worker_bp.route("/", methods=["GET"])
@token_required
def get_workers_route():
    return get_all_workers()

@worker_bp.route("/<int:worker_id>", methods=["GET"])
@token_required
def get_worker_by_id_route(worker_id):
    return get_worker_by_id(worker_id)

@worker_bp.route("/<int:worker_id>", methods=["PUT"])
@token_required
def update_worker_route(worker_id):
    return update_worker(worker_id)

@worker_bp.route("/<int:worker_id>", methods=["DELETE"])
@token_required
def delete_worker_route(worker_id): 
    return delete_worker(worker_id)
