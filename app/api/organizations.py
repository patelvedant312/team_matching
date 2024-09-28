from flask import Blueprint, request, jsonify
from app.models import Organization, db

organizations_bp = Blueprint('organizations', __name__)

# GET all organizations
@organizations_bp.route('/organizations', methods=['GET'])
def get_organizations():
    organizations = Organization.query.all()
    return jsonify([organization.serialize() for organization in organizations])

# GET organization by ID
@organizations_bp.route('/organizations/<int:id>', methods=['GET'])
def get_organization(id):
    organization = Organization.query.get_or_404(id)
    return jsonify(organization.serialize())

# POST (Create) new organization
@organizations_bp.route('/organizations', methods=['POST'])
def create_organization():
    data = request.get_json()
    new_organization = Organization(
        OrgName=data['OrgName']
    )
    db.session.add(new_organization)
    db.session.commit()
    return jsonify(new_organization.serialize()), 201

# PUT (Update) existing organization
@organizations_bp.route('/organizations/<int:id>', methods=['PUT'])
def update_organization(id):
    organization = Organization.query.get_or_404(id)
    data = request.get_json()
    organization.OrgName = data['OrgName']
    db.session.commit()
    return jsonify(organization.serialize())

# DELETE organization
@organizations_bp.route('/organizations/<int:id>', methods=['DELETE'])
def delete_organization(id):
    organization = Organization.query.get_or_404(id)
    db.session.delete(organization)
    db.session.commit()
    return jsonify({"message": "Organization deleted successfully"})
