from app.models import db
from sqlalchemy import Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON

class Resource(db.Model):
    __tablename__ = 'resources'
    
    ResourceID = db.Column(Integer, primary_key=True)
    Name = db.Column(String(100), nullable=False)
    Rate = db.Column(Numeric(10, 2))
    PastJobTitles = db.Column(JSON)  # JSON array for past job titles
    CurrentJobTitle = db.Column(String(100))
    PastWorkDomains = db.Column(JSON)  # JSON array for past work domains
    YearsOfExperience = db.Column(Integer)
    AvailableDate = db.Column(Date)
    OrgID = db.Column(Integer, ForeignKey('organizations.OrgID'))
    
    organization = relationship('Organization', back_populates='resources')
    skills = relationship(
        'Skill',
        secondary='resource_skill_association',  # Replace with correct association table name
        back_populates='resources'
    )

    def serialize(self):
        return {
            'ResourceID': self.ResourceID,
            'Name': self.Name,
            'Rate': str(self.Rate),
            'PastJobTitles': self.PastJobTitles,
            'CurrentJobTitle': self.CurrentJobTitle,
            'PastWorkDomains': self.PastWorkDomains,
            'YearsOfExperience': self.YearsOfExperience,
            'AvailableDate': self.AvailableDate.isoformat() if self.AvailableDate else None,
            'OrgID': self.OrgID
        }
