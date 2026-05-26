from flask import jsonify, request
import datetime
from src import db
from src.models.project_allocation_model import ProjectAllocation
from src.utils.role_utils import get_person_details

def create_allocation(decoded_payload=None):
    try:
        data = request.get_json()
        print(data)
        
        project_id = data.get("project_id")
        members = data.get("members", []) # Default to empty list
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        remark = data.get("remark")
        
        allocated_by_role_id = data.get("role_id")
        allocated_by_role = data.get("role")
        
        if not all([project_id, start_date_str, allocated_by_role_id, allocated_by_role]):
            return jsonify({"msg": "Project ID, start date, role_id, and role are required", "status": 0}), 400

        if members and not isinstance(members, list):
            return jsonify({"msg": "Members must be a JSON array", "status": 0}), 400

        try:
            start_date = datetime.datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.datetime.strptime(end_date_str, '%Y-%m-%d').date() if end_date_str else None
        except ValueError:
            return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD", "status": 0}), 400

        new_allocation = ProjectAllocation(
            project_id=project_id,
            members=members,
            start_date=start_date,
            end_date=end_date,
            remark=remark,
            allocated_by_role_id=allocated_by_role_id,
            allocated_by_role=allocated_by_role
        )
        db.session.add(new_allocation)
        db.session.commit()
        
        return jsonify({"msg": "Project allocation created successfully", "status": 1, "id": new_allocation.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_allocations():
    try:
        allocations = ProjectAllocation.query.all()
        result = []
        for alloc in allocations:
            allocated_by_person = get_person_details(alloc.allocated_by_role, alloc.allocated_by_role_id)
            # Enrich members
            enriched_members = []
            if alloc.members:
                for member in alloc.members:
                    member_role = member.get("role")
                    member_role_id = member.get("role_id")
                    if member_role and member_role_id:
                        member_details = get_person_details(member_role, member_role_id)
                        if member_details:
                            enriched_members.append(member_details)
                        else:
                            enriched_members.append(member)
                    else:
                        enriched_members.append(member)
            result.append({
                "id": alloc.id,
                "project_id": alloc.project_id,
                "project_name": alloc.project.name if alloc.project else None,
                "project_logo": alloc.project.project_logo if alloc.project else None,
                "members": enriched_members,
                "start_date": alloc.start_date.isoformat(),
                "end_date": alloc.end_date.isoformat() if alloc.end_date else None,
                "remark": alloc.remark,
                "allocated_by_role_id": alloc.allocated_by_role_id,
                "allocated_by_role": alloc.allocated_by_role,
                "allocated_by_person": allocated_by_person,
                "created_at": alloc.created_at
            })
        return jsonify({"allocations": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_allocation_by_project_id(project_id):
    try:
        alloc = ProjectAllocation.query.filter_by(project_id=project_id).first()
        if not alloc:
            # Return empty structure if not found
            return jsonify({
                "allocation": {
                    "project_id": project_id,
                    "members": [],
                }, 
                "status": 1
            }), 200
        
        allocated_by_person = get_person_details(alloc.allocated_by_role, alloc.allocated_by_role_id)
        # Enrich members
        enriched_members = []
        if alloc.members:
            for member in alloc.members:
                member_role = member.get("role")
                member_role_id = member.get("role_id")
                if member_role and member_role_id:
                    member_details = get_person_details(member_role, member_role_id)
                    if member_details:
                        enriched_members.append(member_details)
                    else:
                        enriched_members.append(member)
                else:
                    enriched_members.append(member)

        result = {
            "id": alloc.id,
            "project_id": alloc.project_id,
            "project_name": alloc.project.name if alloc.project else None,
            "project_logo": alloc.project.project_logo if alloc.project else None,
            "members": enriched_members,
            "start_date": alloc.start_date.isoformat(),
            "end_date": alloc.end_date.isoformat() if alloc.end_date else None,
            "remark": alloc.remark,
            "allocated_by_role_id": alloc.allocated_by_role_id,
            "allocated_by_role": alloc.allocated_by_role,
            "allocated_by_person": allocated_by_person,
            "created_at": alloc.created_at
        }
        return jsonify({"allocation": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def get_allocation_by_id(allocation_id):
    try:
        alloc = ProjectAllocation.query.get(allocation_id)
        if not alloc:
            return jsonify({"message": "Allocation not found", "status": 0}), 404
        
        allocated_by_person = get_person_details(alloc.allocated_by_role, alloc.allocated_by_role_id)
        # Enrich members
        enriched_members = []
        if alloc.members:
            for member in alloc.members:
                member_role = member.get("role")
                member_role_id = member.get("role_id")
                if member_role and member_role_id:
                    member_details = get_person_details(member_role, member_role_id)
                    if member_details:
                        enriched_members.append(member_details)
                    else:
                        enriched_members.append(member)
                else:
                    enriched_members.append(member)
        
        result = {
            "id": alloc.id,
            "project_id": alloc.project_id,
            "project_name": alloc.project.name if alloc.project else None,
            "project_logo": alloc.project.project_logo if alloc.project else None,
            "members": enriched_members,
            "start_date": alloc.start_date.isoformat(),
            "end_date": alloc.end_date.isoformat() if alloc.end_date else None,
            "remark": alloc.remark,
            "allocated_by_role_id": alloc.allocated_by_role_id,
            "allocated_by_role": alloc.allocated_by_role,
            "allocated_by_person": allocated_by_person,
            "created_at": alloc.created_at
        }
        return jsonify({"allocation": result, "status": 1}), 200
    except Exception as e:
        return jsonify({"success": 0, "error": str(e)}), 500

def update_allocation(allocation_id):
    try:
        alloc = ProjectAllocation.query.get(allocation_id)
        if not alloc:
            return jsonify({"message": "Allocation not found", "status": 0}), 404

        data = request.get_json()
        
        if "project_id" in data:
            alloc.project_id = data["project_id"]
        if "members" in data:
            if not isinstance(data["members"], list):
                return jsonify({"msg": "Members must be a JSON array", "status": 0}), 400
            alloc.members = data["members"]
        if "start_date" in data:
            alloc.start_date = datetime.datetime.strptime(data["start_date"], '%Y-%m-%d').date()
        if "end_date" in data:
            alloc.end_date = datetime.datetime.strptime(data["end_date"], '%Y-%m-%d').date() if data["end_date"] else None
        if "remark" in data:
            alloc.remark = data["remark"]
            
        db.session.commit()
        return jsonify({"message": "Allocation updated successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def update_allocation_members(allocation_id):
    try:
        alloc = ProjectAllocation.query.get(allocation_id)
        if not alloc:
            return jsonify({"message": "Allocation not found", "status": 0}), 404

        data = request.get_json()
        members = data.get("members")
        
        if members is not None:
            if not isinstance(members, list):
                return jsonify({"msg": "Members must be a JSON array", "status": 0}), 400
            alloc.members = members
            db.session.commit()
            return jsonify({"message": "Members updated successfully", "status": 1}), 200
        
        return jsonify({"msg": "No members data provided", "status": 0}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def delete_allocation(allocation_id):
    try:
        alloc = ProjectAllocation.query.get(allocation_id)
        if not alloc:
            return jsonify({"message": "Allocation not found", "status": 0}), 404
            
        db.session.delete(alloc)
        db.session.commit()
        return jsonify({"message": "Allocation deleted successfully", "status": 1}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500
