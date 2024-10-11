# app/api/teams.py

from flask import Blueprint, request, jsonify
from app.db.teams_db import (
    get_all_teams,
    get_team_by_id,
    create_new_team,
    update_team,
    delete_team
)

teams_bp = Blueprint('teams', __name__)

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

@teams_bp.route('/', methods=['POST'])
def create_team():
    try:
        data = request.get_json()
        new_team = create_new_team(data)
        return jsonify(new_team.serialize()), 201
    except Exception as e:
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
