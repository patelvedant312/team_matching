# app/api/teams.py

from flask import Blueprint, request, jsonify
from app.services.team_formation import match_resources_to_projects
from app.models.project import Project
from app.models.resource import Resource
import logging
from app.db.teams_db import (
    get_all_teams,
    get_team_by_id,
    create_new_team,
    update_team,
    delete_team
)

teams_bp = Blueprint('teams', __name__)
logger = logging.getLogger(__name__)

@teams_bp.route('/', methods=['GET'])
def get_teams():
    try:
        teams = get_all_teams()
        serialized_teams = [team.serialize() for team in teams]
        return jsonify(serialized_teams), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teams_bp.route('/<int:id>', methods=['GET'])
def get_team(id):
    try:
        team = get_team_by_id(id)
        return jsonify(team.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# @teams_bp.route('/', methods=['POST'])
# def create_team():
#     try:
#         data = request.get_json()
#         new_team = create_new_team(data)
#         return jsonify(new_team.serialize()), 201
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

@teams_bp.route('/<int:project_id>', methods=['POST'])
def create_team(project_id):
    try:
        # Fetch the specific project
        project = Project.query.get(project_id)
        if not project:
            return jsonify({"error": f"Project with ID {project_id} not found."}), 404
        logger.info(f"Processing project '{project.ProjectName}' (ID: {project.ProjectID})")

        # Fetch resources available after the project's start date and not already assigned
        resources = Resource.query.filter(
            (Resource.AvailableDate == None) | 
            (Resource.AvailableDate > project.ProjectStartDate),
            Resource.TeamID == None  # Exclude resources already assigned
        ).all()
        logger.info(f"Found {len(resources)} available resources for project '{project.ProjectName}'.")

        if not resources:
            logger.warning(f"No available resources for project '{project.ProjectName}'.")
            return jsonify({"error": 'No available resources for this project.'}), 400

        # Call the team formation algorithm with the filtered resources
        team_data, unfilled_roles = match_resources_to_projects(project_id, resources)

        # Return only the TeamID
        return jsonify({
            "TeamID": team_data['TeamID']
        }), 201
    except Exception as e:
        logger.error(f"Error in create_team: {e}")
        return jsonify({"error": str(e)}), 500

@teams_bp.route('/<int:id>', methods=['PUT'])
def update_team_route(id):
    try:
        data = request.get_json()
        updated_team = update_team(id, data)
        return jsonify(updated_team.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@teams_bp.route('/<int:id>', methods=['DELETE'])
def delete_team_route(id):
    try:
        result = delete_team(id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
