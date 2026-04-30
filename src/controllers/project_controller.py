from flask import jsonify, request
import datetime
from src import db
from src.models.project_model import Project

def create_project(decoded_payload):
    try:
        data = request.get_json()
        
        client_id = data.get("client_id")
        name = data.get("name")
        description = data.get("description")
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        status = data.get("status", "active")
        remark = data.get("remark")
        
        # User ID from the decoded JWT token
        created_by = decoded_payload.get("user_id")

        if not all([name, start_date_str, end_date_str]):
            return jsonify({"msg": "Project name, start date, and end date are required", "status": 0}), 400

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD", "status": 0}), 400

        new_project = Project(
            client_id=client_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            remark=remark,
            created_by=created_by
        )
        db.session.add(new_project)
        db.session.commit()
        
        return jsonify({"msg": "Project created successfully", "status": 1, "project_id": new_project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_projects():
    try:
        projects = Project.query.all()
        result = []
        for project in projects:
            result.append({
                "id": project.id,
                "client_id": project.client_id,
                "client_name": project.client.name if project.client else None,
                "name": project.name,
                "description": project.description,
                "start_date": project.start_date.isoformat(),
                "end_date": project.end_date.isoformat(),
                "status": project.status,
                "remark": project.remark,
                "created_by": project.created_by,
                "creator_email": project.creator.email if project.creator else None,
                "created_at": project.created_at
            })
        return jsonify({"projects": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_project_by_id(project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"message": "Project not found", "status": 0}), 404
        
        result = {
            "id": project.id,
            "client_id": project.client_id,
            "client_name": project.client.name if project.client else None,
            "name": project.name,
            "description": project.description,
            "start_date": project.start_date.isoformat(),
            "end_date": project.end_date.isoformat(),
            "status": project.status,
            "remark": project.remark,
            "created_by": project.created_by,
            "creator_email": project.creator.email if project.creator else None,
            "created_at": project.created_at
        }
        return jsonify({"project": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_project(project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"message": "Project not found", "status": 0}), 404

        data = request.get_json()
        
        if "client_id" in data:
            project.client_id = data["client_id"]
        if "name" in data:
            project.name = data["name"]
        if "description" in data:
            project.description = data["description"]
        if "start_date" in data:
            project.start_date = datetime.datetime.strptime(data["start_date"], '%Y-%m-%d').date()
        if "end_date" in data:
            project.end_date = datetime.datetime.strptime(data["end_date"], '%Y-%m-%d').date()
        if "status" in data:
            project.status = data["status"]
        if "remark" in data:
            project.remark = data["remark"]
            
        db.session.commit()
        return jsonify({"message": "Project updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_project(project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"message": "Project not found", "status": 0}), 404
            
        db.session.delete(project)
        db.session.commit()
        return jsonify({"message": "Project deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
