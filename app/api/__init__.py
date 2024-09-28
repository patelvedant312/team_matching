# /app/api/__init__.py
from flask import Blueprint
from .resources import resources_bp


api_bp = Blueprint('api', __name__)

# Register blueprints for each resource
api_bp.register_blueprint(resources_bp)

