# app/database/projects_db.py

from app import db
from app.models.project import Project
from datetime import datetime

def get_all_projects(org_id):
    if org_id:
        projects = Project.query.filter_by(OrgID=org_id).all()
    else:
        projects = Project.query.all()
    return projects

def get_project_by_id(project_id, org_id):
    project = Project.query.filter_by(ProjectID=project_id, OrgID=org_id).first()
    return project

def create_new_project(data):
    try:
        new_project = Project(
            ProjectName=data['ProjectName'],
            OrgID=data['OrgID'],
            RequiredResources=data['RequiredResources'],
            NumberOfDays=data['NumberOfDays'],
            ProjectStartDate=datetime.strptime(data['ProjectStartDate'], '%Y-%m-%d') if data.get('ProjectStartDate') else None,
            Technology=data['Technology'],
            Domain=data['Domain']
        )
        db.session.add(new_project)
        db.session.commit()
        return new_project
    except Exception as e:
        db.session.rollback()
        raise e

def update_project(project_id, org_id, data):
    project = get_project_by_id(project_id, org_id)
    if not project:
        raise ValueError("Project not found")
    try:
        for key, value in data.items():
            if key == 'ProjectStartDate' and value:
                setattr(project, key, datetime.strptime(value, '%Y-%m-%d'))
            else:
                setattr(project, key, value)
        db.session.commit()
        return project
    except Exception as e:
        db.session.rollback()
        raise e

def delete_project(project_id, org_id):
    project = get_project_by_id(project_id, org_id)
    if not project:
        raise ValueError("Project not found")
    try:
        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted successfully"}
    except Exception as e:
        db.session.rollback()
        raise e
