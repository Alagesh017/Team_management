import bcrypt
import datetime
from flask import jsonify, request, current_app
from src import db
from src.models.admin_model import Admin
from src.models.user_model import User
from src.utils.date_utils import parse_date
from src.utils.image_utils import save_image

def create_admin():
    try:
        data = request.get_json()
        
        email = data.get("email")
        password = "Dce@2026"
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        avatar_url = data.get("avatar_url")
        
        # Save image if provided as base64
        saved_url = save_image(avatar_url)
        final_avatar_url = saved_url if saved_url else avatar_url
        
        is_superadmin = data.get("is_superadmin", False)
        is_admin = data.get("is_admin", False)
        is_scrum = data.get("is_scrum", False)
        remark = data.get("remark")

        experience_years = data.get("experience_years")
        if experience_years == "":
            experience_years = None
        working_hours = data.get("working_hours")
        work_mode = data.get("work_mode")
        office_location = data.get("office_location")
        linkedin_url = data.get("linkedin_url")
        address_line1 = data.get("address_line1")
        address_line2 = data.get("address_line2")
        city = data.get("city")
        state = data.get("state")
        country = data.get("country")
        pincode = data.get("pincode")
        status = data.get("status", "ACTIVE")
        joining_date = parse_date(data.get("joining_date"))

        if not all([email]):
            return jsonify({"msg": "Email is mandatory", "status": 0}), 400

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
            email=email,
            avatar_url=final_avatar_url,
            is_superadmin=is_superadmin,
            is_admin=is_admin,
            is_scrum=is_scrum,
            experience_years=experience_years,
            working_hours=working_hours,
            work_mode=work_mode,
            office_location=office_location,
            linkedin_url=linkedin_url,
            address_line1=address_line1,
            address_line2=address_line2,
            city=city,
            state=state,
            country=country,
            pincode=pincode,
            status=status,
            joining_date=joining_date,
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
                "email": admin.email,
                "avatar_url": admin.avatar_url,
                "is_superadmin": admin.is_superadmin,
                "is_admin": admin.is_admin,
                "is_scrum": admin.is_scrum,
                "experience_years": admin.experience_years,
                "working_hours": admin.working_hours,
                "work_mode": admin.work_mode,
                "office_location": admin.office_location,
                "linkedin_url": admin.linkedin_url,
                "address_line1": admin.address_line1,
                "address_line2": admin.address_line2,
                "city": admin.city,
                "state": admin.state,
                "country": admin.country,
                "pincode": admin.pincode,
                "status": admin.status,
                "last_login": admin.last_login,
                "joining_date": admin.joining_date,
                "remark": admin.remark,
                "user_email": user.email if user else None,
                "is_active": user.is_active if user else None
            })
        return jsonify({"admins": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_admin_by_id(admin_id):
    try:
        admin = db.session.get(Admin, admin_id)
        if not admin:
            return jsonify({"message": "Admin not found", "status": 0}), 404
        
        user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
        result = {
            "id": admin.id,
            "first_name": admin.first_name,
            "last_name": admin.last_name,
            "phone": admin.phone,
            "email": admin.email,
            "avatar_url": admin.avatar_url,
            "is_superadmin": admin.is_superadmin,
            "is_admin": admin.is_admin,
            "is_scrum": admin.is_scrum,
            "experience_years": admin.experience_years,
            "working_hours": admin.working_hours,
            "work_mode": admin.work_mode,
            "office_location": admin.office_location,
            "linkedin_url": admin.linkedin_url,
            "address_line1": admin.address_line1,
            "address_line2": admin.address_line2,
            "city": admin.city,
            "state": admin.state,
            "country": admin.country,
            "pincode": admin.pincode,
            "status": admin.status,
            "last_login": admin.last_login,
            "joining_date": admin.joining_date,
            "remark": admin.remark,
            "user_email": user.email if user else None,
            "is_active": user.is_active if user else None
        }
        return jsonify({"admin": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_admin(admin_id):
    try:
        admin = db.session.get(Admin, admin_id)
        if not admin:
            return jsonify({"message": "Admin not found", "status": 0}), 404

        user = User.query.filter_by(role_id=admin.id).filter(User.role.in_(['superadmin', 'admin', 'scrum'])).first()
        data = request.get_json()
        
        if "avatar_url" in data:
            # Save image if provided as base64
            saved_url = save_image(data["avatar_url"])
            if saved_url:
                admin.avatar_url = saved_url
            else:
                # If save_image failed or wasn't base64, only update if it's not a super long string
                # or if it's a valid existing URL/path
                new_url = data["avatar_url"]
                if new_url and len(new_url) < 1000: # Safety check
                    admin.avatar_url = new_url
            
        if "first_name" in data:
            admin.first_name = data["first_name"]
        if "last_name" in data:
            admin.last_name = data["last_name"]
        if "email" in data:
            admin.email = data["email"]
            if user:
                user.email = data["email"]
        if "phone" in data:
            admin.phone = data["phone"]
        if "is_superadmin" in data:
            admin.is_superadmin = data["is_superadmin"]
        if "is_admin" in data:
            admin.is_admin = data["is_admin"]
        if "is_scrum" in data:
            admin.is_scrum = data["is_scrum"]
        if "experience_years" in data:
            exp_val = data["experience_years"]
            if exp_val == "":
                admin.experience_years = None
            else:
                admin.experience_years = exp_val
        if "working_hours" in data:
            admin.working_hours = data["working_hours"]
        if "work_mode" in data:
            admin.work_mode = data["work_mode"]
        if "office_location" in data:
            admin.office_location = data["office_location"]
        if "linkedin_url" in data:
            admin.linkedin_url = data["linkedin_url"]
        if "address_line1" in data:
            admin.address_line1 = data["address_line1"]
        if "address_line2" in data:
            admin.address_line2 = data["address_line2"]
        if "city" in data:
            admin.city = data["city"]
        if "state" in data:
            admin.state = data["state"]
        if "country" in data:
            admin.country = data["country"]
        if "pincode" in data:
            admin.pincode = data["pincode"]
        if "status" in data:
            admin.status = data["status"]
        if "joining_date" in data:
            admin.joining_date = parse_date(data["joining_date"])
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
