#!/usr/bin/python3
"""Index Module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns API status"""
    data = {"status": "OK"}
    return jsonify(data)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of objects by type"""
    object_count = {}
    object_count['amenities'] = storage.count(Amenity)
    object_count['cities'] = storage.count(City)
    object_count['places'] = storage.count(Place)
    object_count['reviews'] = storage.count(Review)
    object_count['states'] = storage.count(State)
    object_count['users'] = storage.count(User)

    return jsonify(object_count)
