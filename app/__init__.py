from flask import Flask
from app.models import db  # Your SQLAlchemy instance
from flask_migrate import Migrate  # Import Flask-Migrate
from app.config.config import Config  # Import your config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load configuration from config file

    db.init_app(app)  # Initialize SQLAlchemy with the app

    # Initialize Flask-Migrate
    migrate = Migrate(app, db)  # Add this line

    # Register Blueprints (add other blueprints as necessary)
    from app.api.resources import resources_bp
    app.register_blueprint(resources_bp)

    return app
