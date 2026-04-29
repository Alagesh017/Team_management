from src.routes.auth_route import auth_bp


def init_routes(app):
    app.register_blueprint(auth_bp)
