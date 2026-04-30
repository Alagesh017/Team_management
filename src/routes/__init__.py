from src.routes.auth_route import auth_bp
from src.routes.admin_route import admin_bp
from src.routes.worker_route import worker_bp
from src.routes.client_route import client_bp
from src.routes.task_status_route import task_status_bp
from src.routes.project_route import project_bp
from src.routes.project_allocation_route import project_allocation_bp
from src.routes.task_route import task_bp
from src.routes.sub_task_route import sub_task_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(client_bp)
    app.register_blueprint(task_status_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(project_allocation_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(sub_task_bp)

