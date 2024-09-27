from app.models import db
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship

class Organization(db.Model):
    __tablename__ = 'organizations'
    
    OrgID = db.Column(Integer, primary_key=True)
    OrgName = db.Column(String(100), nullable=False)
    
    # Relationships
    resources = relationship('Resource', back_populates='organization')
    employees = relationship('Employee', back_populates='organization')  # If you also have an Employee model
    
    def serialize(self):
        return {
            'OrgID': self.OrgID,
            'OrgName': self.OrgName,
        }
