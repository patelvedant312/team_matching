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

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/', methods=['GET'])
def get_projects():
    """
    Retrieve all projects.
    """
    try:
        projects = get_all_projects()
        serialized_projects = [project.serialize() for project in projects]
        logging.info("Successfully retrieved all projects.")
        return jsonify(serialized_projects), 200
    except Exception as e:
        logging.error(f"Error retrieving projects: {e}")
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    """
    Retrieve a single project by ID.
    """
    try:
        project = get_project_by_id(id)
        serialized_project = project.serialize()
        logging.info(f"Successfully retrieved project with ID {id}.")
        return jsonify(serialized_project), 200
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Error retrieving project with ID {id}: {e}")
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/', methods=['POST'])
def create_project():
    """
    Create a new project.
    """
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

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

@projects_bp.route('/<int:id>', methods=['PUT'])
def update_project_route(id):
    """
    Update an existing project.
    """
    try:
        data = request.get_json()
        if not data:
            raise ValueError("No input data provided")

        updated_project = update_project(id, data)
        serialized_project = updated_project.serialize()
        logging.info(f"Successfully updated project with ID {id}.")
        return jsonify(serialized_project), 200
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 400
    except IntegrityError as ie:
        logging.error(f"IntegrityError: {ie}")
        return jsonify({"error": "Database integrity error: " + str(ie.orig)}), 400
    except Exception as e:
        logging.error(f"Error updating project with ID {id}: {e}")
        return jsonify({"error": str(e)}), 500

@projects_bp.route('/<int:id>', methods=['DELETE'])
def delete_project_route(id):
    """
    Delete a project.
    """
    try:
        result = delete_project(id)
        logging.info(f"Successfully deleted project with ID {id}.")
        return jsonify(result), 200
    except ValueError as ve:
        logging.warning(f"ValueError: {ve}")
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        logging.error(f"Error deleting project with ID {id}: {e}")
        return jsonify({"error": str(e)}), 500
