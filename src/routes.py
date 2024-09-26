# src/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from .models import Employee, Project, Team, Organization, Skill, employee_skill_association
from .team_formation import match_users_to_projects
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

        # Create new employee
        new_employee = Employee(
            Name=name,
            Rate=rate,
            AvailableDate=datetime.strptime(available_date, '%Y-%m-%d'),
            OrgID=org.OrgID
        )
        db.session.add(new_employee)
        db.session.flush()  # Flush to get EmployeeID

        # Add skills to association table
        for skill_info in skills:
            skill = Skill.query.filter_by(SkillName=skill_info['name']).first()
            if not skill:
                skill = Skill(SkillName=skill_info['name'])
                db.session.add(skill)
                db.session.flush()
            db.session.execute(employee_skill_association.insert().values(
                EmployeeID=new_employee.EmployeeID,
                SkillID=skill.SkillID,
                Level=skill_info['level']
            ))

        db.session.commit()
        return redirect(url_for('main.index'))
    return render_template('add_user.html')

@main.route('/add_project', methods=['GET', 'POST'])
def add_project():
    if request.method == 'POST':
        # Get form data
        project_name = request.form['project_name']
        required_resources = json.loads(request.form['required_resources'])  # Expecting JSON list of {"Role": "...", "Level": "...", "Skills": [...], "Quantity": ...}
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
    project_assignments, unfilled_roles = match_users_to_projects()

    # Fetch all projects and their assignments
    projects = Project.query.all()
    assignments = []
    for project in projects:
        team = Team.query.filter_by(ProjectID=project.ProjectID).first()
        if team:
            assigned_employees = Employee.query.filter(Employee.EmployeeID.in_(team.EmployeeIDs)).all()
        else:
            assigned_employees = []
        assignments.append({
            'Project': project,
            'Employees': assigned_employees
        })

    return render_template('match_results.html', assignments=assignments, unfilled_roles=unfilled_roles)
