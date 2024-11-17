from app import db
from sqlalchemy import Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

class Project(db.Model):
    __tablename__ = 'projects'
    
    ProjectID = db.Column(Integer, primary_key=True)
    ProjectName = db.Column(String(100), nullable=False, unique=True)
    OrgID = db.Column(String, ForeignKey('organizations.OrgID'), nullable=False)
    RequiredResources = db.Column(JSONB, nullable=False)  # Storing required resources as JSONB
    NumberOfDays = db.Column(Integer, nullable=False)
    ProjectStartDate = db.Column(Date, nullable=False)
    Technology = db.Column(ARRAY(String), nullable=False)  # Storing technologies as an array of strings
    Domain = db.Column(ARRAY(String), nullable=False)  # Storing domains as an array of strings
    
    # Relationships
    organization = relationship('Organization', back_populates='projects')
    team = relationship('Team', back_populates='project', uselist=False, cascade='all, delete-orphan')
    
    # Serialization method to return Project data as JSON-friendly dict
    def serialize(self):
        return {
            'ProjectID': self.ProjectID,
            'ProjectName': self.ProjectName,
            'OrgID': self.OrgID,
            'RequiredResources': self.RequiredResources,
            'NumberOfDays': self.NumberOfDays,
            'ProjectStartDate': self.ProjectStartDate.isoformat() if self.ProjectStartDate else None,
            'Technology': self.Technology,
            'Domain': self.Domain,
            # You can serialize related objects, like 'organization' or 'team', if needed:
            # 'organization': self.organization.serialize() if self.organization else None,
            # 'team': self.team.serialize() if self.team else None
        }
