from app.models import db
from sqlalchemy import Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

class Resource(db.Model):
    __tablename__ = 'resources'
    
    ResourceID = db.Column(Integer, primary_key=True)
    Name = db.Column(String(100), nullable=False)
    Rate = db.Column(Numeric(10, 2), nullable=False)  # Using Numeric for precise decimals
    Skills = db.Column(JSONB, nullable=False)  # Storing skills as JSONB
    PastJobTitles = db.Column(JSONB, nullable=False)  # Storing past job titles as JSONB
    Domain = db.Column(ARRAY(String), nullable=False)  # Storing domains as an array of strings
    AvailableDate = db.Column(Date, nullable=True)
    OrgID = db.Column(Integer, ForeignKey('organizations.OrgID'), nullable=False)
    TeamID = db.Column(Integer, ForeignKey('teams.TeamID'), nullable=True)  # Nullable if not assigned to a team
    
    # Relationships
    organization = relationship('Organization', back_populates='resources')
    team = relationship('Team', back_populates='resources')

    # Serialization method to return Resource data as JSON-friendly dict
    def serialize(self):
        return {
            'ResourceID': self.ResourceID,
            'Name': self.Name,
            'Rate': str(self.Rate),  # Convert Numeric to string for JSON serialization
            'Skills': self.Skills,
            'PastJobTitles': self.PastJobTitles,
            'Domain': self.Domain,
            'AvailableDate': self.AvailableDate.isoformat() if self.AvailableDate else None,
            'OrgID': self.OrgID,
            'TeamID': self.TeamID,
            # Optionally, you can serialize related objects like 'organization' or 'team'
            # 'organization': self.organization.serialize() if self.organization else None,
            # 'team': self.team.serialize() if self.team else None
        }
