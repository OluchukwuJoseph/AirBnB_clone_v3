#!/usr/bin/python3
"""Implementation of a script that handles all default RESTFul API actions"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import state

@app_views.route('/api/v1/states', methods=['GET'])
def retrieveStates():
    """Retrieve the list of all State objects."""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

@app_views.route('/api/v1/states/<state_id>', methods=['GET'])
def getState(state_id):
    """retrieve a state object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/api/v1/states/<state_id>', methods=['DELETE'])
def deleteState(state_id):
    """Delete a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    # delete the state
    storage.delete(state)

    # save to update the state
    storage.save()

    # return  a json with a status
    return jsonify({}), 200

@app_views.route('/api/v1/states', methods=['POST'])
def createState():
    """Create a State."""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")
    # request data
    data = request.get_json()
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new.state.to_dict()), 201

@app_views.route('/api/v1/state/<state_id>', methods=['PUT'])
def updateState(state_id):
    """Update a State object."""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignored_keys = {'id', 'created_at', 'updated_at'}
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
