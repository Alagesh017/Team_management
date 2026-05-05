from flask import jsonify, request
import datetime
from src import db
from src.models.task_model import Task
from src.utils.date_utils import parse_date

def create_task(decoded_payload):
    try:
        data = request.get_json()
        
        project_id = data.get("project_id")
        allocation_id = data.get("allocation_id")
        status_id = data.get("status_id")
        title = data.get("title")
        description = data.get("description")
        goal = data.get("goal")
        priority = data.get("priority", "medium")
        start_date_str = data.get("start_date")
        due_date_str = data.get("due_date")
        user_id = data.get("user_id") # assigned to
        estimated_hours = data.get("estimated_hours")
        actual_hours = data.get("actual_hours")
        remark = data.get("remark")
        
        assigned_by = decoded_payload.get("user_id")

        if not all([project_id, status_id, title, user_id]):
            return jsonify({"msg": "Project ID, Status ID, Title, and Assigned User ID are required", "status": 0}), 400

        start_date = parse_date(start_date_str)
        due_date = parse_date(due_date_str)

        new_task = Task(
            project_id=project_id,
            allocation_id=allocation_id,
            status_id=status_id,
            title=title,
            description=description,
            goal=goal,
            priority=priority,
            start_date=start_date,
            due_date=due_date,
            user_id=user_id,
            assigned_by=assigned_by,
            estimated_hours=estimated_hours,
            actual_hours=actual_hours,
            remark=remark
        )
        db.session.add(new_task)
        db.session.commit()
        
        return jsonify({"msg": "Task created successfully", "status": 1, "task_id": new_task.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_tasks():
    try:
        tasks = Task.query.all()
        result = []
        for task in tasks:
            result.append({
                "id": task.id,
                "project_id": task.project_id,
                "project_name": task.project.name if task.project else None,
                "allocation_id": task.allocation_id,
                "status_id": task.status_id,
                "status_name": task.status.name if task.status else None,
                "title": task.title,
                "description": task.description,
                "goal": task.goal,
                "priority": task.priority,
                "start_date": task.start_date.isoformat() if task.start_date else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "user_id": task.user_id,
                "assigned_to_email": task.assigned_user.email if task.assigned_user else None,
                "assigned_by": task.assigned_by,
                "assigned_by_email": task.assigner.email if task.assigner else None,
                "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
                "actual_hours": float(task.actual_hours) if task.actual_hours else None,
                "remark": task.remark,
                "created_at": task.created_at
            })
        return jsonify({"tasks": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_task_by_id(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found", "status": 0}), 404
        
        result = {
            "id": task.id,
            "project_id": task.project_id,
            "project_name": task.project.name if task.project else None,
            "allocation_id": task.allocation_id,
            "status_id": task.status_id,
            "status_name": task.status.name if task.status else None,
            "title": task.title,
            "description": task.description,
            "goal": task.goal,
            "priority": task.priority,
            "start_date": task.start_date.isoformat() if task.start_date else None,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "user_id": task.user_id,
            "assigned_to_email": task.assigned_user.email if task.assigned_user else None,
            "assigned_by": task.assigned_by,
            "assigned_by_email": task.assigner.email if task.assigner else None,
            "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
            "actual_hours": float(task.actual_hours) if task.actual_hours else None,
            "remark": task.remark,
            "created_at": task.created_at
        }
        return jsonify({"task": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found", "status": 0}), 404

        data = request.get_json()
        
        if "project_id" in data:
            task.project_id = data["project_id"]
        if "allocation_id" in data:
            task.allocation_id = data["allocation_id"]
        if "status_id" in data:
            task.status_id = data["status_id"]
        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "goal" in data:
            task.goal = data["goal"]
        if "priority" in data:
            task.priority = data["priority"]
        if "start_date" in data:
            task.start_date = parse_date(data["start_date"])
        if "due_date" in data:
            task.due_date = parse_date(data["due_date"])
        if "user_id" in data:
            task.user_id = data["user_id"]
        if "estimated_hours" in data:
            task.estimated_hours = data["estimated_hours"]
        if "actual_hours" in data:
            task.actual_hours = data["actual_hours"]
        if "remark" in data:
            task.remark = data["remark"]
            
        db.session.commit()
        return jsonify({"message": "Task updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found", "status": 0}), 404
            
        db.session.delete(task)
        db.session.commit()
        return jsonify({"message": "Task deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
