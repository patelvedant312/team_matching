
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Organization(db.Model):
    __tablename__ = 'organizations'
    OrgID = Column(Integer, primary_key=True)
    OrgName = Column(String(100), nullable=False)
    
    resources = relationship('Resource', back_populates='organization')
    teams = relationship('Team', back_populates='organization')  # This should exist
    projects = relationship('Project', back_populates='organization')  # Relationship to Project


class Resource(db.Model):
    __tablename__ = 'resources'
    ResourceID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Rate = Column(Numeric(10, 2))
    Skills = Column(db.JSON)  # Example: ['Skill A : expert', 'Skill B : intermediate']
    PastJobTitles = Column(db.JSON)  # Example: ['Title A : 3', 'Title B : 4']
    Domain = Column(db.JSON)  # Example: ['Domain A', 'Domain B']
    AvailableDate = Column(Date)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))

    organization = relationship('Organization', back_populates='resources')

class Project(db.Model):
    __tablename__ = 'projects'
    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String(200), nullable=False)
    NumberOfDays = Column(Integer)
    ProjectStartDate = Column(Date)
    Technology = Column(String(200))
    Domain = Column(String(100))
    RequiredResources = Column(db.JSON)  # Example: [{'Role': 'Frontend Developer', 'Skills': ['Skill A: expert', 'Skill B: intermediate'], 'Quantity': 2}]
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))

    organization = relationship('Organization', back_populates='projects')
    team = relationship('Team', back_populates='project', uselist=False)

class Team(db.Model):
    __tablename__ = 'teams'
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID'), primary_key=True)
    ResourceIDs = Column(db.JSON)  # Array of ResourceIDs
    TotalResources = Column(Integer)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))
    
    project = relationship('Project', back_populates='team')
    organization = relationship('Organization', back_populates='teams')

