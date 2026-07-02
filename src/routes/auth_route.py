from flask import Blueprint
from src.controllers.auth_controller import (
    login_controller,
    register_controller,
    token_refresh_controller,
    google_login_controller,
    microsoft_login_controller,
    forgot_password_controller,
    verify_otp_controller,
    reset_password_controller,
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


# Google Login route
@auth_bp.route("/google-login", methods=["POST"])
def google_login():
    return google_login_controller()


# Microsoft Login route
@auth_bp.route("/microsoft-login", methods=["POST"])
def microsoft_login():
    return microsoft_login_controller()


# Token Refresh route
@auth_bp.route("/refresh", methods=["POST"])
def token_refresh():
    return token_refresh_controller()


# Forgot Password route
@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():
    return forgot_password_controller()


# Verify OTP route
@auth_bp.route("/verify-otp", methods=["POST"])
def verify_otp():
    return verify_otp_controller()


# Reset Password route
@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():
    return reset_password_controller()
