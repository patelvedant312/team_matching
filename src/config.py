# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This loads environment variables from .env file into the environment

class Config:
    """Configuration class to encapsulate all configuration variables."""
    DATABASE_URL = os.getenv('DATABASE_URL')  # Default to SQLite if not set
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL  # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal handling