# src/Test/db_setup.py

import os
import json
import logging
from datetime import datetime
from decimal import Decimal
from src.Test import create_app, db
from src.Test.models import Organization, Resource, Project, Team
from src.Test.utils import get_resource_skills_with_levels

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined Organizations
ORGANIZATIONS = [
    {"OrgID": 1, "OrgName": "OrgA"},
    {"OrgID": 2, "OrgName": "OrgB"},
    {"OrgID": 3, "OrgName": "OrgC"}
]

def drop_all_tables():
    db.drop_all()
    logger.info("All tables dropped successfully.")

def create_tables():
    db.create_all()
    logger.info("Tables created successfully.")

def is_level_sufficient(resource_level, required_level):
    levels = ['beginner', 'intermediate', 'expert']
    try:
        resource_index = levels.index(resource_level.lower())
        required_index = levels.index(required_level.lower())
        return resource_index >= required_index
    except ValueError:
        return False

def populate_initial_data():
    app = create_app()
    with app.app_context():
        drop_all_tables()
        create_tables()
        
        # 1. Populate Organizations
        for org_data in ORGANIZATIONS:
            org = Organization(**org_data)
            db.session.merge(org)
        logger.info("Organizations merged.")
        
        db.session.commit()
        
        # 2. Populate Resources
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..', 'data')
        resources_file = os.path.join(data_dir, 'sample_resources.json')
        if os.path.exists(resources_file):
            with open(resources_file, 'r') as f:
                resources = json.load(f)
                for user in resources:
                    resource = Resource(
                        ResourceID=user['ResourceID'],
                        Name=user['Name'],
                        Rate=Decimal(str(user.get('Rate', '0'))),
                        Skills=user.get('Skills', {}),
                        PastJobTitles=user.get('PastJobTitles', {}),
                        Domain=user.get('Domain', []),
                        AvailableDate=datetime.strptime(user['AvailableDate'], '%Y-%m-%d') if user.get('AvailableDate') else None,
                        OrgID=user.get('OrgID'),
                        TeamID=None
                    )
                    db.session.merge(resource)
                    logger.info(f"Added/Updated resource: {resource.Name}")
        logger.info("Resources populated.")
        
        db.session.commit()
        
        # 3. Populate Projects
        projects_file = os.path.join(data_dir, 'sample_projects.json')
        if os.path.exists(projects_file):
            with open(projects_file, 'r') as f:
                projects = json.load(f)
                for project_data in projects:
                    project = Project(
                        ProjectID=project_data['ProjectID'],
                        ProjectName=project_data['ProjectName'],
                        NumberOfDays=project_data.get('NumberOfDays', 0),
                        ProjectStartDate=datetime.strptime(project_data['ProjectStartDate'], '%Y-%m-%d'),
                        Technology=project_data['Technology'],
                        Domain=project_data['Domain'],
                        RequiredResources=project_data['RequiredResources'],
                        OrgID=project_data['OrgID']
                    )
                    db.session.merge(project)
                    logger.info(f"Added/Updated project: {project.ProjectName}")
        logger.info("Projects populated.")
        
        db.session.commit()
        
        # 4. Populate Teams and Assign Resources
        for project in Project.query.all():
            # Create a Team for each Project
            team = Team(
                ProjectID=project.ProjectID,
                TotalResources=0,
                OrgID=project.OrgID
            )
            db.session.add(team)
            db.session.commit()  # Commit to generate TeamID
            logger.info(f"Created team for project: {project.ProjectName}")
        
            # Assign Resources to Team based on RequiredResources
            for req in project.RequiredResources:
                role = req["Role"]
                required_skills = req["Skills"]
                quantity = req["Quantity"]
        
                # Fetch resources that match the required skills and domain, and are not yet assigned to any team
                matching_resources = Resource.query.filter(
                    Resource.Domain.overlap(project.Domain),
                    Resource.TeamID == None
                ).all()
        
                # Filter resources that have the required skills at the desired levels
                suitable_resources = []
                for res in matching_resources:
                    # Check if resource has all required skills with sufficient levels
                    has_all_skills = True
                    resource_skills = get_resource_skills_with_levels(res)
                    for skill, details in required_skills.items():
                        if not is_level_sufficient(resource_skills.get(skill.lower(), 'beginner'), details.get('level', 'beginner')):
                            has_all_skills = False
                            break
                    if has_all_skills:
                        suitable_resources.append(res)
        
                # Assign up to 'quantity' resources
                selected_resources = suitable_resources[:quantity]
        
                # Assign selected resources to the team
                for res in selected_resources:
                    res.TeamID = team.TeamID
                    team.TotalResources += 1
                    logger.info(f"Assigned resource '{res.Name}' to team of project '{project.ProjectName}' for role '{role}'.")
        
            db.session.commit()
            logger.info(f"Resources assigned to team for project: {project.ProjectName}")

def main():
    populate_initial_data()

if __name__ == "__main__":
    main()
