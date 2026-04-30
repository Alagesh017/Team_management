from flask import jsonify, request
import bcrypt
from src import db
from src.models.worker_model import Worker
from src.models.user_model import User

def create_worker():
    try:
        data = request.get_json()
        
        email = data.get("email")
        password = "Dce@2026"
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        
        is_tl = data.get("is_tl", False)
        is_worker = data.get("is_worker", False)
        remark = data.get("remark")

        if not all([email, first_name, last_name]):
            return jsonify({"msg": "Missing required fields", "status": 0}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({"msg": "User with this email already exists", "status": 0}), 409

        # Determine role based on boolean values
        role = "worker" # default
        if is_tl:
            role = "team_leader"
        elif is_worker:
            role = "worker"

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # 1. Create Worker
        new_worker = Worker(
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            is_tl=is_tl,
            is_worker=is_worker,
            remark=remark
        )
        db.session.add(new_worker)
        db.session.flush()

        # 2. Create User
        new_user = User(
            email=email, password=hashed_password.decode("utf-8"), role=role, role_id=new_worker.id
        )
        db.session.add(new_user)
        
        db.session.commit()
        return jsonify({"msg": "Worker created successfully", "status": 1}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_workers():
    try:
        workers = Worker.query.all()
        result = []
        for worker in workers:
            user = User.query.filter_by(role_id=worker.id).filter(User.role.in_(['team_leader', 'worker'])).first()
            result.append({
                "id": worker.id,
                "first_name": worker.first_name,
                "last_name": worker.last_name,
                "phone": worker.phone,
                "avatar_url": worker.avatar_url,
                "is_tl": worker.is_tl,
                "is_worker": worker.is_worker,
                "remark": worker.remark,
                "email": user.email if user else None,
                "is_active": user.is_active if user else None
            })
        return jsonify({"workers": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_worker_by_id(worker_id):
    try:
        worker = Worker.query.get(worker_id)
        if not worker:
            return jsonify({"message": "Worker not found", "status": 0}), 404
        
        user = User.query.filter_by(role_id=worker.id).filter(User.role.in_(['team_leader', 'worker'])).first()
        result = {
            "id": worker.id,
            "first_name": worker.first_name,
            "last_name": worker.last_name,
            "phone": worker.phone,
            "avatar_url": worker.avatar_url,
            "is_tl": worker.is_tl,
            "is_worker": worker.is_worker,
            "remark": worker.remark,
            "email": user.email if user else None,
            "is_active": user.is_active if user else None
        }
        return jsonify({"worker": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_worker(worker_id):
    try:
        worker = Worker.query.get(worker_id)
        if not worker:
            return jsonify({"message": "Worker not found", "status": 0}), 404

        user = User.query.filter_by(role_id=worker.id).filter(User.role.in_(['team_leader', 'worker'])).first()
        data = request.get_json()
        
        if "first_name" in data:
            worker.first_name = data["first_name"]
        if "last_name" in data:
            worker.last_name = data["last_name"]
        if "phone" in data:
            worker.phone = data["phone"]
        if "avatar_url" in data:
            worker.avatar_url = data["avatar_url"]
        if "is_tl" in data:
            worker.is_tl = data["is_tl"]
        if "is_worker" in data:
            worker.is_worker = data["is_worker"]
        if "remark" in data:
            worker.remark = data["remark"]
            
        if "is_active" in data and user:
            user.is_active = data["is_active"]

        # Sync User role if it has changed based on booleans
        if user:
            if worker.is_tl:
                user.role = "team_leader"
            elif worker.is_worker:
                user.role = "worker"

        db.session.commit()
        return jsonify({"message": "Worker updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_worker(worker_id):
    try:
        worker = Worker.query.get(worker_id)
        if not worker:
            return jsonify({"message": "Worker not found", "status": 0}), 404
            
        user = User.query.filter_by(role_id=worker.id).filter(User.role.in_(['team_leader', 'worker'])).first()
        if user:
            db.session.delete(user)
            
        db.session.delete(worker)
        db.session.commit()
        return jsonify({"message": "Worker deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
