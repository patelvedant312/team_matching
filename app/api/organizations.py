# api/organizations.py

from flask import Blueprint, request, jsonify
from app.db.organizations_db import (
    get_all_organizations,
    get_organization_by_id,
    create_new_organization,
    update_organization,
    delete_organization
)

organizations_bp = Blueprint('organizations', __name__)

@organizations_bp.route('/', methods=['GET'])
def get_organizations():
    try:
        organizations = get_all_organizations()
        serialized_orgs = [org.serialize() for org in organizations]
        return jsonify(serialized_orgs), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@organizations_bp.route('/<int:id>', methods=['GET'])
def get_organization(id):
    try:
        organization = get_organization_by_id(id)
        return jsonify(organization.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@organizations_bp.route('/', methods=['POST'])
def create_organization():
    try:
        data = request.get_json()
        new_organization = create_new_organization(data)
        return jsonify(new_organization.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@organizations_bp.route('/<int:id>', methods=['PUT'])
def update_organization_route(id):
    try:
        data = request.get_json()
        updated_organization = update_organization(id, data)
        return jsonify(updated_organization.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@organizations_bp.route('/<int:id>', methods=['DELETE'])
def delete_organization_route(id):
    try:
        result = delete_organization(id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
