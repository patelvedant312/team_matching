from flask import Blueprint
from .resources import resources_bp
from .projects import projects_bp
from .teams import teams_bp
from .organizations import organizations_bp

api_bp = Blueprint('api', __name__)

# Register the blueprints
api_bp.register_blueprint(resources_bp)
api_bp.register_blueprint(projects_bp)
api_bp.register_blueprint(teams_bp)
api_bp.register_blueprint(organizations_bp)