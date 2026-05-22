import os
import uuid
import datetime
import bcrypt
import base64
from src import db
from flask import jsonify, request, current_app
from src.models.user_model import User
from src.models.admin_model import Admin
from src.models.worker_model import Worker
from src.utils.jwt import decode_jwt_token, generate_jwt_token
from src.utils.image_utils import save_image

def register_controller():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")
        role = data.get("role")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        avatar_url = data.get("avatar_url")

        if not all([email, password, role]):
            return jsonify({"msg": "Email, Password and Role are mandatory", "status": 0}), 400

        valid_roles = ["superadmin", "admin", "scrum", "team_leader", "worker"]
        if role not in valid_roles:
            return jsonify({"msg": f"Invalid role. Must be one of {valid_roles}", "status": 0}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User with this email already exists", "status": 0}), 409

        # Save image if provided
        final_avatar_url = save_image(avatar_url) or avatar_url

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Create Admin or Worker based on role
        role_id = None
        if role in ["superadmin", "admin", "scrum"]:
            new_person = Admin(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                email=email,
                avatar_url=final_avatar_url,
                is_superadmin=(role == "superadmin"),
                is_admin=(role == "admin"),
                is_scrum=(role == "scrum")
            )
            db.session.add(new_person)
            db.session.flush()
            role_id = new_person.id
            
        elif role in ["team_leader", "worker"]:
            new_person = Worker(
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                avatar_url=final_avatar_url,
                is_tl=(role == "team_leader"),
                is_worker=(role == "worker")
            )
            db.session.add(new_person)
            db.session.flush()
            role_id = new_person.id

        new_user = User(
            email=email, password=hashed_password.decode("utf-8"), role=role, role_id=role_id
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "User registered successfully", "status": 1}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500


def login_controller():
    try:
        data = request.get_json()

        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return jsonify({"message": "Email and password required", "status": 0}), 400

        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            return jsonify({"message": "Invalid credentials", "status": 0}), 401

        if not user.is_active:
            return jsonify({"message": "User account is inactive", "status": 0}), 403

        access_token = generate_jwt_token(user.id, user.role_id, user.role)
        refresh_token = generate_jwt_token(user.id, user.role_id, user.role, is_refresh=True)

        user.refresh_token = refresh_token
        user.refresh_token_created_at = datetime.datetime.utcnow()
        
        # Update last_login for Admin if applicable
        if user.role in ["superadmin", "admin", "scrum"]:
            admin = Admin.query.get(user.role_id)
            if admin:
                admin.last_login = datetime.datetime.utcnow()
                
        db.session.commit()

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": user.email,
            "role": user.role,
            "user_id": user.id,
            "role_id": user.role_id,
            "status": 1,
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500


def google_login_controller():
    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({"message": "Email is required", "status": 0}), 400

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "User with this Google account not found. Please register first.", "status": 0}), 404

        if not user.is_active:
            return jsonify({"message": "User account is inactive", "status": 0}), 403

        access_token = generate_jwt_token(user.id, user.role_id, user.role)
        refresh_token = generate_jwt_token(user.id, user.role_id, user.role, is_refresh=True)

        user.refresh_token = refresh_token
        user.refresh_token_created_at = datetime.datetime.utcnow()
        
        if user.role in ["superadmin", "admin", "scrum"]:
            admin = Admin.query.get(user.role_id)
            if admin:
                admin.last_login = datetime.datetime.utcnow()
                
        db.session.commit()

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "email": user.email,
            "role": user.role,
            "user_id": user.id,
            "role_id": user.role_id,
            "status": 1,
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500


def token_refresh_controller():
    try:
        refresh_token = request.headers.get("Authorization")
        if not refresh_token or not refresh_token.startswith("Bearer "):
            return jsonify({"message": "Refresh token missing or invalid", "status": 0}), 400

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
        user.refresh_token_created_at = datetime.datetime.utcnow() # Fixed typo from token_created_at
        db.session.commit()

        return jsonify({
            "message": "Access token refreshed",
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "status": 1,
        }), 200
        
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500
