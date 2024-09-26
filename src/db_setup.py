# src/db_setup.py

import os
import json
import logging
from datetime import datetime
from src import create_app, db
from src.models import Organization, Skill, Employee, Project, Team

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(name)s:%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def drop_all_tables():
    """Drops all tables in the database."""
    db.drop_all()
    logger.info("All tables dropped successfully.")

def create_tables():
    """Creates all tables based on the models."""
    db.create_all()
    logger.info("Tables created successfully.")

def populate_initial_data():
    """Populates the database with initial data from JSON files."""
    # Define the path to the data directory
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    # 1. Populate Organizations
    orgs = [
        {'OrgID': 1, 'OrgName': 'OrgA'},
        {'OrgID': 2, 'OrgName': 'OrgB'}
    ]
    for org_data in orgs:
        org = Organization(**org_data)
        db.session.merge(org)  # Use merge to avoid duplicates
    logger.info("Organizations merged.")

    # 2. Extract and Populate Skills Dynamically
    users_file = os.path.join(data_dir, 'sample_users.json')
    projects_file = os.path.join(data_dir, 'sample_projects.json')

    skills_set = set()

    # Extract skills from users
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
            for user in users:
                for skill in user.get('skills', []):
                    skills_set.add(skill['name'])
        logger.info(f"Extracted {len(skills_set)} unique skills from users.")

    # Extract skills from projects
    if os.path.exists(projects_file):
        with open(projects_file, 'r') as f:
            projects = json.load(f)
            for project in projects:
                required_resources = project.get('required_resources', [])
                for resource in required_resources:
                    for skill in resource.get('Skills', []):
                        skills_set.add(skill)
        logger.info(f"Extracted skills from projects.")

    # Add skills to the database
    existing_skills = {skill.SkillName for skill in db.session.query(Skill.SkillName).all()}
    new_skills = skills_set - existing_skills
    for skill_name in sorted(new_skills):
        skill = Skill(SkillName=skill_name)
        db.session.add(skill)
        logger.info(f"Added skill: {skill_name}")
    
    db.session.commit()
    logger.info(f"Total skills in database: {len(existing_skills) + len(new_skills)}")

    # 3. Populate Employees
    if os.path.exists(users_file):
        with open(users_file, 'r') as f:
            users = json.load(f)
            for user in users:
                employee = Employee(
                    EmployeeID=user['EmployeeID'],
                    Name=user['Name'],
                    Rate=user.get('Rate'),
                    PastJobTitles=user.get('PastJobTitles', []),  # JSON array
                    CurrentJobTitle=user.get('CurrentJobTitle'),
                    PastWorkDomains=user.get('PastWorkDomains', []),  # JSON array
                    YearsOfExperience=user.get('YearsOfExperience'),
                    AvailableDate=datetime.strptime(user['AvailableDate'], '%Y-%m-%d') if user.get('AvailableDate') else None,
                    OrgID=user.get('OrgID')
                )
                db.session.merge(employee)
                logger.info(f"Added/Updated employee: {employee.Name}")
    logger.info("Employees populated.")

    # 4. Populate Projects
    if os.path.exists(projects_file):
        with open(projects_file, 'r') as f:
            projects = json.load(f)
            for project in projects:
                required_resources = project.get('required_resources', [])
                project_obj = Project(
                    ProjectID=project['ProjectID'],
                    ProjectName=project['ProjectName'],
                    NumberOfDays=project.get('number_of_days'),
                    ProjectStartDate=datetime.strptime(project['project_start_date'], '%Y-%m-%d') if project.get('project_start_date') else None,
                    Technology=project.get('technology'),
                    Domain=project.get('domain'),
                    RequiredResources=required_resources,
                    OrgID=project.get('OrgID')
                )
                db.session.merge(project_obj)
                logger.info(f"Added/Updated project: {project_obj.ProjectName}")
    logger.info("Projects populated.")

    # 5. Populate Teams (Initially empty or based on some logic)
    # For simplicity, initializing teams as empty. Team assignment will be handled by team_formation.py
    logger.info("Teams will be populated by team_formation.py.")
    
    db.session.commit()
    logger.info("Initial data populated successfully.")

def main():
    """Main function to setup the database."""
    app = create_app()
    with app.app_context():
        drop_all_tables()
        create_tables()
        populate_initial_data()

if __name__ == "__main__":
    main()
