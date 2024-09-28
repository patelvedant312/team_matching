from flask import Flask
from app.models import db  # Import db from models
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')  # Load configuration

    db.init_app(app)  # Initialize SQLAlchemy with the Flask app
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Register Blueprints
    from app.api.resources import resources_bp
    from app.api.projects import projects_bp
    from app.api.teams import teams_bp
    from app.api.organizations import organizations_bp

    app.register_blueprint(resources_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(organizations_bp)

    return app
