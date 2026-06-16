from flask import Blueprint
from src.controllers.project_excel_controller import (
    create_project_excel,
    get_all_project_excels,
    get_excel_by_id,
    get_excels_by_project_id,
    update_project_excel,
    delete_project_excel,
)
from src.utils.jwt import token_required

project_excel_bp = Blueprint("project_excel", __name__, url_prefix="/api/v1/project-excels")

@project_excel_bp.route("/", methods=["POST"])
@token_required
def create_project_excel_route():
    return create_project_excel()

@project_excel_bp.route("/", methods=["GET"])
@token_required
def get_all_project_excels_route():
    return get_all_project_excels()

@project_excel_bp.route("/<int:excel_id>", methods=["GET"])
@token_required
def get_excel_by_id_route(excel_id):
    return get_excel_by_id(excel_id)

@project_excel_bp.route("/project/<int:project_id>", methods=["GET"])
@token_required
def get_excels_by_project_id_route(project_id):
    return get_excels_by_project_id(project_id)

@project_excel_bp.route("/<int:excel_id>", methods=["PUT"])
@token_required
def update_project_excel_route(excel_id):
    return update_project_excel(excel_id)

@project_excel_bp.route("/<int:excel_id>", methods=["DELETE"])
@token_required
def delete_project_excel_route(excel_id):
    return delete_project_excel(excel_id)
