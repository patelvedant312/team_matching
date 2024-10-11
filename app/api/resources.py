# api/resources.py

from flask import Blueprint, request, jsonify
from app.db.resources_db import (
    get_all_resources,
    get_resource_by_id,
    create_new_resource,
    update_resource,
    delete_resource
)

resources_bp = Blueprint('resources', __name__)

# GET all resources
@resources_bp.route('/', methods=['GET'])
def get_resources():
    try:
        resources = get_all_resources()
        serialized_resources = [resource.serialize() for resource in resources]
        return jsonify(serialized_resources), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET resource by ID
@resources_bp.route('/<int:id>', methods=['GET'])
def get_resource(id):
    try:
        resource = get_resource_by_id(id)
        return jsonify(resource.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# POST (Create) new resource
@resources_bp.route('/', methods=['POST'])
def create_resource():
    try:
        data = request.get_json()
        new_resource = create_new_resource(data)
        return jsonify(new_resource.serialize()), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# PUT (Update) existing resource
@resources_bp.route('/<int:id>', methods=['PUT'])
def update_resource_route(id):
    try:
        data = request.get_json()
        updated_resource = update_resource(id, data)
        return jsonify(updated_resource.serialize()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE resource
@resources_bp.route('/<int:id>', methods=['DELETE'])
def delete_resource_route(id):
    try:
        result = delete_resource(id)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
