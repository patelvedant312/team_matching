# models/__init__.py

from app import db


# Import models here to register them with SQLAlchemy
from app.models.organization import Organization
from app.models.team import Team
from app.models.resource import Resource
from app.models.project import Project
