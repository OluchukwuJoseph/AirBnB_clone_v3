#!/usr/bin/python3
"""
    This module contains views for User objects that handles
    all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve all user objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a user object"""
    user = storage.get(User, user_id)
    # Return 404 if user does not exist
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete User object"""
    user = storage.get(User, user_id)
    # Return 404 if user does not exist
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user"""
    # Check if user passed correct data
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")
    # Create new user
    data = request.get_json()
    user = User(**data)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update user"""
    # Check if user passed correct data
    if not request.get_json():
        abort(400, description="Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    unchangeable_atributes = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in unchangeable_atributes:
            setattr(user, key, value)
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
