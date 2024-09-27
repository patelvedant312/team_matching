from flask import Blueprint, request, jsonify
from app.models import Resource, db

resources_bp = Blueprint('resources', __name__)

# GET all resources
@resources_bp.route('/resources', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([resource.serialize() for resource in resources])

# GET resource by ID
@resources_bp.route('/resources/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return jsonify(resource.serialize())

# POST (Create) new resource
@resources_bp.route('/resources', methods=['POST'])
def create_resource():
    data = request.get_json()

    new_resource = Resource(
        Name=data['Name'],
        Rate=data.get('Rate'),
        PastJobTitles=data.get('PastJobTitles', []),
        CurrentJobTitle=data.get('CurrentJobTitle'),
        PastWorkDomains=data.get('PastWorkDomains', []),
        YearsOfExperience=data.get('YearsOfExperience', 0),
        AvailableDate=data.get('AvailableDate'),
        OrgID=data.get('OrgID')
    )

    db.session.add(new_resource)
    db.session.commit()

    return jsonify(new_resource.serialize()), 201

# PUT (Update) existing resource
@resources_bp.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get_or_404(id)
    data = request.get_json()

    resource.Name = data['Name']
    resource.Rate = data.get('Rate')
    resource.PastJobTitles = data.get('PastJobTitles', [])
    resource.CurrentJobTitle = data.get('CurrentJobTitle')
    resource.PastWorkDomains = data.get('PastWorkDomains', [])
    resource.YearsOfExperience = data.get('YearsOfExperience', 0)
    resource.AvailableDate = data.get('AvailableDate')
    resource.OrgID = data.get('OrgID')

    db.session.commit()

    return jsonify(resource.serialize())

# DELETE resource
@resources_bp.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()

    return jsonify({"message": "Resource deleted successfully"})
