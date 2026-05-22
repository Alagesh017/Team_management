from src.models.admin_model import Admin
from src.models.worker_model import Worker

def get_person_by_role(role, role_id):
    """
    Get the Admin or Worker object based on role and role_id.
    
    Args:
        role (str): One of: superadmin, admin, scrum, worker, team_leader
        role_id (int): The ID in the respective table (admins or workers)
    
    Returns:
        Admin or Worker or None: The person object if found, None otherwise
    """
    if role in ["superadmin", "admin", "scrum"]:
        return Admin.query.get(role_id)
    elif role in ["worker", "team_leader"]:
        return Worker.query.get(role_id)
    return None

def get_person_details(role, role_id):
    """
    Get person details as a dictionary.
    
    Args:
        role (str): Role name
        role_id (int): Role ID
        
    Returns:
        dict: Person details with first_name, last_name, email, avatar_url
    """
    person = get_person_by_role(role, role_id)
    if person:
        return {
            "role_id": role_id,
            "role": role,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "email": getattr(person, "email", None),
            "avatar_url": person.avatar_url
        }
    return None
