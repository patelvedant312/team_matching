# app/api/resources.py

from flask import Blueprint, request, jsonify
from app.db.resources_db import (
    get_all_resources,
    get_resource_by_id,
    create_new_resource,
    update_resource,
    delete_resource
)

resources_bp = Blueprint('resources', __name__)

# GET all resources for a given organization
@resources_bp.route('/all', methods=['GET'])
def get_all_resources_route():
    try:
        org_id = request.args.get('orgID')
        if not org_id:
            return jsonify({"error": "orgID is required"}), 400

        resources = get_all_resources(org_id)
        serialized_resources = [resource.serialize() for resource in resources]
        return jsonify(serialized_resources), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET resource by ID for a given organization
@resources_bp.route('/by-id', methods=['GET'])
def get_resource_by_id_route():
    try:
        org_id = request.args.get('orgID')
        resource_id = request.args.get('resourceID', type=int)

        if not org_id or not resource_id:
            return jsonify({"error": "orgID and resourceID are required"}), 400

        resource = get_resource_by_id(resource_id, org_id)
        if resource:
            return jsonify(resource.serialize()), 200
        else:
            return jsonify({"error": "Resource not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST (Create) new resource
@resources_bp.route('/', methods=['POST'])
def create_resource():
    try:
        org_id = request.args.get('orgID')
        if not org_id:
            return jsonify({"error": "orgID is required"}), 400
        data = request.get_json()
        data['OrgID'] = org_id
        new_resource = create_new_resource(data)
        return jsonify(new_resource.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT (Update) existing resource
@resources_bp.route('/', methods=['PUT'])
def update_resource_route():
    try:
        org_id = request.args.get('orgID')
        resource_id = request.args.get('resourceID', type=int)
        if not org_id or not resource_id:
            return jsonify({"error": "orgID and resourceID are required"}), 400
        data = request.get_json()
        updated_resource = update_resource(resource_id, org_id, data)
        return jsonify(updated_resource.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE resource
@resources_bp.route('/', methods=['DELETE'])
def delete_resource_route():
    try:
        org_id = request.args.get('orgID')
        resource_id = request.args.get('resourceID', type=int)
        if not org_id or not resource_id:
            return jsonify({"error": "orgID and resourceID are required"}), 400
        result = delete_resource(resource_id, org_id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
