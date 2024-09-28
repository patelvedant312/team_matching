# src/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from src.Test.models import Resource, Project, Team, Organization
from src.Test.team_formation import match_resources_to_projects
from . import db
import json
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        # Get form data
        name = request.form['name']
        skills = json.loads(request.form['skills'])  # Expecting JSON list of {"name": "...", "level": "..."}
        rate = float(request.form['rate'])
        available_date = request.form['available_date']
        org_name = request.form['organization']

        # Find or create organization
        org = Organization.query.filter_by(OrgName=org_name).first()
        if not org:
            org = Organization(OrgName=org_name)
            db.session.add(org)
            db.session.commit()

        # Create new resource
        new_resource = Resource(
            Name=name,
            Rate=rate,
            Skills=skills,
            PastJobTitles=request.form.get('past_job_titles', []),
            Domain=request.form.get('domain', []),
            AvailableDate=datetime.strptime(available_date, '%Y-%m-%d') if available_date else None,
            OrgID=org.OrgID
        )
        db.session.add(new_resource)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_user.html')

@main.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        # Get form data
        project_name = request.form['project_name']
        required_resources = json.loads(request.form['required_resources'])  # Expecting JSON list of {"Role": "...", "Skills": [...], "Quantity": ...}
        project_start_date = request.form['project_start_date']
        number_of_days = int(request.form['number_of_days'])
        domain = request.form['domain']
        technology = request.form['technology']
        org_id = int(request.form['organization_id'])  # Assuming OrgID is provided

        # Create new project
        new_project = Project(
            ProjectName=project_name,
            RequiredResources=required_resources,
            ProjectStartDate=datetime.strptime(project_start_date, '%Y-%m-%d'),
            NumberOfDays=number_of_days,
            Domain=domain,
            Technology=technology,
            OrgID=org_id
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_project.html')

@main.route('/match_teams')
def match_teams():
    # Run the matching algorithm
    project_assignments, unfilled_roles = match_resources_to_projects()

    # Fetch all projects and their assignments
    projects = Project.query.all()
    assignments = []
    for project in projects:
        team = Team.query.filter_by(ProjectID=project.ProjectID).first()
        if team:
            assigned_employees = Resource.query.filter(Resource.ResourceID.in_(team.ResourceIDs)).all()
        else:
            assigned_employees = []
        assignments.append({
            'Project': project,
            'Employees': assigned_employees
        })

    return render_template('match_results.html', assignments=assignments, unfilled_roles=unfilled_roles)