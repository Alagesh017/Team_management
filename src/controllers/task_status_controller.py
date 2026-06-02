from flask import jsonify, request
from src import db
from src.models.task_status_model import TaskStatus

def create_task_status():
    try:
        data = request.get_json()
        
        name = data.get("name")
        color = data.get("color")
        sort_order = data.get("sort_order", 0)
        remark = data.get("remark")
        is_confidential = data.get("is_confidential", False)

        if not name:
            return jsonify({"msg": "Status name is required", "status": 0}), 400

        if TaskStatus.query.filter_by(name=name).first():
            return jsonify({"msg": f"Status '{name}' already exists", "status": 0}), 409

        new_status = TaskStatus(
            name=name,
            color=color,
            sort_order=sort_order,
            remark=remark,
            is_confidential=is_confidential
        )
        db.session.add(new_status)
        db.session.commit()
        
        return jsonify({"msg": "Task status created successfully", "status": 1, "id": new_status.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_task_statuses():
    try:
        statuses = TaskStatus.query.order_by(TaskStatus.sort_order.asc()).all()
        result = []
        for status in statuses:
            result.append({
                "id": status.id,
                "name": status.name,
                "color": status.color,
                "sort_order": status.sort_order,
                "remark": status.remark,
                "is_confidential": status.is_confidential,
                "created_at": status.created_at
            })
        return jsonify({"task_statuses": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_task_status_by_id(status_id):
    try:
        status = TaskStatus.query.get(status_id)
        if not status:
            return jsonify({"message": "Task status not found", "status": 0}), 404
        
        result = {
            "id": status.id,
            "name": status.name,
            "color": status.color,
            "sort_order": status.sort_order,
            "remark": status.remark,
            "is_confidential": status.is_confidential,
            "created_at": status.created_at
        }
        return jsonify({"task_status": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_task_status(status_id):
    try:
        status = TaskStatus.query.get(status_id)
        if not status:
            return jsonify({"message": "Task status not found", "status": 0}), 404

        data = request.get_json()
        
        if "name" in data:
            # Check if new name already exists for another record
            existing = TaskStatus.query.filter_by(name=data["name"]).first()
            if existing and existing.id != status_id:
                return jsonify({"msg": f"Status '{data['name']}' already exists", "status": 0}), 409
            status.name = data["name"]
        if "color" in data:
            status.color = data["color"]
        if "sort_order" in data:
            status.sort_order = data["sort_order"]
        if "remark" in data:
            status.remark = data["remark"]
        if "is_confidential" in data:
            status.is_confidential = data["is_confidential"]
            
        db.session.commit()
        return jsonify({"message": "Task status updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_task_status(status_id):
    try:
        status = TaskStatus.query.get(status_id)
        if not status:
            return jsonify({"message": "Task status not found", "status": 0}), 404
            
        db.session.delete(status)
        db.session.commit()
        return jsonify({"message": "Task status deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
