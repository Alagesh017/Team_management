from flask import jsonify, request
import datetime
from src import db
from src.models.sub_task_model import SubTask

def create_sub_task(decoded_payload):
    try:
        data = request.get_json()
        
        parent_task_id = data.get("parent_task_id")
        status_id = data.get("status_id")
        title = data.get("title")
        description = data.get("description")
        priority = data.get("priority", "medium")
        start_date_str = data.get("start_date")
        due_date_str = data.get("due_date")
        user_id = data.get("user_id") # assigned to
        estimated_hours = data.get("estimated_hours")
        actual_hours = data.get("actual_hours")
        remark = data.get("remark")
        
        assigned_by = decoded_payload.get("user_id")

        if not all([parent_task_id, status_id, title, user_id]):
            return jsonify({"msg": "Parent Task ID, Status ID, Title, and Assigned User ID are required", "status": 0}), 400

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date() if start_date_str else None
            due_date = datetime.datetime.strptime(due_date_str, '%Y-%m-%d').date() if due_date_str else None
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD", "status": 0}), 400

        new_sub_task = SubTask(
            parent_task_id=parent_task_id,
            status_id=status_id,
            title=title,
            description=description,
            priority=priority,
            start_date=start_date,
            due_date=due_date,
            user_id=user_id,
            assigned_by=assigned_by,
            estimated_hours=estimated_hours,
            actual_hours=actual_hours,
            remark=remark
        )
        db.session.add(new_sub_task)
        db.session.commit()
        
        return jsonify({"msg": "SubTask created successfully", "status": 1, "sub_task_id": new_sub_task.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_sub_tasks():
    try:
        sub_tasks = SubTask.query.all()
        result = []
        for st in sub_tasks:
            result.append({
                "id": st.id,
                "parent_task_id": st.parent_task_id,
                "parent_task_title": st.parent_task.title if st.parent_task else None,
                "status_id": st.status_id,
                "status_name": st.status.name if st.status else None,
                "title": st.title,
                "description": st.description,
                "priority": st.priority,
                "start_date": st.start_date.isoformat() if st.start_date else None,
                "due_date": st.due_date.isoformat() if st.due_date else None,
                "user_id": st.user_id,
                "assigned_to_email": st.assigned_user.email if st.assigned_user else None,
                "assigned_by": st.assigned_by,
                "assigned_by_email": st.assigner.email if st.assigner else None,
                "estimated_hours": float(st.estimated_hours) if st.estimated_hours else None,
                "actual_hours": float(st.actual_hours) if st.actual_hours else None,
                "remark": st.remark,
                "created_at": st.created_at
            })
        return jsonify({"sub_tasks": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_sub_task_by_id(sub_task_id):
    try:
        st = SubTask.query.get(sub_task_id)
        if not st:
            return jsonify({"message": "SubTask not found", "status": 0}), 404
        
        result = {
            "id": st.id,
            "parent_task_id": st.parent_task_id,
            "parent_task_title": st.parent_task.title if st.parent_task else None,
            "status_id": st.status_id,
            "status_name": st.status.name if st.status else None,
            "title": st.title,
            "description": st.description,
            "priority": st.priority,
            "start_date": st.start_date.isoformat() if st.start_date else None,
            "due_date": st.due_date.isoformat() if st.due_date else None,
            "user_id": st.user_id,
            "assigned_to_email": st.assigned_user.email if st.assigned_user else None,
            "assigned_by": st.assigned_by,
            "assigned_by_email": st.assigner.email if st.assigner else None,
            "estimated_hours": float(st.estimated_hours) if st.estimated_hours else None,
            "actual_hours": float(st.actual_hours) if st.actual_hours else None,
            "remark": st.remark,
            "created_at": st.created_at
        }
        return jsonify({"sub_task": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_sub_task(sub_task_id):
    try:
        st = SubTask.query.get(sub_task_id)
        if not st:
            return jsonify({"message": "SubTask not found", "status": 0}), 404

        data = request.get_json()
        
        if "parent_task_id" in data:
            st.parent_task_id = data["parent_task_id"]
        if "status_id" in data:
            st.status_id = data["status_id"]
        if "title" in data:
            st.title = data["title"]
        if "description" in data:
            st.description = data["description"]
        if "priority" in data:
            st.priority = data["priority"]
        if "start_date" in data:
            st.start_date = datetime.datetime.strptime(data["start_date"], '%Y-%m-%d').date() if data["start_date"] else None
        if "due_date" in data:
            st.due_date = datetime.datetime.strptime(data["due_date"], '%Y-%m-%d').date() if data["due_date"] else None
        if "user_id" in data:
            st.user_id = data["user_id"]
        if "estimated_hours" in data:
            st.estimated_hours = data["estimated_hours"]
        if "actual_hours" in data:
            st.actual_hours = data["actual_hours"]
        if "remark" in data:
            st.remark = data["remark"]
            
        db.session.commit()
        return jsonify({"message": "SubTask updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_sub_task(sub_task_id):
    try:
        st = SubTask.query.get(sub_task_id)
        if not st:
            return jsonify({"message": "SubTask not found", "status": 0}), 404
            
        db.session.delete(st)
        db.session.commit()
        return jsonify({"message": "SubTask deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
