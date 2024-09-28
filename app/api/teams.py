from flask import Blueprint, request, jsonify
from app.models import Team, db

teams_bp = Blueprint('teams', __name__)

# GET all teams
@teams_bp.route('/teams', methods=['GET'])
def get_teams():
    teams = Team.query.all()
    return jsonify([team.serialize() for team in teams])

# GET team by ID
@teams_bp.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    team = Team.query.get_or_404(id)
    return jsonify(team.serialize())

# POST (Create) new team
@teams_bp.route('/teams', methods=['POST'])
def create_team():
    data = request.get_json()
    new_team = Team(
        ProjectID=data['ProjectID'],
        TotalResources=data['TotalResources'],
        OrgID=data['OrgID']
    )
    db.session.add(new_team)
    db.session.commit()
    return jsonify(new_team.serialize()), 201

# PUT (Update) existing team
@teams_bp.route('/teams/<int:id>', methods=['PUT'])
def update_team(id):
    team = Team.query.get_or_404(id)
    data = request.get_json()
    team.ProjectID = data['ProjectID']
    team.TotalResources = data['TotalResources']
    team.OrgID = data['OrgID']
    db.session.commit()
    return jsonify(team.serialize())

# DELETE team
@teams_bp.route('/teams/<int:id>', methods=['DELETE'])
def delete_team(id):
    team = Team.query.get_or_404(id)
    db.session.delete(team)
    db.session.commit()
    return jsonify({"message": "Team deleted successfully"})
