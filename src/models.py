from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Numeric, Date, ForeignKey, Table
from sqlalchemy.orm import relationship

db = SQLAlchemy()

# Association table between Employee and Skill with additional 'Level' field
employee_skill_association = Table(
    'employee_skill_association',
    db.metadata,
    Column('EmployeeID', Integer, ForeignKey('employees.EmployeeID'), primary_key=True),
    Column('SkillID', Integer, ForeignKey('skills.SkillID'), primary_key=True),
    Column('Level', String(20))  # 'beginner', 'intermediate', 'expert'
)

class Organization(db.Model):
    __tablename__ = 'organizations'
    OrgID = Column(Integer, primary_key=True)
    OrgName = Column(String(100), nullable=False)
    
    employees = relationship('Employee', back_populates='organization')
    teams = relationship('Team', back_populates='organization')  # Relationship to Team
    projects = relationship('Project', back_populates='organization')  # New relationship to Project

class Employee(db.Model):
    __tablename__ = 'employees'
    EmployeeID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False)
    Rate = Column(Numeric(10, 2))
    PastJobTitles = Column(db.JSON)  # Changed to JSON array
    CurrentJobTitle = Column(String(100))
    PastWorkDomains = Column(db.JSON)  # Changed to JSON array
    YearsOfExperience = Column(Integer)
    AvailableDate = Column(Date)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))
    
    organization = relationship('Organization', back_populates='employees')
    skills = relationship(
        'Skill',
        secondary=employee_skill_association,
        back_populates='employees'
    )

class Skill(db.Model):
    __tablename__ = 'skills'
    SkillID = Column(Integer, primary_key=True)
    SkillName = Column(String(100), nullable=False, unique=True)
    
    employees = relationship(
        'Employee',
        secondary=employee_skill_association,
        back_populates='skills'
    )

class Project(db.Model):
    __tablename__ = 'projects'
    ProjectID = Column(Integer, primary_key=True)
    ProjectName = Column(String(200), nullable=False)
    NumberOfDays = Column(Integer)
    ProjectStartDate = Column(Date)
    Technology = Column(String(200))
    Domain = Column(String(100))
    RequiredResources = Column(db.JSON)  # Renamed and restructured
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))  # Added OrgID
    
    organization = relationship('Organization', back_populates='projects')  # Relationship to Organization
    team = relationship('Team', back_populates='project', uselist=False)  # One team per project

class Team(db.Model):
    __tablename__ = 'teams'
    ProjectID = Column(Integer, ForeignKey('projects.ProjectID'), primary_key=True)
    EmployeeIDs = Column(db.JSON)  # Array of EmployeeIDs
    TotalEmployees = Column(Integer)
    OrgID = Column(Integer, ForeignKey('organizations.OrgID'))
    
    project = relationship('Project', back_populates='team')
    organization = relationship('Organization', back_populates='teams')
