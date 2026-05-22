from flask import jsonify
from src import db
from src.models.project_allocation_model import ProjectAllocation
from src.models.task_status_model import TaskStatus
from src.models.task_model import Task
from src.models.admin_model import Admin
from src.models.worker_model import Worker
from src.utils.role_utils import get_person_details

def get_project_task_data(project_id):
    try:
        print("=== Starting get_project_task_data ===")
        print("Project ID:", project_id)
        
        allocation = ProjectAllocation.query.filter_by(project_id=project_id).first()
        print("Allocation found:", allocation)
        print("Allocation members:", allocation.members if allocation else None)
        
        # Fetch all admins and workers first for better performance (backward compatibility)
        all_admins = Admin.query.all()
        all_workers = Worker.query.all()
        admin_map = {admin.id: admin for admin in all_admins}
        worker_map = {worker.id: worker for worker in all_workers}
        print(f"Fetched {len(all_admins)} admins and {len(all_workers)} workers")
        
        allocated_members = []
        
        if allocation and allocation.members:
            print(f"\nAllocation has {len(allocation.members)} members to process")
            for idx, member in enumerate(allocation.members):
                print(f"\nProcessing member {idx}:", member)
                
                # Handle both formats: old {user_id} and new {role_id, role}
                role_id = member.get("role_id")
                role = member.get("role")
                user_id = member.get("user_id")
                
                if role_id and role:
                    # New format: use get_person_details
                    person_details = get_person_details(role, role_id)
                    if person_details:
                        print(f"Adding person (new format): {person_details['first_name']} {person_details['last_name']}")
                        allocated_members.append({
                            "user_id": role_id,
                            "type": "admin" if role in ["superadmin", "admin", "scrum"] else "worker",
                            "role": role,
                            "parent_id": member.get("parent_id"),
                            "first_name": person_details["first_name"],
                            "last_name": person_details["last_name"],
                            "email": person_details.get("email"),
                            "avatar_url": person_details.get("avatar_url"),
                            "is_tl": role == "team_leader" or role == "Team Leader",
                            "is_worker": role in ["worker", "team_leader", "Worker", "Team Leader"],
                            "job_title": ""
                        })
                elif user_id:
                    # Old format: backward compatibility
                    print("User ID (old format):", user_id)
                    if user_id in worker_map:
                        worker = worker_map[user_id]
                        print(f"Adding worker (old format): {worker.first_name} {worker.last_name} (ID: {user_id})")
                        allocated_members.append({
                            "user_id": worker.id,
                            "type": "worker",
                            "role": member.get("role"),
                            "parent_id": member.get("parent_id"),
                            "first_name": worker.first_name,
                            "last_name": worker.last_name,
                            "email": worker.email,
                            "avatar_url": worker.avatar_url,
                            "is_tl": worker.is_tl,
                            "is_worker": worker.is_worker,
                            "job_title": worker.job_title
                        })
                    elif user_id in admin_map:
                        admin = admin_map[user_id]
                        print(f"Adding admin (old format): {admin.first_name} {admin.last_name} (ID: {user_id})")
                        allocated_members.append({
                            "user_id": admin.id,
                            "type": "admin",
                            "role": member.get("role"),
                            "parent_id": member.get("parent_id"),
                            "first_name": admin.first_name,
                            "last_name": admin.last_name,
                            "email": admin.email,
                            "avatar_url": admin.avatar_url,
                            "is_tl": False,
                            "is_worker": False,
                            "job_title": ""
                        })
                    else:
                        print(f"WARNING: User with ID {user_id} not found!")
                        print(f"Available worker IDs: {list(worker_map.keys())}")
                        print(f"Available admin IDs: {list(admin_map.keys())}")
        
        print("\n=== Final allocated_members ===")
        print("Count:", len(allocated_members))
        print("Allocated members:", allocated_members)
        
        statuses = TaskStatus.query.order_by(TaskStatus.sort_order).all()
        
        tasks = Task.query.filter_by(project_id=project_id).all()
        
        tasks_with_workers = []
        for task in tasks:
            # Get task members (handle both old worker_ids and new members)
            task_members = []
            if hasattr(task, 'members') and task.members:
                task_members = task.members
            elif hasattr(task, 'worker_ids') and task.worker_ids:
                task_members = task.worker_ids
            
            task_data = {
                "task_id": task.id,
                "project_id": task.project_id,
                "allocation_id": task.allocation_id,
                "status_id": task.status_id,
                "title": task.title,
                "description": task.description,
                "goal": task.goal,
                "priority": task.priority,
                "start_date": task.start_date.isoformat() if task.start_date else None,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "worker_ids": task_members or [],
                "assigned_workers": [],
                "assigned_by": task.assigned_by if hasattr(task, 'assigned_by') else None,
                "estimated_hours": float(task.estimated_hours) if task.estimated_hours else None,
                "actual_hours": float(task.actual_hours) if task.actual_hours else None,
                "remark": task.remark,
                "created_at": task.created_at.isoformat() if task.created_at else None
            }
            
            if task_members:
                for member_item in task_members:
                    worker_data = None
                    
                    # Handle both formats: new {role_id, role} and old {user_id} or just user_id
                    if isinstance(member_item, dict):
                        role_id = member_item.get("role_id")
                        role = member_item.get("role")
                        user_id = member_item.get("user_id")
                        user_type = member_item.get("type")
                        
                        if role_id and role:
                            # New format
                            person_details = get_person_details(role, role_id)
                            if person_details:
                                worker_data = {
                                    "user_id": role_id,
                                    "type": "admin" if role in ["superadmin", "admin", "scrum"] else "worker",
                                    "first_name": person_details["first_name"],
                                    "last_name": person_details["last_name"],
                                    "email": person_details.get("email"),
                                    "avatar_url": person_details.get("avatar_url")
                                }
                        elif user_id:
                            # Old format (dict with user_id)
                            if user_type == "admin" or (user_type is None and user_id in admin_map):
                                admin = admin_map.get(user_id)
                                if admin:
                                    worker_data = {
                                        "user_id": admin.id,
                                        "type": "admin",
                                        "first_name": admin.first_name,
                                        "last_name": admin.last_name,
                                        "email": admin.email,
                                        "avatar_url": admin.avatar_url
                                    }
                            elif user_type == "worker" or (user_type is None and user_id in worker_map):
                                worker = worker_map.get(user_id)
                                if worker:
                                    worker_data = {
                                        "user_id": worker.id,
                                        "type": "worker",
                                        "first_name": worker.first_name,
                                        "last_name": worker.last_name,
                                        "email": worker.email,
                                        "avatar_url": worker.avatar_url
                                    }
                    else:
                        # Old format (just user_id number)
                        user_id = member_item
                        if user_id in admin_map:
                            admin = admin_map.get(user_id)
                            if admin:
                                worker_data = {
                                    "user_id": admin.id,
                                    "type": "admin",
                                    "first_name": admin.first_name,
                                    "last_name": admin.last_name,
                                    "email": admin.email,
                                    "avatar_url": admin.avatar_url
                                }
                        elif user_id in worker_map:
                            worker = worker_map.get(user_id)
                            if worker:
                                worker_data = {
                                    "user_id": worker.id,
                                    "type": "worker",
                                    "first_name": worker.first_name,
                                    "last_name": worker.last_name,
                                    "email": worker.email,
                                    "avatar_url": worker.avatar_url
                                }
                    
                    if worker_data:
                        task_data["assigned_workers"].append(worker_data)
            
            tasks_with_workers.append(task_data)
        
        statuses_with_tasks = []
        for status in statuses:
            status_tasks = [task for task in tasks_with_workers if task["status_id"] == status.id]
            statuses_with_tasks.append({
                "status_id": status.id,
                "name": status.name,
                "color": status.color,
                "sort_order": status.sort_order,
                "remark": status.remark,
                "tasks": status_tasks
            })
        
        allocation_dict = None
        if allocation:
            allocation_dict = {
                "allocation_id": allocation.id,
                "project_id": allocation.project_id,
                "members": allocation.members,
                "remark": allocation.remark,
                "created_at": allocation.created_at.isoformat() if allocation.created_at else None,
                "updated_at": allocation.updated_at.isoformat() if allocation.updated_at else None
            }
        
        all_admins_list = []
        for admin in all_admins:
            all_admins_list.append({
                "user_id": admin.id,
                "type": "admin",
                "first_name": admin.first_name,
                "last_name": admin.last_name,
                "email": admin.email,
                "avatar_url": admin.avatar_url,
                "is_superadmin": admin.is_superadmin,
                "is_admin": admin.is_admin,
                "is_scrum": admin.is_scrum
            })
        
        return jsonify({
            "allocation": allocation_dict,
            "allocated_members": allocated_members,
            "all_admins": all_admins_list,
            "statuses": statuses_with_tasks,
            "status": 1
        }), 200
    except Exception as e:
        import traceback
        print(f"Error in get_project_task_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"success": 0, "error": str(e)}), 500
