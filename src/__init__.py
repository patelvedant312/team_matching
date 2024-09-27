# src/__init__.py

from flask import Flask
from flask_migrate import Migrate
from src.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object('src.config.Config')  # Ensure your config is set correctly

    db.init_app(app)  # Initialize SQLAlchemy with the app
    migrate = Migrate(app, db)  # Initialize Flask-Migrate

    # Register blueprints or routes here if any
    from .routes import main
    app.register_blueprint(main)

    return app
