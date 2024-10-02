from flask import Blueprint, request, jsonify
from app.models import Resource, db

resources_bp = Blueprint('resources', __name__)

# GET all resources
@resources_bp.route('/', methods=['GET'])
def get_resources():
    resources = Resource.query.all()
    return jsonify([resource.serialize() for resource in resources])

# GET resource by ID
@resources_bp.route('/<int:id>', methods=['GET'])
def get_resource(id):
    resource = Resource.query.get_or_404(id)
    return jsonify(resource.serialize())

@resources_bp.route('/', methods=['POST'])
def create_resource():
    try:
        data = request.get_json()
        new_resource = Resource(
            Name=data['Name'],
            Rate=data['Rate'],
            Skills=data['Skills'],
            PastJobTitles=data['PastJobTitles'],
            Domain=data['Domain'],
            AvailableDate=data.get('AvailableDate'),
            OrgID=data['OrgID'],
            TeamID=data.get('TeamID')  # TeamID is optional
        )
        db.session.add(new_resource)
        db.session.commit()
        return jsonify(new_resource.serialize()), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error: {str(e)}")
        return jsonify({"error": "Something went wrong while creating the resource"}), 500


# PUT (Update) existing resource
@resources_bp.route('/<int:id>', methods=['PUT'])
def update_resource(id):
    resource = Resource.query.get_or_404(id)
    data = request.get_json()
    resource.Name = data['Name']
    resource.Rate = data['Rate']
    resource.Skills = data['Skills']
    resource.PastJobTitles = data['PastJobTitles']
    resource.Domain = data['Domain']
    resource.AvailableDate = data.get('AvailableDate')
    resource.OrgID = data['OrgID']
    resource.TeamID = data.get('TeamID')  # TeamID is optional
    db.session.commit()
    return jsonify(resource.serialize())

# DELETE resource
@resources_bp.route('/<int:id>', methods=['DELETE'])
def delete_resource(id):
    resource = Resource.query.get_or_404(id)
    db.session.delete(resource)
    db.session.commit()
    return jsonify({"message": "Resource deleted successfully"})
