from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # This is your database instance

from app.models.organization import Organization
from app.models.resource import Resource