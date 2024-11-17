# app/db/projects_db.py

from app.models import Project
from app import db
from datetime import datetime
from sqlalchemy.exc import IntegrityError
import logging

# Configure logging (you can configure this elsewhere in your app)
logging.basicConfig(level=logging.INFO)

def get_all_projects():
    """
    Retrieve all Project instances from the database.
    """
    try:
        projects = Project.query.all()
        logging.info(f"Retrieved {len(projects)} projects.")
        return projects
    except Exception as e:
        logging.error(f"Error retrieving all projects: {e}")
        raise e

def get_project_by_id(project_id):
    """
    Retrieve a single Project instance by its ID.
    """
    try:
        project = Project.query.get(project_id)
        if not project:
            raise ValueError("Project not found")
        logging.info(f"Retrieved project with ID {project_id}.")
        return project
    except Exception as e:
        logging.error(f"Error retrieving project by ID {project_id}: {e}")
        raise e

def create_new_project(data):
    """
    Create a new Project instance and add it to the database.
    """
    try:
        # Extract and validate data
        required_fields = ['ProjectName', 'OrgID', 'NumberOfDays', 'ProjectStartDate', 'Technology', 'Domain', 'RequiredResources']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            raise ValueError(f"Missing required fields: {', '.join(missing_fields)}")

        project_name = data['ProjectName']
        org_id = data['OrgID']
        number_of_days = data['NumberOfDays']
        project_start_date_str = data['ProjectStartDate']
        technology = data['Technology']
        domain = data['Domain']
        required_resources = data['RequiredResources']

        # Validate data types
        if not isinstance(technology, list) or not all(isinstance(item, str) for item in technology):
            raise ValueError("Technology must be a list of strings.")
        if not isinstance(domain, list) or not all(isinstance(item, str) for item in domain):
            raise ValueError("Domain must be a list of strings.")
        if not isinstance(required_resources, list):
            raise ValueError("RequiredResources must be a list.")

        # Convert ProjectStartDate from string to date object
        try:
            project_start_date = datetime.strptime(project_start_date_str, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("ProjectStartDate must be in 'YYYY-MM-DD' format.")

        # Create Project instance
        project = Project(
            ProjectName=project_name,
            OrgID=org_id,
            NumberOfDays=number_of_days,
            ProjectStartDate=project_start_date,
            Technology=technology,
            Domain=domain,
            RequiredResources=required_resources  # Stored as JSONB
        )

        db.session.add(project)
        db.session.commit()
        logging.info(f"Created new project with ID {project.ProjectID}.")
        return project

    except KeyError as e:
        db.session.rollback()
        logging.error(f"Missing field during project creation: {e}")
        raise ValueError(f"Missing field: {e.args[0]}")
    except ValueError as ve:
        db.session.rollback()
        logging.error(f"Value error during project creation: {ve}")
        raise ve
    except IntegrityError as ie:
        db.session.rollback()
        logging.error(f"Integrity error during project creation: {ie}")
        raise ValueError(f"Database integrity error: {ie.orig}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error during project creation: {e}")
        raise e

def update_project(project_id, data):
    """
    Update an existing Project instance.
    """
    try:
        project = Project.query.get(project_id)
        if not project:
            raise ValueError("Project not found")

        # Update fields if present in data
        if 'ProjectName' in data:
            project.ProjectName = data['ProjectName']
        if 'OrgID' in data:
            project.OrgID = data['OrgID']
        if 'NumberOfDays' in data:
            project.NumberOfDays = data['NumberOfDays']
        if 'ProjectStartDate' in data:
            try:
                project.ProjectStartDate = datetime.strptime(data['ProjectStartDate'], '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("ProjectStartDate must be in 'YYYY-MM-DD' format.")
        if 'Technology' in data:
            if not isinstance(data['Technology'], list) or not all(isinstance(item, str) for item in data['Technology']):
                raise ValueError("Technology must be a list of strings.")
            project.Technology = data['Technology']
        if 'Domain' in data:
            if not isinstance(data['Domain'], list) or not all(isinstance(item, str) for item in data['Domain']):
                raise ValueError("Domain must be a list of strings.")
            project.Domain = data['Domain']
        if 'RequiredResources' in data:
            if not isinstance(data['RequiredResources'], list):
                raise ValueError("RequiredResources must be a list.")
            project.RequiredResources = data['RequiredResources']

        db.session.commit()
        logging.info(f"Updated project with ID {project_id}.")
        return project

    except ValueError as ve:
        db.session.rollback()
        logging.error(f"Value error during project update: {ve}")
        raise ve
    except IntegrityError as ie:
        db.session.rollback()
        logging.error(f"Integrity error during project update: {ie}")
        raise ValueError(f"Database integrity error: {ie.orig}")
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error during project update: {e}")
        raise e

def delete_project(project_id):
    """
    Delete a Project instance from the database.
    """
    try:
        project = Project.query.get(project_id)
        if not project:
            raise ValueError("Project not found")

        db.session.delete(project)
        db.session.commit()
        logging.info(f"Deleted project with ID {project_id}.")
        return {"message": "Project deleted successfully"}
    except ValueError as ve:
        db.session.rollback()
        logging.error(f"Value error during project deletion: {ve}")
        raise ve
    except Exception as e:
        db.session.rollback()
        logging.error(f"Unexpected error during project deletion: {e}")
        raise e
