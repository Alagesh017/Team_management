from flask import Blueprint
from src.controllers.admin_controller import (
    create_admin,
    get_all_admins,
    get_admin_by_id,
    update_admin,
    delete_admin,
)
from src.utils.jwt import token_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admins")


# ➕ Create Admin (no token for now)
@admin_bp.route("/", methods=["POST"])
def create_admin_route():
    return create_admin()


# 📄 Get all admins
@admin_bp.route("/", methods=["GET"])
@token_required
def get_admins_route(decoded_payload):
    return get_all_admins()


# 🔍 Get admin by ID
@admin_bp.route("/<int:admin_id>", methods=["GET"])
@token_required
def get_admin_by_id_route(decoded_payload, admin_id):
    return get_admin_by_id(admin_id)


# ✏️ Update admin
@admin_bp.route("/<int:admin_id>", methods=["PUT"])
@token_required
def update_admin_route(decoded_payload, admin_id):
    return update_admin(admin_id)


# ❌ Delete admin
@admin_bp.route("/<int:admin_id>", methods=["DELETE"])
@token_required
def delete_admin_route(decoded_payload, admin_id):
    return delete_admin(admin_id)