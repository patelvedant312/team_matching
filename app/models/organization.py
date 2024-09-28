from app.models import db  # Import db instance from models
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    OrgID = db.Column(Integer, primary_key=True)
    OrgName = db.Column(String(100), nullable=False, unique=True)

    # Relationships
    resources = db.relationship('Resource', back_populates='organization', cascade='all, delete-orphan')
    projects = db.relationship('Project', back_populates='organization', cascade='all, delete-orphan')
    teams = db.relationship('Team', back_populates='organization', cascade='all, delete-orphan')

    def serialize(self):
        return {
            'OrgID': self.OrgID,
            'OrgName': self.OrgName,
        }
