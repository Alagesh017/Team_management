from flask import jsonify, request
import bcrypt
from src import db
from src.models.admin_model import Admin
from src.models.user_model import User

def create_admin():
    try:
        data = request.get_json()
        
        email = data.get("email")
        password = "Dce@2026"
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        
        is_superadmin = data.get("is_superadmin", False)
        is_admin = data.get("is_admin", False)
        is_scrum = data.get("is_scrum", False)
        remark = data.get("remark")

        if not all([email, first_name, last_name]):
            return jsonify({"msg": "Missing required fields", "status": 0}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User with this email already exists", "status": 0}), 409

        # Determine role based on boolean values
        role = "admin" # default
        if is_superadmin:
            role = "superadmin"
        elif is_admin:
            role = "admin"
        elif is_scrum:
            role = "scrum"

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # 1. Create Admin
        new_admin = Admin(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_superadmin=is_superadmin,
            is_admin=is_admin,
            is_scrum=is_scrum,
            remark=remark
        )
        db.session.add(new_admin)
        db.session.flush()

        # 2. Create User
        new_user = User(
            email=email, password=hashed_password.decode("utf-8"), role=role, role_id=new_admin.id
        )
        db.session.add(new_user)
        
        db.session.commit()
        return jsonify({"msg": "Admin created successfully", "status": 1}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_admins():
    try:
        admins = Admin.query.all()
        result = []
        for admin in admins:
            user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
            result.append({
                "id": admin.id,
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "phone": admin.phone,
                "avatar_url": admin.avatar_url,
                "is_superadmin": admin.is_superadmin,
                "is_admin": admin.is_admin,
                "is_scrum": admin.is_scrum,
                "remark": admin.remark,
                "email": user.email if user else None,
                "is_active": user.is_active if user else None
            })
        return jsonify({"admins": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_admin_by_id(admin_id):
    try:
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({"message": "Admin not found", "status": 0}), 404
        
        user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
        result = {
            "id": admin.id,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "phone": admin.phone,
            "avatar_url": admin.avatar_url,
            "is_superadmin": admin.is_superadmin,
            "is_admin": admin.is_admin,
            "is_scrum": admin.is_scrum,
            "remark": admin.remark,
            "email": user.email if user else None,
            "is_active": user.is_active if user else None
        }
        return jsonify({"admin": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_admin(admin_id):
    try:
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({"message": "Admin not found", "status": 0}), 404

        user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
        data = request.get_json()
        
        if "first_name" in data:
            admin.first_name = data["first_name"]
        if "last_name" in data:
            admin.last_name = data["last_name"]
        if "phone" in data:
            admin.phone = data["phone"]
        if "avatar_url" in data:
            admin.avatar_url = data["avatar_url"]
        if "is_superadmin" in data:
            admin.is_superadmin = data["is_superadmin"]
        if "is_admin" in data:
            admin.is_admin = data["is_admin"]
        if "is_scrum" in data:
            admin.is_scrum = data["is_scrum"]
        if "remark" in data:
            admin.remark = data["remark"]
            
        if "is_active" in data and user:
            user.is_active = data["is_active"]

        # Sync User role if it has changed based on booleans
        if user:
            if admin.is_superadmin:
                user.role = "superadmin"
            elif admin.is_admin:
                user.role = "admin"
            elif admin.is_scrum:
                user.role = "scrum"

        db.session.commit()
        return jsonify({"message": "Admin updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_admin(admin_id):
    try:
        admin = Admin.query.get(admin_id)
        if not admin:
            return jsonify({"message": "Admin not found", "status": 0}), 404
            
        user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
        if user:
            db.session.delete(user)
            
        db.session.delete(admin)
        db.session.commit()
        return jsonify({"message": "Admin deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
