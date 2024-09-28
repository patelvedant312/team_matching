from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

class Organization(db.Model):
    __tablename__ = 'organizations'
    OrgID = Column(Integer, primary_key=True)
    OrgName = Column(String(100), nullable=False, unique=True)

    # Relationships
    resources = relationship('Resource', back_populates='organization', cascade='all, delete-orphan')
    projects = relationship('Project', back_populates='organization', cascade='all, delete-orphan')
    teams = relationship('Team', back_populates='organization', cascade='all, delete-orphan')
    
    def serialize(self):
        return {
            'OrgID': self.OrgID,
            'OrgName': self.OrgName,
        }
