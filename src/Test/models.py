# src/models.py

from src.Test import db
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


class Resource(db.Model):
    __tablename__ = 'resources'
    ResourceID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Rate = Column(Numeric(10, 2), nullable=False)  # Using Numeric for precise decimals
    Skills = Column(JSONB, nullable=False)  # Storing skills as JSONB
    PastJobTitles = Column(JSONB, nullable=False)  # Storing past job titles as JSONB
    Domain = Column(ARRAY(String), nullable=False)  # Storing domains as an array of strings
    AvailableDate = Column(Date, nullable=True)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'), nullable=False)
    TeamID = Column(Integer, ForeignKey('teams.TeamID'), nullable=True)  # Nullable if not assigned to a team
    
    # Relationships
    organization = relationship('Organization', back_populates='resources')
    team = relationship('Team', back_populates='resources')


class Project(db.Model):
    __tablename__ = 'projects'
    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String(100), nullable=False, unique=True)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'), nullable=False)
    RequiredResources = Column(JSONB, nullable=False)  # Storing required resources as JSONB
    NumberOfDays = Column(Integer, nullable=False)
    ProjectStartDate = Column(Date, nullable=False)
    Technology = Column(ARRAY(String), nullable=False)  # Storing technologies as an array of strings
    Domain = Column(ARRAY(String), nullable=False)  # Storing domains as an array of strings
    
    # Relationships
    organization = relationship('Organization', back_populates='projects')
    team = relationship('Team', back_populates='project', uselist=False, cascade='all, delete-orphan')


class Team(db.Model):
    __tablename__ = 'teams'
    TeamID = Column(Integer, primary_key=True)
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID'), nullable=False, unique=True)
    TotalResources = Column(Integer, nullable=False)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'), nullable=False)
    
    # Relationships
    project = relationship('Project', back_populates='team')
    organization = relationship('Organization', back_populates='teams')
    resources = relationship('Resource', back_populates='team')