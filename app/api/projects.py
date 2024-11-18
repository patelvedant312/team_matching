# app/api/projects.py

from flask import Blueprint, request, jsonify
from app.Files_Database.projects_db import (
    get_all_projects,
    get_project_by_id,
    create_new_project,
    update_project,
    delete_project
)
from sqlalchemy.exc import IntegrityError
import logging

# Configure logging (you can configure this elsewhere in your app)
logging.basicConfig(level=logging.INFO)

projects_bp = Blueprint('projects', __name__)

# GET all projects for a given organization
@projects_bp.route('/all', methods=['GET'])
def get_all_projects_route():
    try:
        org_id = request.args.get('orgID')
        if not org_id:
            return jsonify({"error": "orgID is required"}), 400

        projects = get_all_projects(org_id)
        serialized_projects = [project.serialize() for project in projects]
        logging.info("Successfully retrieved all projects.")
        return jsonify(serialized_projects), 200
    except Exception as e:
        logging.error(f"Error retrieving projects: {e}")
        return jsonify({"error": str(e)}), 500

# GET project by ID for a given organization
@projects_bp.route('/by-id', methods=['GET'])
def get_project_by_id_route():
    try:
        org_id = request.args.get('orgID')
        project_id = request.args.get('projectID', type=int)

        if not org_id or not project_id:
            return jsonify({"error": "orgID and projectID are required"}), 400

        project = get_project_by_id(project_id, org_id)
        if project:
            serialized_project = project.serialize()
            logging.info(f"Successfully retrieved project with ID {project_id}.")
            return jsonify(serialized_project), 200
        else:
            logging.warning(f"Project with ID {project_id} not found.")
            return jsonify({"error": "Project not found"}), 404
    except Exception as e:
        logging.error(f"Error retrieving project with ID {project_id}: {e}")
        return jsonify({"error": str(e)}), 500

# POST (Create) new project
@projects_bp.route('/', methods=['POST'])
def create_project_route():
    try:
        org_id = request.args.get('orgID')
        if not org_id:
            return jsonify({"error": "orgID is required"}), 400

        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        data['OrgID'] = org_id  # Ensure OrgID is included in the data
        new_project = create_new_project(data)
        serialized_project = new_project.serialize()
        logging.info(f"Successfully created project with ID {new_project.ProjectID}.")
        return jsonify(serialized_project), 201
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except IntegrityError as ie:
        logging.error(f"IntegrityError: {ie}")
        return jsonify({"error": "Database integrity error: " + str(ie.orig)}), 400
    except Exception as e:
        logging.error(f"Error creating project: {e}")
        return jsonify({"error": str(e)}), 500

# PUT (Update) existing project
@projects_bp.route('/', methods=['PUT'])
def update_project_route():
    try:
        org_id = request.args.get('orgID')
        project_id = request.args.get('projectID', type=int)
        if not org_id or not project_id:
            return jsonify({"error": "orgID and projectID are required"}), 400

        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        updated_project = update_project(project_id, org_id, data)
        serialized_project = updated_project.serialize()
        logging.info(f"Successfully updated project with ID {project_id}.")
        return jsonify(serialized_project), 200
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except IntegrityError as ie:
        logging.error(f"IntegrityError: {ie}")
        return jsonify({"error": "Database integrity error: " + str(ie.orig)}), 400
    except Exception as e:
        logging.error(f"Error updating project with ID {project_id}: {e}")
        return jsonify({"error": str(e)}), 500

# DELETE project
@projects_bp.route('/', methods=['DELETE'])
def delete_project_route():
    try:
        org_id = request.args.get('orgID')
        project_id = request.args.get('projectID', type=int)
        if not org_id or not project_id:
            return jsonify({"error": "orgID and projectID are required"}), 400

        result = delete_project(project_id, org_id)
        logging.info(f"Successfully deleted project with ID {project_id}.")
        return jsonify(result), 200
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Error deleting project with ID {project_id}: {e}")
        return jsonify({"error": str(e)}), 500
