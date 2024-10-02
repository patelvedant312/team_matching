from flask import Blueprint, request, jsonify
from app.models import Project, db

projects_bp = Blueprint('projects', __name__)

# GET all projects
@projects_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.serialize() for project in projects])

# GET project by ID
@projects_bp.route('/<int:id>', methods=['GET'])
def get_project(id):
    project = Project.query.get_or_404(id)
    return jsonify(project.serialize())

# POST (Create) new project
@projects_bp.route('/', methods=['POST'])
def create_project():
    print(request.get_json())

    data = request.get_json()
    new_project = Project(
        ProjectName=data['ProjectName'],
        OrgID=data['OrgID'],
        RequiredResources=data.get('RequiredResources', {}),
        NumberOfDays=data['NumberOfDays'],
        ProjectStartDate=data['ProjectStartDate'],
        Technology=data['Technology'],
        Domain=data['Domain']
    )
    
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.serialize()), 201

@projects_bp.route('/<int:id>', methods=['PUT'])
def update_project(id):
    project = Project.query.get_or_404(id)
    data = request.get_json()
    
    # Debugging print to see what's being passed for Technology
    print(f"Technology field: {data['Technology']}")  # This will show you if it's a dict or list
    
    if isinstance(data['Technology'], list):
        project.Technology = data['Technology']
    else:
        return jsonify({"error": "Technology must be a list of strings"}), 400
    
    # Other field updates
    project.ProjectName = data['ProjectName']
    project.OrgID = data['OrgID']
    project.RequiredResources = data.get('RequiredResources', {})
    project.NumberOfDays = data['NumberOfDays']
    project.ProjectStartDate = data['ProjectStartDate']
    project.Domain = data['Domain']
    
    db.session.commit()
    return jsonify(project.serialize())


# DELETE project
@projects_bp.route('/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted successfully"})
