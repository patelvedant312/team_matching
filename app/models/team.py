from app import db
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Team(db.Model):
    __tablename__ = 'teams'
    
    TeamID = db.Column(Integer, primary_key=True)
    ProjectID = db.Column(Integer, ForeignKey('projects.ProjectID'), nullable=False, unique=True)
    TotalResources = db.Column(Integer, nullable=False)
    OrgID = db.Column(String, ForeignKey('organizations.OrgID'), nullable=False)
    
    # Relationships
    project = relationship('Project', back_populates='team')
    organization = relationship('Organization', back_populates='teams')
    resources = relationship('Resource', back_populates='team')

    def serialize(self):
        return {
            'TeamID': self.TeamID,
            'ProjectID': self.ProjectID,
            'TotalResources': self.TotalResources,
            'OrgID': self.OrgID,
        }
