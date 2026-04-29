import datetime
import bcrypt
from src import db
from flask import jsonify, request
from src.models.user_model import User
from src.utils.jwt import decode_jwt_token, generate_jwt_token


def register_controller():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")
        role = data.get("role", "user")

        if User.query.filter_by(username=username).first():
            return jsonify({"msg": "User already exists", "success": 2})

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        new_user = User(
            username=username, password=hashed_password.decode("utf-8"), role=role
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully", "status": 1}), 201

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def login_controller():

    try:

        data = request.get_json()

        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return (
                jsonify({"message": "Username and password required", "status": 0}),
                400,
            )

        user = User.query.filter_by(username=username).first()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return jsonify({"message": "Invalid credentials", "status": 0})

        additional_claims = {
            "user_id": user.id,
            "username": user.username,
            "role": user.role,
        }

        access_token = generate_jwt_token(user.id)
        refresh_token = generate_jwt_token(user.id, is_refresh=True)

        user.refresh_token = refresh_token
        user.refresh_token_created_at = datetime.datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "username": user.username,
                    "role": user.role,
                    "status": 1,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return (jsonify({"success": 0, "error": str(e)}), 500)


def token_refresh_controller():

    try:

        refresh_token = request.headers.get("Authorization")
        if not refresh_token or not refresh_token.startswith("Bearer "):
            return (
                jsonify({"message": "Refresh token missing or invalid", "status": 0}),
                400,
            )

        refresh_token = refresh_token.split(" ")[1]

        identity = decode_jwt_token(refresh_token)
        user = User.query.filter_by(id=identity["user_id"]).first()

        if not user:
            return jsonify({"message": "User not found", "status": 0}), 404

        if refresh_token != user.refresh_token:
            return jsonify({"message": "Invalid refresh token", "status": 0}), 401

        new_access_token = generate_jwt_token(user.id)
        new_refresh_token = generate_jwt_token(user.id, is_refresh=True)

        user.refresh_token = new_refresh_token
        user.token_created_at = datetime.datetime.utcnow()
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Access token refreshed",
                    "access_token": new_access_token,
                    "refresh_token": new_refresh_token,
                    "status": 1,
                }
            ),
            200,
        )
    except Exception as e:
        return (jsonify({"success": 0, "error": str(e)}), 500)
