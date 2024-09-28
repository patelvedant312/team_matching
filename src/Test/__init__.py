# src/__init__.py

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()  # Centralized SQLAlchemy instance

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')  # Ensure your config is set correctly
    
    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate = Migrate(app, db)  # Initialize Flask-Migrate
    
    # Import models to ensure they are registered with SQLAlchemy
    from src.Test.models import Organization, Resource, Project, Team
    
    # Register blueprints or routes here if any
    try:
        from .routes import main
        app.register_blueprint(main)
    except ImportError:
        # If routes are not defined yet, you can skip or handle accordingly
        pass
    
    return app