from flask import jsonify, request
import datetime
from src import db
from src.models.project_model import Project
from src.models.project_allocation_model import ProjectAllocation
from src.utils.date_utils import parse_date
from src.utils.image_utils import save_image
from src.utils.role_utils import get_person_details

def create_project(decoded_payload=None):
    try:
        data = request.get_json()
        print(data)
        
        client_id = data.get("client_id")
        name = data.get("name")
        description = data.get("description")
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        status = data.get("status", "active")
        group_id = data.get("group_id")

        remark = data.get("remark")
        project_logo = data.get("project_logo")
        by_tl_managed = data.get("by_tl_managed", False)
        team_managed = data.get("team_managed", False)
        company_managed = data.get("company_managed", False)
        
        # Save project logo if provided as base64
        saved_logo_url = save_image(project_logo, folder="project_logos")
        final_logo_url = saved_logo_url if saved_logo_url else project_logo
        
        created_by_role_id = decoded_payload.get("role_id") if decoded_payload else None
        created_by_role = decoded_payload.get("role") if decoded_payload else None
        
        if not all([name, start_date_str, end_date_str]):
            return jsonify({"msg": "Project name, start date, end date, and creator are required", "status": 0}), 400

        start_date = parse_date(start_date_str)
        end_date = parse_date(end_date_str)

        if not start_date or not end_date:
            return jsonify({"msg": "Invalid date format", "status": 0}), 400

        new_project = Project(
            client_id=client_id,
            name=name,
            group_id=group_id,
            description=description,
            start_date=start_date,
            end_date=end_date,
            status=status,
            project_logo=final_logo_url,
            remark=remark,
            by_tl_managed=by_tl_managed,
            team_managed=team_managed,
            company_managed=company_managed,
            created_by_role_id=created_by_role_id,
            created_by_role=created_by_role
        )
        db.session.add(new_project)
        db.session.commit()
        
        # Automatically create a project allocation entry
        new_allocation = ProjectAllocation(
            project_id=new_project.id,
            members=[], # Default empty members as requested
            start_date=start_date,
            end_date=end_date,
            remark=remark,
            allocated_by_role_id=created_by_role_id,
            allocated_by_role=created_by_role
        )
        db.session.add(new_allocation)
        db.session.commit()
        
        return jsonify({"msg": "Project created successfully and allocation initialized", "status": 1, "project_id": new_project.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_projects():
    try:
        role = request.args.get("role")
        role_id = request.args.get("role_id")
        if role_id:
            role_id = int(role_id)
        
        projects = Project.query.all()
        
        # Filter projects for team_leader or worker based on allocation
        if role in ["team_leader", "worker"] and role_id:
            filtered_project_ids = []
            allocations = ProjectAllocation.query.all()
            for allocation in allocations:
                members = allocation.members or []
                for member in members:
                    if member.get("user_id") == role_id:
                        filtered_project_ids.append(allocation.project_id)
                        break
            
            # Filter projects to only those in filtered_project_ids
            projects = [p for p in projects if p.id in filtered_project_ids]
        
        result = []
        for project in projects:
            created_by_person = get_person_details(project.created_by_role, project.created_by_role_id)
            result.append({
                "id": project.id,
                "client_id": project.client_id,
                "client_name": project.client.name if project.client else None,
                "name": project.name,
                "group_id": project.group_id,
                "group_name": project.group.name if project.group else None,
                "description": project.description,
                "start_date": project.start_date.isoformat(),
                "end_date": project.end_date.isoformat(),
                "status": project.status,
                "project_logo": project.project_logo,
                "remark": project.remark,
                "by_tl_managed": project.by_tl_managed,
                "team_managed": project.team_managed,
                "company_managed": project.company_managed,
                "created_by_role_id": project.created_by_role_id,
                "created_by_role": project.created_by_role,
                "created_by_person": created_by_person,
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
        
        created_by_person = get_person_details(project.created_by_role, project.created_by_role_id)
        result = {
            "id": project.id,
            "client_id": project.client_id,
            "client_name": project.client.name if project.client else None,
            "group_id": project.group_id,
            "group_name": project.group.name if project.group else None,
            "name": project.name,
            "description": project.description,
            "start_date": project.start_date.isoformat(),
            "end_date": project.end_date.isoformat(),
            "status": project.status,
            "project_logo": project.project_logo,
            "remark": project.remark,
            "by_tl_managed": project.by_tl_managed,
            "team_managed": project.team_managed,
            "company_managed": project.company_managed,
            "created_by_role_id": project.created_by_role_id,
            "created_by_role": project.created_by_role,
            "created_by_person": created_by_person,
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
        if "group_id" in data:
            project.group_id = data["group_id"]
        if "name" in data:
            project.name = data["name"]
        if "description" in data:
            project.description = data["description"]
        if "start_date" in data:
            project.start_date = parse_date(data["start_date"])
        if "end_date" in data:
            project.end_date = parse_date(data["end_date"])
        if "status" in data:
            project.status = data["status"]
        if "project_logo" in data:
            project_logo = data.get("project_logo")
            saved_logo_url = save_image(project_logo, folder="project_logos")
            project.project_logo = saved_logo_url if saved_logo_url else project_logo
        if "remark" in data:
            project.remark = data["remark"]
        if "by_tl_managed" in data:
            project.by_tl_managed = data["by_tl_managed"]
        if "team_managed" in data:
            project.team_managed = data["team_managed"]
        if "company_managed" in data:
            project.company_managed = data["company_managed"]
            
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
