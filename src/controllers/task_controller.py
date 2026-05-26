from flask import jsonify, request
import datetime
from src import db
from src.models.task_model import Task
from src.utils.date_utils import parse_date
from src.utils.role_utils import get_person_details

def create_task(decoded_payload=None):
    try:
        data = request.get_json()
        print(data)
        
        project_id = data.get("project_id")
        allocation_id = data.get("allocation_id")
        status_id = data.get("status_id")
        title = data.get("title")
        description = data.get("description")
        goal = data.get("goal")
        priority = data.get("priority", "medium")
        start_date_str = data.get("start_date")
        due_date_str = data.get("due_date")
        # Handle both members (new) and worker_ids (old)
        members = data.get("members", [])
        worker_ids = data.get("worker_ids", [])
        if worker_ids and not members:
            members = worker_ids
        estimated_hours = data.get("estimated_hours")
        actual_hours = data.get("actual_hours")
        remark = data.get("remark")
        
        # Get assigned_by from decoded_payload (new format) or data (old format)
        assigned_by_role_id = None
        assigned_by_role = None
        if decoded_payload:
            assigned_by_role_id = decoded_payload.get("role_id")
            assigned_by_role = decoded_payload.get("role")
        
        # Fallback to old format if needed
        assigned_by_user_id = data.get("assigned_by")
        if not assigned_by_role_id and assigned_by_user_id:
            # Old format: try to determine role from user (backward compatibility)
            from src.models.user_model import User
            user = User.query.get(assigned_by_user_id)
            if user:
                assigned_by_role_id = user.role_id
                assigned_by_role = user.role
        
        if not all([project_id, status_id, title, assigned_by_role_id, assigned_by_role]):
            return jsonify({"msg": "Project, Status, Title, and Assigner are required", "status": 0}), 400

        start_date = parse_date(start_date_str) if start_date_str else None
        due_date = parse_date(due_date_str) if due_date_str else None
        
        created_task_ids = []
        
        # If there are members, create a separate task for each member
        if members and len(members) > 0:
            for member in members:
                # Wrap single member in a list for the task
                task_members = [member]
                
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
                    members=task_members,
                    worker_ids=[member] if worker_ids else None, # Backward compatibility
                    assigned_by_role_id=assigned_by_role_id,
                    assigned_by_role=assigned_by_role,
                    assigned_by=assigned_by_user_id if assigned_by_user_id else None, # Backward compatibility
                    estimated_hours=estimated_hours,
                    actual_hours=actual_hours,
                    remark=remark
                )
                db.session.add(new_task)
                db.session.flush()
                created_task_ids.append(new_task.id)
        else:
            # If no members, create single task
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
                members=members,
                worker_ids=worker_ids if worker_ids else None, # Backward compatibility
                assigned_by_role_id=assigned_by_role_id,
                assigned_by_role=assigned_by_role,
                assigned_by=assigned_by_user_id if assigned_by_user_id else None, # Backward compatibility
                estimated_hours=estimated_hours,
                actual_hours=actual_hours,
                remark=remark
            )
            db.session.add(new_task)
            db.session.flush()
            created_task_ids.append(new_task.id)
        
        db.session.commit()
        
        return jsonify({"msg": "Task(s) created successfully", "status": 1, "task_ids": created_task_ids}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": 0, "error": str(e)}), 500

def get_tasks_by_project(project_id):
    try:
        tasks = Task.query.filter_by(project_id=project_id).all()
        
        result = []
        for task in tasks:
            # Enrich members
            enriched_members = []
            # Use task.worker_ids if available, else task.members (backward compatibility)
            task_members = task.worker_ids if task.worker_ids else task.members
            if task_members:
                for member in task_members:
                    member_role = member.get("role")
                    member_role_id = member.get("role_id")
                    user_id = member.get("user_id")
                    if member_role and member_role_id:
                        member_details = get_person_details(member_role, member_role_id)
                        if member_details:
                            enriched_members.append(member_details)
                        else:
                            enriched_members.append(member)
                    else:
                        enriched_members.append(member)
            
            assigned_by_person = get_person_details(task.assigned_by_role, task.assigned_by_role_id)
            task_data = {
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
                "assigned_by_role_id": task.assigned_by_role_id,
                "assigned_by_role": task.assigned_by_role,
                "assigned_by_person": assigned_by_person,
                "assigned_by": task.assigned_by, # Backward compatibility
                "worker_ids": task.worker_ids, # Backward compatibility
                "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
                "actual_hours": float(task.actual_hours) if task.actual_hours else None,
                "remark": task.remark,
                "created_at": task.created_at,
                "members": enriched_members
            }
            
            result.append(task_data)
        return jsonify({"tasks": result, "status": 1}), 200
    except Exception as e:
        import traceback
        print(f"Error in get_tasks_by_project: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": 0, "error": str(e)}), 500

def get_all_tasks():
    try:
        tasks = Task.query.all()
        result = []
        for task in tasks:
            # Enrich members
            enriched_members = []
            # Use task.worker_ids if available, else task.members (backward compatibility)
            task_members = task.worker_ids if task.worker_ids else task.members
            if task_members:
                for member in task_members:
                    member_role = member.get("role")
                    member_role_id = member.get("role_id")
                    user_id = member.get("user_id")
                    if member_role and member_role_id:
                        member_details = get_person_details(member_role, member_role_id)
                        if member_details:
                            enriched_members.append(member_details)
                        else:
                            enriched_members.append(member)
                    else:
                        enriched_members.append(member)
            
            assigned_by_person = get_person_details(task.assigned_by_role, task.assigned_by_role_id)
            task_data = {
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
                "assigned_by_role_id": task.assigned_by_role_id,
                "assigned_by_role": task.assigned_by_role,
                "assigned_by_person": assigned_by_person,
                "assigned_by": task.assigned_by, # Backward compatibility
                "worker_ids": task.worker_ids, # Backward compatibility
                "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
                "actual_hours": float(task.actual_hours) if task.actual_hours else None,
                "remark": task.remark,
                "created_at": task.created_at,
                "members": enriched_members
            }
            result.append(task_data)
        return jsonify({"tasks": result, "status": 1}), 200
    except Exception as e:
        import traceback
        print(f"Error in get_all_tasks: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": 0, "error": str(e)}), 500

def get_task_by_id(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({"message": "Task not found", "status": 0}), 404
        
        # Enrich members
        enriched_members = []
        # Use task.worker_ids if available, else task.members (backward compatibility)
        task_members = task.worker_ids if task.worker_ids else task.members
        if task_members:
            for member in task_members:
                member_role = member.get("role")
                member_role_id = member.get("role_id")
                user_id = member.get("user_id")
                if member_role and member_role_id:
                    member_details = get_person_details(member_role, member_role_id)
                    if member_details:
                        enriched_members.append(member_details)
                    else:
                        enriched_members.append(member)
                else:
                    enriched_members.append(member)
        
        assigned_by_person = get_person_details(task.assigned_by_role, task.assigned_by_role_id)
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
            "assigned_by_role_id": task.assigned_by_role_id,
            "assigned_by_role": task.assigned_by_role,
            "assigned_by_person": assigned_by_person,
            "assigned_by": task.assigned_by, # Backward compatibility
            "worker_ids": task.worker_ids, # Backward compatibility
            "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
            "actual_hours": float(task.actual_hours) if task.actual_hours else None,
            "remark": task.remark,
            "created_at": task.created_at,
            "members": enriched_members
        }
        return jsonify({"task": result, "status": 1}), 200
    except Exception as e:
        import traceback
        print(f"Error in get_task_by_id: {str(e)}")
        print(traceback.format_exc())
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
        if "members" in data:
            task.members = data["members"]
        if "worker_ids" in data:
            task.worker_ids = data["worker_ids"]
            if not task.members:
                task.members = data["worker_ids"]
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
