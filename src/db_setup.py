import os
import json
import logging
from datetime import datetime
from src import create_app, db
from src.models import Organization, Resource, Project, Team

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def drop_all_tables():
    db.drop_all()
    logger.info("All tables dropped successfully.")

def create_tables():
    db.create_all()
    logger.info("Tables created successfully.")

def populate_initial_data():
    data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')

    # 1. Populate Organizations
    orgs = [{'OrgID': 1, 'OrgName': 'OrgA'}, {'OrgID': 2, 'OrgName': 'OrgB'}, {'OrgID': 3, 'OrgName': 'OrgC'}]
    for org_data in orgs:
        org = Organization(**org_data)
        db.session.merge(org)
    logger.info("Organizations merged.")

    # 2. Populate Resources (Skills and PastJobTitles in new format)
    resources_file = os.path.join(data_dir, 'sample_resources.json')
    if os.path.exists(resources_file):
        with open(resources_file, 'r') as f:
            resources = json.load(f)
            for user in resources:
                # Loading resources from JSON
                resource = Resource(
                    ResourceID=user['ResourceID'],
                    Name=user['Name'],
                    Rate=user.get('Rate'),  # Ensure it fetches the numeric value
                    Skills=user.get('Skills', []),
                    PastJobTitles=user.get('PastJobTitles', []),
                    Domain=user.get('Domain', []),
                    AvailableDate=datetime.strptime(user['AvailableDate'], '%Y-%m-%d') if user.get('AvailableDate') else None,
                    OrgID=user.get('OrgID')
                )

                db.session.merge(resource)
                logger.info(f"Added/Updated resource: {resource.Name}")
    logger.info("Resources populated.")

    # 3. Populate Projects (Updated required_resource schema)
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

def main():
    app = create_app()
    with app.app_context():
        drop_all_tables()
        create_tables()
        populate_initial_data()

if __name__ == "__main__":
    main()
