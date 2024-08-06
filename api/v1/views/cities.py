#!/usr/bin/python3
"""
    This module contains views for City objects that handles
    all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.city import City
from models.state import State
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Retrieves the list of all cities object belonging to a state"""
    state = storage.get(State, state_id)
    # Return 404 if state does not exist
    if not state:
        abort(404)
    # Return 404 if state has no cities
    if len(state.cities) == 0:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a city object"""
    city = storage.get(City, city_id)
    # Return 404 if state does not exist
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a city object"""
    city = storage.get(City, city_id)
    # Return 404 if state does not exist
    if not city:
        abort(404)
    # Delete city and save to update
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Create a city object"""
    # Check if user passed correct data
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'name' not in request.get_json():
        abort(400, description="Missing name")
    state = storage.get(State, state_id)
    # Return 404 if state does not exist
    if not state:
        abort(404)
    # Create new city
    data = request.get_json()
    city = City(**data, state_id=state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_state(city_id):
    """Update a city object"""
    # Check if user passed correct data
    if not request.get_json():
        abort(400, description="Not a JSON")
    city = storage.get(City, city_id)
    # Return 404 if state does not exist
    if not city:
        abort(404)
    data = request.get_json()
    unchangeable_attributes = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in unchangeable_attributes:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
