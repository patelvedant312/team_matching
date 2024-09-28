from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models here
from app.models.organization import Organization
from app.models.team import Team
from app.models.resource import Resource  
from app.models.project import Project
