from flask import Blueprint
from src.controllers.task_attachment_controller import (
    create_attachment,
    get_all_attachments,
    get_attachment_by_id,
    update_attachment,
    delete_attachment,
)
from src.utils.jwt import token_required

task_attachment_bp = Blueprint("task_attachment", __name__, url_prefix="/api/v1/task_attachments")

@task_attachment_bp.route("/", methods=["POST"])
@token_required
def create_attachment_route(decoded_payload):
    return create_attachment(decoded_payload)

@task_attachment_bp.route("/", methods=["GET"])
@token_required
def get_attachments_route(decoded_payload):
    return get_all_attachments()

@task_attachment_bp.route("/<int:attachment_id>", methods=["GET"])
@token_required
def get_attachment_by_id_route(decoded_payload, attachment_id):
    return get_attachment_by_id(attachment_id)

@task_attachment_bp.route("/<int:attachment_id>", methods=["PUT"])
@token_required
def update_attachment_route(decoded_payload, attachment_id):
    return update_attachment(attachment_id)

@task_attachment_bp.route("/<int:attachment_id>", methods=["DELETE"])
@token_required
def delete_attachment_route(decoded_payload, attachment_id):
    return delete_attachment(attachment_id)
