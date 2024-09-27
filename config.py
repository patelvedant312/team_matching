# src/config.py

import os
from dotenv import load_dotenv

load_dotenv()  # This loads environment variables from .env file into the environment

class Config:
    """Configuration class to encapsulate all configuration variables."""
    DATABASE_URL = os.getenv('postgresql://team_matching_owner:Zf3AKJrwqnc1@ep-purple-unit-a54far0t.us-east-2.aws.neon.tech/team_matching?sslmode=require')
    SECRET_KEY = os.getenv('4bad2517464bafe5ab39973ece1d50381a9da2ee81ff9b62dd0d57a78394e07b')
    SQLALCHEMY_DATABASE_URI = DATABASE_URL  # SQLAlchemy configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable signal handling
