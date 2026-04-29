from flask import Blueprint
from src.controllers.auth_controller import (
    login_controller,
    register_controller,
    token_refresh_controller,
)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


# Register route
@auth_bp.route("/register", methods=["POST"])
def register():
    return register_controller()


# Login route
@auth_bp.route("/login", methods=["POST"])
def login():
    return login_controller()


# Token Refresh route
@auth_bp.route("/refresh", methods=["POST"])
def token_refresh():
    return token_refresh_controller()


# @user_bp.route("/", methods=["GET"])
# @token_required
# def get_user(decoded_payload):
#     return get_user_controller()
