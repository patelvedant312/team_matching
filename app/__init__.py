from flask import Flask
from app.models import db
from flask_migrate import Migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.config.Config')  # Load configuration

    db.init_app(app)  # Initialize the database
    migrate = Migrate(app, db)  # Initialize migrations

    # Register blueprints with the correct prefixes
    from app.api.resources import resources_bp
    from app.api.projects import projects_bp
    from app.api.teams import teams_bp
    from app.api.organizations import organizations_bp
    

    app.register_blueprint(organizations_bp, url_prefix='/organizations') 
    app.register_blueprint(projects_bp, url_prefix='/projects')
    app.register_blueprint(resources_bp, url_prefix='/resources')
    app.register_blueprint(teams_bp, url_prefix='/teams') # This must match

    return app