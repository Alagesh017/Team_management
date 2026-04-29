from src.routes.auth_route import auth_bp
from src.routes.admin_route import admin_bp
from src.routes.worker_route import worker_bp

def init_routes(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(worker_bp)

