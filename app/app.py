from flask import Flask
from app.api.organizations import organizations_bp  # Import your blueprint

def create_app():
    app = Flask(__name__)

    # Register the blueprint
    app.register_blueprint(organizations_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(teams_bp)


    return app
