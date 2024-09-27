# src/db_setup.py

import os
import json
import logging
from datetime import datetime
from src import create_app, db
from src.models import Organization, Resource, Project, Team
from decimal import Decimal
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Predefined Organizations (ensure consistency with models.py)
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

def populate_initial_data():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    # 1. Populate Organizations
    orgs = ORGANIZATIONS
    for org_data in orgs:
        org = Organization(**org_data)
        db.session.merge(org)
    logger.info("Organizations merged.")

    db.session.commit()

    # 2. Populate Resources
    resources_file = os.path.join(data_dir, 'sample_resources.json')
    if os.path.exists(resources_file):
        with open(resources_file, 'r') as f:
            resources = json.load(f)
            for user in resources:
                resource = Resource(
                    ResourceID=user['ResourceID'],
                    Name=user['Name'],
                    Rate=Decimal(str(user.get('Rate', '0'))),  # Ensure Rate is Decimal
                    Skills=user.get('Skills', {}),
                    PastJobTitles=user.get('PastJobTitles', {}),
                    Domain=user.get('Domain', []),
                    AvailableDate=datetime.strptime(user['AvailableDate'], '%Y-%m-%d') if user.get('AvailableDate') else None,
                    OrgID=user.get('OrgID'),
                    TeamID=None  # Initially, resources are not assigned to any team
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
                    Technology=project_data['Technology'],  # Assuming it's a list
                    Domain=project_data['Domain'],  # Assuming it's a list
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
            TotalResources=0,  # Will update after assigning resources
            OrgID=project.OrgID
        )
        db.session.add(team)
        db.session.commit()
        logger.info(f"Created team for project: {project.ProjectName}")

        # Assign Resources to Team based on RequiredResources
        for req in project.RequiredResources:
            role = req["Role"]
            required_skills = req["Skills"]  # Dictionary
            quantity = req["Quantity"]

            # Fetch resources that match the required skills and domain, and are not yet assigned to any team
            # This is a simplistic filter; you might need a more robust matching mechanism
            matching_resources = Resource.query.filter(
                Resource.Domain.overlap(project.Domain),
                Resource.TeamID == None  # Resources not yet assigned to any team
            ).all()

            # Filter resources that have the required skills at the desired levels
            suitable_resources = []
            for res in matching_resources:
                # Check if resource has all required skills with at least the required level
                has_all_skills = True
                for skill, details in required_skills.items():
                    res_skill = res.Skills.get(skill)
                    if not res_skill:
                        has_all_skills = False
                        break
                    # Define a hierarchy for skill levels
                    level_order = {"beginner": 1, "intermediate": 2, "expert": 3}
                    if level_order.get(res_skill['level'], 0) < level_order.get(details['level'], 0):
                        has_all_skills = False
                        break
                if has_all_skills:
                    suitable_resources.append(res)

            # Randomly select resources from suitable_resources
            random.shuffle(suitable_resources)
            selected_resources = suitable_resources[:quantity]

            # Assign selected resources to the team
            for res in selected_resources:
                res.TeamID = team.TeamID
                team.TotalResources += 1
                logger.info(f"Assigned resource '{res.Name}' to team of project '{project.ProjectName}' for role '{role}'.")

        db.session.commit()
        logger.info(f"Resources assigned to team for project: {project.ProjectName}")

def main():
    app = create_app()
    with app.app_context():
        drop_all_tables()
        create_tables()
        populate_initial_data()

if __name__ == "__main__":
    main()
