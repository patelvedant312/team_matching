# app/db/teams_db.py

from app.models import db, Team

def get_all_teams():
    return Team.query.all()

def get_team_by_id(team_id):
    team = Team.query.get(team_id)
    if not team:
        raise ValueError("Team not found")
    return team

def create_new_team(data):
    new_team = Team(
        ProjectID=data['ProjectID'],
        TotalResources=data['TotalResources'],
        OrgID=data['OrgID']
    )
    db.session.add(new_team)
    db.session.commit()
    return new_team

def update_team(team_id, data):
    team = Team.query.get(team_id)
    if not team:
        raise ValueError("Team not found")
    
    team.ProjectID = data.get('ProjectID', team.ProjectID)
    team.TotalResources = data.get('TotalResources', team.TotalResources)
    team.OrgID = data.get('OrgID', team.OrgID)
    db.session.commit()
    return team

def delete_team(team_id):
    team = Team.query.get(team_id)
    if not team:
        raise ValueError("Team not found")
    
    db.session.delete(team)
    db.session.commit()
    return {"message": "Team deleted successfully"}
